#!/usr/bin/env python3
"""
Vibe-Sync Controller CLI
"""

import datetime
import re
import subprocess
from pathlib import Path

import pyperclip
import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(help="Vibe-Coding Session Manager")
console = Console()

PROJECT_ROOT = Path(__file__).parent.parent
SESSION_LOGS_DIR = PROJECT_ROOT / "session_logs"
CONTEXT_FILE = PROJECT_ROOT / ".agent" / "CONTEXT.md"


def get_context_section(content: str, section_name: str) -> str:
    """Extract a specific markdown section from CONTEXT.md."""
    lines = content.splitlines()
    section_content = []
    in_section = False

    # Normalize section name for matching (e.g., "## Recent" -> "Recent")
    target_header = f"## {section_name}"

    for line in lines:
        if line.strip().startswith("## "):
            if line.strip().startswith(target_header):
                in_section = True
                continue
            elif in_section:
                break  # Reached next section

        if in_section:
            section_content.append(line)

    return "\n".join(section_content).strip()


def get_last_handoff(logs) -> str:
    """Extract handoff notes from the most recent session log."""
    if not logs:
        return "No previous logs found."

    last_log = logs[0]["path"].read_text()

    # Look for "## Handoff Notes"
    # Simple heuristic parsing
    if "## Handoff Notes" in last_log:
        parts = last_log.split("## Handoff Notes")
        if len(parts) > 1:
            handoff_section = parts[1].split("## ")[0].strip()
            return handoff_section

    return "No handoff notes found in last log."


class ContextSynthesizer:
    def __init__(self, context_path: Path, logs_dir: Path):
        self.context_path = context_path
        self.logs_dir = logs_dir
        self.context_content = (
            self.context_path.read_text() if self.context_path.exists() else ""
        )

    def get_latest_log(self):
        """Retrieve the most recent session log."""
        if not self.logs_dir.exists():
            return None

        all_logs = []
        for date_dir in self.logs_dir.iterdir():
            if date_dir.is_dir() and date_dir.name != "telemetry":
                try:
                    date_obj = datetime.datetime.strptime(
                        date_dir.name, "%m-%d-%Y"
                    ).date()
                    for log_file in date_dir.glob("*.md"):
                        all_logs.append(
                            {"path": log_file, "date": date_obj, "name": log_file.name}
                        )
                except ValueError:
                    continue

        all_logs.sort(key=lambda x: (x["date"], x["name"]), reverse=True)
        return all_logs[0] if all_logs else None

    def extract_section(self, content: str, header: str) -> str:
        """Extracts content under a specific markdown header."""
        lines = content.splitlines()
        section_content = []
        in_section = False
        target_header = f"## {header}"

        for line in lines:
            if line.strip().startswith("## "):
                if line.strip().startswith(target_header):
                    in_section = True
                    continue
                elif in_section:
                    break

            if in_section:
                section_content.append(line)

        return "\n".join(section_content).strip()

    def generate_prime_directive(self, start_mode: str) -> str:
        """Assembles the High-Density Handoff string."""
        snapshot = (
            self.extract_section(self.context_content, "Project Snapshot")
            or "No snapshot available."
        )

        last_log = self.get_latest_log()
        if last_log:
            log_content = last_log["path"].read_text()
            momentum = (
                self.extract_section(log_content, "Work Completed")
                or "No recent work recorded."
            )
            immediate_next = (
                self.extract_section(log_content, "Next Steps")
                or "No next steps defined."
            )
        else:
            momentum = "No previous session logs found."
            immediate_next = "Initialize project structure."

        # Skeptical Researcher: Check for stale context
        # (Simple heuristic implementation for now)
        if "No next steps defined" in immediate_next:
            immediate_next = (
                "REVIEW REQUIRED: Last session ended without clear next steps."
            )

        directive = f"""
VIBE-SYNC HANDOFF
---
MODE: {start_mode}
SNAPSHOT: {snapshot.splitlines()[0] if snapshot else "N/A"}
MOMENTUM: {momentum.splitlines()[0] if momentum else "N/A"}... (see log for details)
IMMEDIATE_NEXT:
{immediate_next}
---
"""
        return directive.strip()

    def copy_to_clipboard(self, text: str):
        try:
            pyperclip.copy(text)
            return True
        except Exception:
            return False


def get_session_logs():
    """Retrieve all session logs, sorted by date and sequence."""
    logs = []
    if not SESSION_LOGS_DIR.exists():
        return logs

    for date_dir in SESSION_LOGS_DIR.iterdir():
        if date_dir.is_dir() and date_dir.name != "telemetry":
            # Ignore telemetry if it exists
            try:
                date_obj = datetime.datetime.strptime(date_dir.name, "%m-%d-%Y").date()
            except ValueError:
                continue

            for log_file in date_dir.glob("*.md"):
                logs.append({"path": log_file, "date": date_obj, "name": log_file.name})

    # Sort by date desc, then by name desc (assuming N - Title format)
    logs.sort(key=lambda x: (x["date"], x["name"]), reverse=True)
    return logs


