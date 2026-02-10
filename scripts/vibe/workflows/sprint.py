"""Vibe Sprint workflow implementation."""

import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..agents.claude import ClaudeAdapter
from ..agents.codex import CodexAdapter
from ..agents.gemini import GeminiAdapter
from ..state import VibeState
from .handoff import HandoffGenerator


class VibeSprint:
    """Manages the 3-phase Vibe Sprint workflow."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.state = VibeState(project_root)
        self.gemini = GeminiAdapter(project_root)
        self.claude = ClaudeAdapter(project_root)
        self.codex = CodexAdapter(project_root)
        self.handoff_gen = HandoffGenerator(project_root)

        # Ensure session_logs directory exists
        self.session_logs_dir = project_root / "session_logs"
        self.session_logs_dir.mkdir(exist_ok=True)

    def start(self, objective: str) -> str:
        """Start a new sprint."""
        sprint_id = self.state.start_sprint(objective)
        self._create_session_log(sprint_id, objective)
        print(f"\n✅ Sprint started: {sprint_id}")
        print(f"📋 Objective: {objective}")
        return sprint_id

    def phase_1_context(self) -> bool:
        """Phase 1: Context analysis with Gemini."""
        start_time = time.time()
        print("\n" + "=" * 80)
        print("PHASE 1: CONTEXT ANALYSIS (Gemini)")
        print("=" * 80)

        objective = self.state.get("sprint.objective")
        if not objective:
            print("❌ No active sprint. Run 'vibe sprint start' first.")
            return False

        self.state.set("sprint.status", "context_analysis")
        self.state.save()

        # Track agent invocation
        self.state.record_agent_invocation("gemini")

        # Invoke Gemini for context analysis
        response = self.gemini.analyze_context(objective)

        # Record timing
        duration = time.time() - start_time
        self.state.record_phase_time("context_analysis", duration)

        if not response.success:
            print(f"❌ Context analysis failed: {response.error}")
            self._log_phase("Context", "failed", error=response.error)
            # Post blocker to blackboard
            self.state.post_blocker(
                "gemini",
                "phase-1",
                f"Context analysis failed: {response.error}",
                error=response.error
            )
            return False

        # Save context summary
        context_file = self.session_logs_dir / f"{self.state.get('sprint.id')}_context.md"
        with open(context_file, "w") as f:
            f.write(response.output)

        self.state.set("context.repo_summary_path", str(context_file))

        # Estimate token usage (rough estimate based on output length)
        estimated_tokens = len(response.output.split()) * 1.3
        self.state.record_token_usage("gemini", int(estimated_tokens))

        self.state.save()

        print(f"\n✅ Context analysis complete: {context_file}")
        print(f"⏱️  Duration: {duration:.1f}s")
        self._log_phase("Context", "completed", output_file=str(context_file))
        return True

    def phase_2_plan(self) -> bool:
        """Phase 2: Planning with Claude Code."""
        start_time = time.time()
        print("\n" + "=" * 80)
        print("PHASE 2: PLANNING (Claude Code)")
        print("=" * 80)

        objective = self.state.get("sprint.objective")
        context_path = self.state.get("context.repo_summary_path")

        if not context_path or not Path(context_path).exists():
            print("⚠️  No context summary found. Run phase 1 first.")
            return False

        with open(context_path) as f:
            context_summary = f.read()

        self.state.set("sprint.status", "planning")
        self.state.record_agent_invocation("claude")
        self.state.save()

        # Check for unresolved blockers from context phase
        blockers = self.state.get_unresolved_blockers()
        if blockers:
            print(f"\n⚠️  WARNING: {len(blockers)} unresolved blockers from previous phases")
            print("Consider addressing these before planning:")
            for b in blockers[:3]:
                print(f"  - [{b['agent']}] {b['description']}")

        # Invoke Claude for planning
        response = self.claude.plan(objective, context_summary)

        # Record timing (even though it's manual)
        duration = time.time() - start_time
        self.state.record_phase_time("planning", duration)

        # Since Claude adapter returns a prompt for manual execution,
        # we need to wait for the user to create PLAN.md
        print("\n📝 Once you've created PLAN.md, run: vibe plan --load PLAN.md")
        self._log_phase("Planning", "awaiting_manual_completion")
        return True

    def load_plan(self, plan_path: Optional[Path] = None) -> bool:
        """Load a completed plan from PLAN.md."""
        if not plan_path:
            plan_path = self.project_root / "PLAN.md"

        if not plan_path.exists():
            print(f"❌ Plan not found at {plan_path}")
            return False

        print(f"📖 Loading plan from {plan_path}...")

        with open(plan_path) as f:
            plan_content = f.read()

        # Estimate Claude token usage for plan generation
        estimated_tokens = len(plan_content.split()) * 1.3
        self.state.record_token_usage("claude", int(estimated_tokens))

        # Parse tasks from the plan (simple parsing)
        tasks = self._parse_plan_tasks(plan_content)

        self.state.set("plan.path", str(plan_path))
        self.state.set("plan.tasks", tasks)
        self.state.set("sprint.status", "ready_for_execution")
        self.state.save()

        print(f"✅ Loaded {len(tasks)} tasks from plan")
        self._log_phase("Planning", "completed", output_file=str(plan_path))
        return True

    def phase_3_execute(self, task_id: Optional[str] = None, interactive: bool = False) -> bool:
        """Phase 3: Execution with Codex."""
        print("\n" + "=" * 80)
        print("PHASE 3: EXECUTION (Codex)")
        print("=" * 80)

        tasks = self.state.get("plan.tasks", [])
        if not tasks:
            print("❌ No tasks to execute. Load a plan first.")
            return False

        self.state.set("sprint.status", "executing")
        self.state.save()

        # Get context and plan for handoff packets
        context_path = self.state.get("context.repo_summary_path")
        context_summary = ""
        if context_path and Path(context_path).exists():
            with open(context_path) as f:
                context_summary = f.read()

        plan_path = self.state.get("plan.path")
        plan_content = ""
        if plan_path and Path(plan_path).exists():
            with open(plan_path) as f:
                plan_content = f.read()

        # Execute specific task or all pending tasks
        if task_id:
            task = self.state.get_task(task_id)
            if not task:
                print(f"❌ Task not found: {task_id}")
                return False
            return self._execute_task(task, context_summary, plan_content)
        else:
            # Execute all pending tasks
            pending = self.state.get_pending_tasks()
            print(f"📋 Found {len(pending)} pending tasks")

            for i, task in enumerate(pending, 1):
                print(f"\n--- Task {i}/{len(pending)} ---")
                success = self._execute_task(task, context_summary, plan_content)

                if not success and not interactive:
                    print("❌ Task failed. Stopping execution.")
                    return False

                if interactive and i < len(pending):
                    print("\nContinue to next task? (y/n): ", end="")
                    if input().lower() != 'y':
                        print("⏸️  Execution paused.")
                        self.state.set("sprint.status", "paused")
                        self.state.save()
                        return False

            print("\n✅ All tasks executed!")
            self.state.set("sprint.status", "completed")
            self.state.save()
            return True

    def _execute_task(self, task: dict, context_summary: str, plan_content: str) -> bool:
        """Execute a single task."""
        task_id = task.get("id", "unknown")
        print(f"\n🎯 Executing: {task.get('title', task_id)}")

        start_time = time.time()

        # Generate handoff packet
        packet = self.handoff_gen.generate_packet(task, context_summary, plan_content)

        # Update task status
        self.state.update_task(task_id, status="in_progress")
        self.state.record_agent_invocation("codex")
        self.state.save()

        # Invoke Codex
        response = self.codex.execute_task(task, packet)

        # Record timing
        duration = time.time() - start_time

        if response.success:
            print(f"✅ Task completed: {task_id}")
            print(f"⏱️  Duration: {duration:.1f}s")

            # Estimate token usage
            estimated_tokens = len(response.output.split()) * 1.3
            self.state.record_token_usage("codex", int(estimated_tokens))

            self.state.update_task(task_id, status="completed")
            self._log_task_completion(task, "completed", response.output)

            # Post success insight
            self.state.post_insight(
                "codex",
                f"Task {task_id} completed successfully in {duration:.1f}s"
            )
        else:
            print(f"❌ Task failed: {response.error}")
            print(f"⏱️  Failed after: {duration:.1f}s")

            self.state.update_task(task_id, status="failed")
            self._log_task_completion(task, "failed", error=response.error)

            # Post blocker to blackboard
            self.state.post_blocker(
                "codex",
                task_id,
                f"Task execution failed: {task.get('title', task_id)}",
                error=response.error
            )

            # Post message for architect attention
            self.state.post_message(
                "codex",
                "task_failure",
                f"Task {task_id} failed and may need re-planning",
                severity="error"
            )

        # Update overall task stats
        self.state.update_task_stats()
        self.state.save()
        return response.success

    def _parse_plan_tasks(self, plan_content: str) -> list:
        """Parse tasks from PLAN.md (simple parser)."""
        tasks = []
        lines = plan_content.split("\n")
        current_task = None

        for line in lines:
            # Look for task headers like "### Task 1:" or "## Task 1:"
            if line.startswith("### Task") or line.startswith("## Task"):
                if current_task:
                    tasks.append(current_task)

                # Extract task title
                title = line.split(":", 1)[1].strip() if ":" in line else line.strip("#").strip()
                task_num = len(tasks) + 1
                current_task = {
                    "id": f"task-{task_num:03d}",
                    "title": title,
                    "status": "pending",
                    "assigned_agent": "codex",
                    "description": "",
                    "dependencies": [],
                    "files_to_modify": [],
                    "acceptance_criteria": []
                }

            elif current_task:
                # Parse task details
                if line.startswith("- **ID:**"):
                    current_task["id"] = line.split(":", 1)[1].strip()
                elif line.startswith("- **Description:**"):
                    current_task["description"] = line.split(":", 1)[1].strip()
                elif "- [ ]" in line and "Acceptance Criteria" in plan_content[:plan_content.index(line)]:
                    criterion = line.replace("- [ ]", "").strip()
                    current_task["acceptance_criteria"].append(criterion)

        if current_task:
            tasks.append(current_task)

        return tasks

    def _create_session_log(self, sprint_id: str, objective: str):
        """Create initial session log file."""
        log_path = self.session_logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}_sprint-{sprint_id}.md"
        template = f"""---
