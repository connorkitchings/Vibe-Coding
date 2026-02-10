"""Handoff packet generation for MADE workflows."""

from pathlib import Path
from typing import Any, Dict, List


class HandoffGenerator:
    """Generates handoff packets for task execution."""

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def generate_packet(
        self,
        task: Dict[str, Any],
        context_summary: str,
        plan_content: str
    ) -> str:
        """Generate a handoff packet for a specific task."""
        packet_parts = [
            "# Handoff Packet",
            "",
            "## Task Context",
            f"**Task ID:** {task.get('id', 'unknown')}",
            f"**Title:** {task.get('title', 'untitled')}",
            f"**Status:** {task.get('status', 'pending')}",
            "",
            "## Task Description",
            task.get("description", "No description provided."),
            "",
        ]

        # Add dependencies if present
        dependencies = task.get("dependencies", [])
        if dependencies:
            packet_parts.extend([
                "## Dependencies",
                "The following tasks must be completed before this one:",
                ""
            ])
            for dep_id in dependencies:
                packet_parts.append(f"- {dep_id}")
            packet_parts.append("")

        # Add files to modify
        files = task.get("files_to_modify", [])
        if files:
            packet_parts.extend([
                "## Files to Modify",
                ""
            ])
            for file_path in files:
                packet_parts.append(f"- `{file_path}`")
            packet_parts.append("")

        # Add acceptance criteria
        criteria = task.get("acceptance_criteria", [])
        if criteria:
            packet_parts.extend([
                "## Acceptance Criteria",
                ""
            ])
            for criterion in criteria:
                packet_parts.append(f"- [ ] {criterion}")
            packet_parts.append("")

        # Add relevant context
        packet_parts.extend([
            "## Repository Context (Summary)",
            "",
            context_summary[:2000] if context_summary else "No context summary available.",
            "",
            "## Full Plan Reference",
            "",
            "For complete context, see the full plan:",
            "```markdown",
            plan_content[:3000] if plan_content else "No plan available.",
            "```",
            "",
            "---",
            "",
            "Execute this task following the guidelines in the MADE Executor prompt.",
        ])

        return "\n".join(packet_parts)

    def generate_batch_packets(
        self,
        tasks: List[Dict[str, Any]],
        context_summary: str,
        plan_content: str
    ) -> Dict[str, str]:
        """Generate handoff packets for multiple tasks."""
        packets = {}
        for task in tasks:
            task_id = task.get("id", f"task-{len(packets)}")
            packets[task_id] = self.generate_packet(task, context_summary, plan_content)
        return packets

    def save_packet(self, task_id: str, packet: str, output_dir: Path) -> Path:
        """Save a handoff packet to disk."""
        output_dir.mkdir(parents=True, exist_ok=True)
        packet_path = output_dir / f"{task_id}_handoff.md"

        with open(packet_path, "w") as f:
            f.write(packet)

        return packet_path
