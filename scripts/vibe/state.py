"""State management for MADE orchestrator."""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class VibeState:
    """Manages .vibe_state.json at project root."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.state_file = project_root / ".vibe_state.json"
        self._state: Optional[Dict[str, Any]] = None

    def load(self) -> Dict[str, Any]:
        """Load state from disk."""
        if not self.state_file.exists():
            self._state = self._default_state()
            return self._state

        try:
            with open(self.state_file) as f:
                self._state = json.load(f)
            return self._state
        except json.JSONDecodeError:
            # Backup corrupted file
            backup_path = self.state_file.with_suffix(".json.backup")
            shutil.copy(self.state_file, backup_path)
            self._state = self._default_state()
            return self._state

    def save(self) -> None:
        """Save state to disk with backup."""
        if self._state is None:
            return

        # Backup existing state
        if self.state_file.exists():
            backup_path = self.state_file.with_suffix(".json.bak")
            shutil.copy(self.state_file, backup_path)

        with open(self.state_file, "w") as f:
            json.dump(self._state, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get state value by dot-notation key (e.g., 'sprint.status')."""
        if self._state is None:
            self.load()

        keys = key.split(".")
        value = self._state
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        """Set state value by dot-notation key."""
        if self._state is None:
            self.load()

        keys = key.split(".")
        target = self._state
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value

    def update_task(self, task_id: str, **updates) -> None:
        """Update a specific task in the plan."""
        tasks = self.get("plan.tasks", [])
        for task in tasks:
            if task.get("id") == task_id:
                task.update(updates)
                break
        self.set("plan.tasks", tasks)

    def add_task(self, task: Dict[str, Any]) -> None:
        """Add a new task to the plan."""
        tasks = self.get("plan.tasks", [])
        tasks.append(task)
        self.set("plan.tasks", tasks)

    def reset(self) -> None:
        """Reset to default state."""
        self._state = self._default_state()
        self.save()

    def start_sprint(self, objective: str) -> str:
        """Initialize a new sprint."""
        sprint_id = f"sprint-{datetime.now().strftime('%Y-%m-%d-%H%M%S')}"
        session_log = f"session_logs/{datetime.now().strftime('%Y-%m-%d')}_sprint-{sprint_id}.md"

        self.set("sprint.id", sprint_id)
        self.set("sprint.status", "planning")
        self.set("sprint.objective", objective)
        self.set("session_log", session_log)
        self.save()

        return sprint_id

    def _default_state(self) -> Dict[str, Any]:
        """Return default state structure."""
        return {
            "version": "1.0",
            "sprint": {
                "id": None,
                "status": None,
                "objective": None
            },
            "context": {
                "repo_summary_path": None,
                "token_budget_used": 0
            },
            "plan": {
                "path": None,
                "tasks": []
            },
            "session_log": None,
            "blackboard": {
                "messages": [],
                "blockers": [],
                "insights": [],
                "questions": []
            },
            "metrics": {
                "token_usage": {
                    "gemini": 0,
                    "claude": 0,
                    "codex": 0
                },
                "task_stats": {
                    "total": 0,
                    "completed": 0,
                    "failed": 0
                },
                "phase_times": {},
                "agent_invocations": {
                    "gemini": 0,
                    "claude": 0,
                    "codex": 0
                }
            }
        }

    @property
    def has_active_sprint(self) -> bool:
        """Check if there's an active sprint."""
        status = self.get("sprint.status")
        return status in ["planning", "executing", "paused"]

    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get all pending tasks."""
        tasks = self.get("plan.tasks", [])
        return [t for t in tasks if t.get("status") == "pending"]

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID."""
        tasks = self.get("plan.tasks", [])
        for task in tasks:
            if task.get("id") == task_id:
                return task
        return None

    # Blackboard methods
    def post_message(self, agent: str, message_type: str, content: str, severity: str = "info") -> None:
        """Post a message to the blackboard for other agents to see."""
        messages = self.get("blackboard.messages", [])
        messages.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "type": message_type,
            "content": content,
            "severity": severity
        })
        self.set("blackboard.messages", messages)
        self.save()

    def post_blocker(self, agent: str, task_id: str, description: str, error: str = None) -> None:
        """Post a blocker that needs attention from the architect."""
        blockers = self.get("blackboard.blockers", [])
        blockers.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "task_id": task_id,
            "description": description,
            "error": error,
            "resolved": False
        })
        self.set("blackboard.blockers", blockers)
        self.save()

    def post_insight(self, agent: str, insight: str) -> None:
        """Post an insight or observation for other agents."""
        insights = self.get("blackboard.insights", [])
        insights.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "insight": insight
        })
        self.set("blackboard.insights", insights)
        self.save()

    def post_question(self, agent: str, question: str, context: str = None) -> None:
        """Post a question for the architect or librarian to address."""
        questions = self.get("blackboard.questions", [])
        questions.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "question": question,
            "context": context,
            "answered": False
        })
        self.set("blackboard.questions", questions)
        self.save()

    def get_unresolved_blockers(self) -> List[Dict[str, Any]]:
        """Get all unresolved blockers."""
        blockers = self.get("blackboard.blockers", [])
        return [b for b in blockers if not b.get("resolved", False)]

    def get_unanswered_questions(self) -> List[Dict[str, Any]]:
        """Get all unanswered questions."""
        questions = self.get("blackboard.questions", [])
        return [q for q in questions if not q.get("answered", False)]

    def resolve_blocker(self, blocker_index: int, resolution: str) -> None:
        """Mark a blocker as resolved."""
        blockers = self.get("blackboard.blockers", [])
        if 0 <= blocker_index < len(blockers):
            blockers[blocker_index]["resolved"] = True
            blockers[blocker_index]["resolution"] = resolution
            blockers[blocker_index]["resolved_at"] = datetime.now().isoformat()
            self.set("blackboard.blockers", blockers)
            self.save()

    # Metrics methods
    def record_token_usage(self, agent: str, tokens: int) -> None:
        """Record token usage for an agent."""
        current = self.get(f"metrics.token_usage.{agent}", 0)
        self.set(f"metrics.token_usage.{agent}", current + tokens)
        self.save()

    def record_agent_invocation(self, agent: str) -> None:
        """Record an agent invocation."""
        current = self.get(f"metrics.agent_invocations.{agent}", 0)
        self.set(f"metrics.agent_invocations.{agent}", current + 1)
        self.save()

    def record_phase_time(self, phase: str, duration_seconds: float) -> None:
        """Record time taken for a phase."""
        times = self.get("metrics.phase_times", {})
        times[phase] = duration_seconds
        self.set("metrics.phase_times", times)
        self.save()

    def update_task_stats(self) -> None:
        """Update task statistics from current tasks."""
        tasks = self.get("plan.tasks", [])
        stats = {
            "total": len(tasks),
            "completed": len([t for t in tasks if t.get("status") == "completed"]),
            "failed": len([t for t in tasks if t.get("status") == "failed"]),
            "in_progress": len([t for t in tasks if t.get("status") == "in_progress"]),
            "pending": len([t for t in tasks if t.get("status") == "pending"])
        }
        self.set("metrics.task_stats", stats)
        self.save()

    def get_sprint_metrics(self) -> Dict[str, Any]:
        """Get all sprint metrics."""
        return {
            "token_usage": self.get("metrics.token_usage", {}),
            "task_stats": self.get("metrics.task_stats", {}),
            "phase_times": self.get("metrics.phase_times", {}),
            "agent_invocations": self.get("metrics.agent_invocations", {}),
            "total_tokens": sum(self.get("metrics.token_usage", {}).values()),
            "success_rate": self._calculate_success_rate()
        }

    def _calculate_success_rate(self) -> float:
        """Calculate task success rate."""
        stats = self.get("metrics.task_stats", {})
        total = stats.get("total", 0)
        if total == 0:
            return 0.0
        completed = stats.get("completed", 0)
        return (completed / total) * 100
