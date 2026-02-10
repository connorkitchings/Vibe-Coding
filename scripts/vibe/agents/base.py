"""Base agent protocol for MADE orchestrator."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class AgentResponse:
    """Response from an agent invocation."""
    success: bool
    output: str
    artifacts: list[Path] = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.artifacts is None:
            self.artifacts = []


class BaseAgent(ABC):
    """Base protocol for agent adapters."""

    def __init__(self, project_root: Path):
        self.project_root = project_root

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the agent CLI is available."""
        pass

    @abstractmethod
    def invoke(self, prompt: str, context: Dict[str, Any]) -> AgentResponse:
        """Invoke the agent with a prompt and context."""
        pass

    def _prompt_for_result(self, prompt: str) -> AgentResponse:
        """Fallback: print prompt and ask user to paste result."""
        print("\n" + "=" * 80)
        print(f"MANUAL INVOCATION REQUIRED")
        print("=" * 80)
        print(prompt)
        print("=" * 80)
        print("\nExecute the above prompt manually and paste the result.")
        print("Press Enter when done (or 'skip' to skip this step):")

        user_input = input().strip()
        if user_input.lower() == "skip":
            return AgentResponse(
                success=False,
                output="",
                error="User skipped manual invocation"
            )

        return AgentResponse(
            success=True,
            output=user_input
        )

    def get_prompt_file(self, prompt_name: str) -> Optional[Path]:
        """Get path to prompt file in .agents/prompts/."""
        prompt_path = self.project_root / ".agents" / "prompts" / f"{prompt_name}.md"
        return prompt_path if prompt_path.exists() else None

    def load_prompt(self, prompt_name: str, **variables) -> str:
        """Load and format a prompt template."""
        prompt_path = self.get_prompt_file(prompt_name)
        if not prompt_path:
            return f"# {prompt_name.replace('_', ' ').title()}\n\n[Prompt template not found]"

        with open(prompt_path) as f:
            template = f.read()

        # Simple variable substitution
        for key, value in variables.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))

        return template
