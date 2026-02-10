"""Claude Code agent adapter."""

import subprocess
from pathlib import Path
from typing import Any, Dict

from .base import AgentResponse, BaseAgent


class ClaudeAdapter(BaseAgent):
    """Adapter for Claude Code CLI."""

    def is_available(self) -> bool:
        """Check if Claude Code CLI is available."""
        try:
            result = subprocess.run(
                ["claude", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def invoke(self, prompt: str, context: Dict[str, Any]) -> AgentResponse:
        """Invoke Claude Code with a prompt."""
        if not self.is_available():
            print("\n⚠️  Claude Code CLI not available. Using manual fallback.")
            return self._prompt_for_result(prompt)

        # For Claude Code, we print the prompt for the user to paste into their session
        # since it's typically run in an interactive session
        print("\n" + "=" * 80)
        print("CLAUDE CODE PROMPT (paste into your Claude session)")
        print("=" * 80)
        print(prompt)
        print("=" * 80)

        return AgentResponse(
            success=True,
            output="Prompt provided for manual execution in Claude session",
            artifacts=[]
        )

    def plan(self, objective: str, context_summary: str) -> AgentResponse:
        """Generate a plan using Claude Code's architect mode."""
        prompt = self.load_prompt(
            "made_architect",
            objective=objective,
            context_summary=context_summary
        )
        return self.invoke(prompt, {"objective": objective})
