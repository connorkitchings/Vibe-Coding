"""Gemini CLI agent adapter."""

import subprocess
from pathlib import Path
from typing import Any, Dict

from .base import AgentResponse, BaseAgent


class GeminiAdapter(BaseAgent):
    """Adapter for Gemini CLI."""

    def is_available(self) -> bool:
        """Check if Gemini CLI is available."""
        try:
            result = subprocess.run(
                ["gemini", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def invoke(self, prompt: str, context: Dict[str, Any]) -> AgentResponse:
        """Invoke Gemini CLI with a prompt."""
        if not self.is_available():
            print("\n⚠️  Gemini CLI not available. Using manual fallback.")
            return self._prompt_for_result(prompt)

        try:
            # Auto-invoke Gemini CLI
            print("\n🔍 Invoking Gemini CLI for context analysis...")
            result = subprocess.run(
                ["gemini", "--prompt", prompt],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout for large context
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
                error="Gemini CLI timed out after 5 minutes"
            )
        except Exception as e:
            return AgentResponse(
                success=False,
                output="",
                error=f"Failed to invoke Gemini CLI: {str(e)}"
            )

    def analyze_context(self, objective: str) -> AgentResponse:
        """Analyze repository context for a sprint objective."""
        prompt = self.load_prompt(
            "made_librarian",
            objective=objective,
            repo_path=str(self.project_root)
        )
        return self.invoke(prompt, {"objective": objective})