@app.command()
def start(
    intent: str = typer.Option(..., prompt="What is the intent of this session?"),
    mode: str = typer.Option(
        "EXECUTION", prompt="Mode (PLANNING, EXECUTION, VERIFICATION)?"
    ),
):
    """
    Initialize a new development session.
    Generates a pruned context for the AI agent.
    """
    console.print(Panel.fit("Vibe-Sync: Initializing Session", style="bold blue"))

    # 1. Read Context
    if not CONTEXT_FILE.exists():
        console.print("[yellow]No CONTEXT.md found.[/yellow]")

    # 2. Get Recent Logs (Last 3)
    logs = get_session_logs()
    recent_logs = logs[:3]

    log_summaries = []
    for log in recent_logs:
        content = log["path"].read_text()
        # Extract TL;DR or first few lines
        lines = content.splitlines()
        summary = "\n".join(lines[:15]) + "\n..."  # Rough heuristic
        log_summaries.append(f"### {log['name']} ({log['name']})\n{summary}")

    # 3. Parse Context Sections
    # project_snapshot = get_context_section(context_content, "Project Snapshot")
    # critical_rules = get_context_section(context_content, "Critical Rules")

    # 4. Generate Prime Directive via Synthesizer
    synthesizer = ContextSynthesizer(CONTEXT_FILE, SESSION_LOGS_DIR)
    prime_directive = synthesizer.generate_prime_directive(mode)

    # 5. Output and Copy
    console.print(Panel(prime_directive, title="Prime Directive", style="bold green"))

    if synthesizer.copy_to_clipboard(prime_directive):
        console.print("[bold green]✓ Copied to clipboard![/bold green]")
    else:
        console.print("[yellow]Clipboard copy failed. Please copy manually.[/yellow]")


def get_git_changes():
    """Get list of changed files using git."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True
        )
        if result.returncode != 0:
            return []

        changes = []
        for line in result.stdout.splitlines():
            if line.strip():
                changes.append(line.strip())
        return changes
    except Exception:
        return []


@app.command()
def end(
    title: str = typer.Option(..., prompt="Session Title"),
):
    """
    Conclude the current session and generate a session log.
    """
    console.print(Panel.fit("Vibe-Sync: Ending Session", style="bold red"))

    # 1. Gather Intelligence
    changes = get_git_changes()

    # 2. Prompt for Details
    goal = typer.prompt("Session Goal (TL;DR)")
    accomplished = typer.prompt("Accomplished")
    blockers = typer.prompt("Blockers", default="None")
    next_steps = typer.prompt("Next Steps")

    # 3. Create Log File
    today = datetime.datetime.now()
    date_str = today.strftime("%m-%d-%Y")
    date_dir = SESSION_LOGS_DIR / date_str
    date_dir.mkdir(parents=True, exist_ok=True)

    existing_logs = list(date_dir.glob("*.md"))
    seq = len(existing_logs) + 1
    filename = f"{seq} - {title}.md"
    filepath = date_dir / filename

    # 4. Generate Content
    if changes:
        files_list = "\n".join([f"- `{c.split()[-1]}` - Modified" for c in changes])
    else:
        files_list = "- No file changes detected via git."

    content = f"""# Session Log — {date_str} ({seq} - {title})

## TL;DR
- **Goal**: {goal}
- **Accomplished**: {accomplished}
- **Blockers**: {blockers}
- **Next**: {next_steps}

## Work Completed

### Files Modified
{files_list}

### Commands Run
(Auto-generated placeholder)

## Handoff Notes
- **For next session**: {next_steps}
"""

    filepath.write_text(content)

    console.print(f"[green]Created session log:[/green] {filepath}")
    console.print(
        "[dim]Remember to update .agent/CONTEXT.md with recent progress.[/dim]"
    )


@app.command()
def update(
    recent: str = typer.Option(
        ..., prompt="What is the recent activity/accomplishment?"
    ),
):
    """
    Update the 'Recent' status in CONTEXT.md.
    """
    if not CONTEXT_FILE.exists():
        console.print("[red]CONTEXT.md not found![/red]")
        return

    content = CONTEXT_FILE.read_text()

    # Regex to find the Recent line
    # Matches: - **Recent**: ...
    pattern = r"(- \*\*Recent\*\*: ).*"

    if re.search(pattern, content):
        new_content = re.sub(pattern, f"\\1{recent}", content)
        CONTEXT_FILE.write_text(new_content)
        console.print(f"[green]Updated 'Recent' in CONTEXT.md:[/green] {recent}")
    else:
        console.print("[yellow]Could not find 'Recent' line in CONTEXT.md[/yellow]")

    # Also touch the file to ensure timestamp update if needed
    CONTEXT_FILE.touch()


if __name__ == "__main__":
    app()
