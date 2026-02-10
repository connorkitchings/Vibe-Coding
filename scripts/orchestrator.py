"""
Vibe Orchestrator (The Commander)
=================================
Central CLI for managing the Vibe Coding project.
Instead of remembering many scripts, agents use this entry point.

Usage:
    python scripts/orchestrator.py [command] [args]

Commands:
    list        List available skills and scripts
    run         Run a specific script or skill
    audit       Run the context audit
    init-web    Run the web scaffolder (if listed)
"""

import subprocess
import sys
from pathlib import Path

# Map detailed commands to actual scripts
COMMANDS = {
    "audit": "uv run python .agents/skills/context-audit.py",
    "init-web": "uv run python .agents/skills/web_init.py",
    "test": "uv run pytest",
    "lint": "uv run ruff check .",
    "format": "uv run ruff format .",
    # MADE Orchestrator commands
    "vibe": "uv run python scripts/vibe/made.py",
    "vibe-status": "uv run python scripts/vibe/made.py status",
    "vibe-reset": "uv run python scripts/vibe/made.py reset",
    "vibe-context": "uv run python scripts/vibe/made.py context",
    "vibe-plan": "uv run python scripts/vibe/made.py plan",
    "vibe-exec": "uv run python scripts/vibe/made.py exec",
    "vibe-verify": "uv run python scripts/vibe/made.py verify",
    "vibe-sprint": "uv run python scripts/vibe/made.py sprint",
    "vibe-blackboard": "uv run python scripts/vibe/made.py blackboard",
    "vibe-metrics": "uv run python scripts/vibe/made.py metrics",
}


def list_commands():
    print("🤖 Vibe Orchestrator - Available Commands needed:")
    print("-" * 40)
    for cmd, target in COMMANDS.items():
        print(f"{cmd:<15} -> {target}")

    # Also scan scripts/ dir
    print("\nFound in scripts/:")
    script_dir = Path("scripts")
    if script_dir.exists():
        for f in script_dir.glob("*.py"):
            if f.name != "orchestrator.py":
                print(f"run {f.name:<11} -> python scripts/{f.name}")


def run_command(cmd_name):
    if cmd_name in COMMANDS:
        target = COMMANDS[cmd_name]
        print(f"🚀 Launching: {target}")
        subprocess.run(target, shell=True)
    else:
        # Check if it's a direct script run
        script_path = Path("scripts") / cmd_name
        if script_path.exists():
            print(f"🚀 Launching script: {script_path}")
            subprocess.run(["uv", "run", "python", str(script_path)])
        else:
            print(f"❌ Unknown command: {cmd_name}")
            list_commands()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        list_commands()
        sys.exit(0)

    mode = sys.argv[1]

    if mode == "list":
        list_commands()
    elif mode == "run" and len(sys.argv) > 2:
        run_command(sys.argv[2])
    elif mode in COMMANDS:
        run_command(mode)
    else:
        list_commands()
