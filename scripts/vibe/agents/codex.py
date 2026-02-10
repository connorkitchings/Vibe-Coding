"""Codex CLI agent adapter."""

import subprocess
from pathlib import Path
from typing import Any, Dict

from .base import AgentResponse, BaseAgent


class CodexAdapter(BaseAgent):
    """Adapter for Codex CLI."""

    def is_available(self) -> bool:
        """Check if Codex CLI is available."""
        try:
            result = subprocess.run(
                ["codex", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def invoke(self, prompt: str, context: Dict[str, Any]) -> AgentResponse:
        """Invoke Codex CLI with a prompt."""
        if not self.is_available():
            print("\n⚠️  Codex CLI not available. Using manual fallback.")
            return self._prompt_for_result(prompt)

        try:
            print("\n⚙️  Invoking Codex CLI for execution...")
            result = subprocess.run(
                ["codex", "--prompt", prompt],
                capture_output=True,
                text=True,
                timeout=600,  # 10 minute timeout for execution
                cwd=self.project_root
            )

            if result.returncode != 0:
                return AgentResponse(
                    success=False,
                    output=result.stdout,
                    error=result.stderr
                )

            return AgentResponse(
                success=True,
                output=result.stdout,
                artifacts=[]
            )

        except subprocess.TimeoutExpired:
            return AgentResponse(
                success=False,
                output="",
                error="Codex CLI timed out after 10 minutes"
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                output="",
                error=f"Failed to invoke Codex CLI: {str(e)}"
            )

    def execute_task(self, task: Dict[str, Any], handoff_packet: str) -> AgentResponse:
        """Execute a specific task with handoff context."""
        prompt = self.load_prompt(
            "made_executor",
            task_title=task.get("title", ""),
            task_description=task.get("description", ""),
            handoff_packet=handoff_packet
        )
        return self.invoke(prompt, {"task": task})