date: {datetime.now().strftime('%Y-%m-%d')}
sprint_id: {sprint_id}
objective: {objective}
agents_used: []
status: in_progress
---

# Sprint: {sprint_id}

## Objective
{objective}

## Phase 1: Context (Gemini)
Status: pending

## Phase 2: Planning (Claude)
Status: pending

## Phase 3: Execution (Codex)
Status: pending

## Tasks
(Tasks will be added during planning phase)

## Notes
"""
        with open(log_path, "w") as f:
            f.write(template)

        self.state.set("session_log", str(log_path))
        self.state.save()

    def _log_phase(self, phase: str, status: str, output_file: str = None, error: str = None):
        """Update session log with phase completion."""
        log_path = Path(self.state.get("session_log"))
        if not log_path.exists():
            return

        with open(log_path) as f:
            content = f.read()

        # Update phase status
        phase_marker = f"## Phase"
        if phase in content:
            # Simple status update (would be more sophisticated in production)
            content = content.replace(
                f"{phase_marker}",
                f"{phase_marker} - {status.upper()}"
            )

        with open(log_path, "w") as f:
            f.write(content)

    def _log_task_completion(self, task: dict, status: str, output: str = None, error: str = None):
        """Log task completion to session log."""
        log_path = Path(self.state.get("session_log"))
        if not log_path.exists():
            return

        with open(log_path, "a") as f:
            f.write(f"\n### Task: {task.get('title')}\n")
            f.write(f"- **ID:** {task.get('id')}\n")
            f.write(f"- **Status:** {status}\n")
            if error:
                f.write(f"- **Error:** {error}\n")
