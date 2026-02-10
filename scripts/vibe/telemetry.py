"""Telemetry and observability for MADE orchestrator."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .state import VibeState


class TelemetryTracker:
    """Tracks and reports sprint efficiency metrics."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.telemetry_dir = project_root / "session_logs" / "telemetry"
        self.telemetry_dir.mkdir(parents=True, exist_ok=True)

    def save_sprint_report(self, state: VibeState) -> Path:
        """Save a comprehensive sprint efficiency report."""
        sprint_id = state.get("sprint.id")
        if not sprint_id:
            return None

        report = self._generate_report(state)
        report_path = self.telemetry_dir / f"{sprint_id}_telemetry.json"

        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        return report_path

    def _generate_report(self, state: VibeState) -> Dict[str, Any]:
        """Generate telemetry report from state."""
        metrics = state.get_sprint_metrics()

        return {
            "sprint_id": state.get("sprint.id"),
            "objective": state.get("sprint.objective"),
            "status": state.get("sprint.status"),
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "blackboard": {
                "messages": len(state.get("blackboard.messages", [])),
                "blockers": len(state.get("blackboard.blockers", [])),
                "unresolved_blockers": len(state.get_unresolved_blockers()),
                "insights": len(state.get("blackboard.insights", [])),
                "questions": len(state.get("blackboard.questions", [])),
                "unanswered_questions": len(state.get_unanswered_questions())
            },
            "efficiency": self._calculate_efficiency(state, metrics)
        }

    def _calculate_efficiency(self, state: VibeState, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate efficiency metrics."""
        total_tokens = metrics.get("total_tokens", 0)
        task_stats = metrics.get("task_stats", {})
        completed = task_stats.get("completed", 0)

        # Cost per task (assuming avg cost per 1M tokens)
        avg_cost_per_million = 2.0  # Rough estimate in USD
        total_cost = (total_tokens / 1_000_000) * avg_cost_per_million
        cost_per_task = total_cost / completed if completed > 0 else 0

        # Tokens per task
        tokens_per_task = total_tokens / completed if completed > 0 else 0

        # Agent efficiency (completed tasks per invocation)
        agent_invocations = metrics.get("agent_invocations", {})
        codex_invocations = agent_invocations.get("codex", 1)
        tasks_per_codex_run = completed / codex_invocations if codex_invocations > 0 else 0

        return {
            "total_cost_usd": round(total_cost, 2),
            "cost_per_task": round(cost_per_task, 2),
            "tokens_per_task": round(tokens_per_task, 0),
            "tasks_per_codex_run": round(tasks_per_codex_run, 2),
            "success_rate": metrics.get("success_rate", 0)
        }

    def generate_markdown_report(self, state: VibeState) -> str:
        """Generate a markdown efficiency report."""
        report = self._generate_report(state)
        metrics = report["metrics"]
        efficiency = report["efficiency"]
        blackboard = report["blackboard"]

        lines = [
            f"# Sprint Efficiency Report",
            f"",
            f"**Sprint ID:** {report['sprint_id']}",
            f"**Objective:** {report['objective']}",
            f"**Status:** {report['status']}",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"",
            f"## Token Usage",
            f"",
            f"| Agent | Tokens | Invocations | Tokens/Invocation |",
            f"|-------|--------|-------------|-------------------|",
        ]

        token_usage = metrics["token_usage"]
        invocations = metrics["agent_invocations"]
        for agent in ["gemini", "claude", "codex"]:
            tokens = token_usage.get(agent, 0)
            agent_invokes = invocations.get(agent, 0)
            tokens_per = tokens / agent_invokes if agent_invokes > 0 else 0
            lines.append(f"| {agent.title()} | {tokens:,} | {agent_invokes} | {tokens_per:,.0f} |")

        lines.extend([
            f"| **Total** | **{metrics['total_tokens']:,}** | - | - |",
            f"",
            f"## Task Statistics",
            f""
        ])

        task_stats = metrics["task_stats"]
        lines.extend([
            f"- **Total Tasks:** {task_stats.get('total', 0)}",
            f"- **Completed:** {task_stats.get('completed', 0)}",
            f"- **Failed:** {task_stats.get('failed', 0)}",
            f"- **In Progress:** {task_stats.get('in_progress', 0)}",
            f"- **Pending:** {task_stats.get('pending', 0)}",
            f"- **Success Rate:** {efficiency['success_rate']:.1f}%",
            f"",
            f"## Efficiency Metrics",
            f""
        ])

        lines.extend([
            f"- **Estimated Cost:** ${efficiency['total_cost_usd']:.2f}",
            f"- **Cost per Task:** ${efficiency['cost_per_task']:.2f}",
            f"- **Tokens per Task:** {efficiency['tokens_per_task']:,.0f}",
            f"- **Tasks per Codex Run:** {efficiency['tasks_per_codex_run']:.2f}",
            f"",
            f"## Phase Timing",
            f""
        ])

        phase_times = metrics.get("phase_times", {})
        if phase_times:
            for phase, duration in phase_times.items():
                minutes = int(duration // 60)
                seconds = int(duration % 60)
                lines.append(f"- **{phase.title()}:** {minutes}m {seconds}s")
        else:
            lines.append("_No phase timing data available_")

        lines.extend([
            f"",
            f"## Blackboard Activity",
            f"",
            f"- **Messages:** {blackboard['messages']}",
            f"- **Blockers:** {blackboard['blockers']} ({blackboard['unresolved_blockers']} unresolved)",
            f"- **Insights:** {blackboard['insights']}",
            f"- **Questions:** {blackboard['questions']} ({blackboard['unanswered_questions']} unanswered)",
            f""
        ])

        # Add unresolved blockers section
        unresolved = state.get_unresolved_blockers()
        if unresolved:
            lines.extend([
                f"",
                f"## ⚠️ Unresolved Blockers",
                f""
            ])
            for i, blocker in enumerate(unresolved, 1):
                lines.append(f"{i}. **[{blocker['agent'].upper()}]** {blocker['description']}")
                if blocker.get('error'):
                    lines.append(f"   - Error: `{blocker['error']}`")
                lines.append(f"   - Task: {blocker['task_id']}")
                lines.append("")

        # Add unanswered questions
        unanswered = state.get_unanswered_questions()
        if unanswered:
            lines.extend([
                f"## ❓ Unanswered Questions",
                f""
            ])
            for i, question in enumerate(unanswered, 1):
                lines.append(f"{i}. **[{question['agent'].upper()}]** {question['question']}")
                if question.get('context'):
                    lines.append(f"   - Context: {question['context']}")
                lines.append("")

        return "\n".join(lines)

    def compare_sprints(self, sprint_ids: List[str]) -> Dict[str, Any]:
        """Compare efficiency across multiple sprints."""
        comparisons = []

        for sprint_id in sprint_ids:
            report_path = self.telemetry_dir / f"{sprint_id}_telemetry.json"
            if report_path.exists():
                with open(report_path) as f:
                    comparisons.append(json.load(f))

        if not comparisons:
            return {}

        return {
            "sprints": comparisons,
            "averages": self._calculate_averages(comparisons)
        }

    def _calculate_averages(self, reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate average metrics across sprints."""
        if not reports:
            return {}

        total_cost = sum(r["efficiency"]["total_cost_usd"] for r in reports)
        total_tokens = sum(r["metrics"]["total_tokens"] for r in reports)
        avg_success_rate = sum(r["efficiency"]["success_rate"] for r in reports) / len(reports)

        return {
            "avg_cost_per_sprint": round(total_cost / len(reports), 2),
            "avg_tokens_per_sprint": round(total_tokens / len(reports), 0),
            "avg_success_rate": round(avg_success_rate, 1),
            "total_sprints": len(reports)
        }
