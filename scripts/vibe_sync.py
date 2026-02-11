#!/usr/bin/env python3
"""
Vibe-Sync Controller CLI
"""

import datetime
from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

app = typer.Typer(help="Vibe-Coding Session Manager")
console = Console()

PROJECT_ROOT = Path(__file__).parent.parent
SESSION_LOGS_DIR = PROJECT_ROOT / "session_logs"
CONTEXT_FILE = PROJECT_ROOT / ".agent" / "CONTEXT.md"


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
    if CONTEXT_FILE.exists():
        context_content = CONTEXT_FILE.read_text()
    else:
        context_content = "No CONTEXT.md found."

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

    # 3. Generate Pruned Context
    pruned_context = f"""
# Vibe-Coding Session Context

## Strategic Intent
{intent}

## Mode
{mode}

## Active Context (from CONTEXT.md)
{context_content[:1000]}... (truncated)

## Recent History
{chr(10).join(log_summaries)}
    """

    console.print(Markdown(pruned_context))
    console.print(Panel("Copy the above context to your AI agent.", style="green"))


@app.command()
def end(
    title: str = typer.Option(..., prompt="Session Title"),
):
    """
    Conclude the current session and generate a session log.
    """
    console.print(Panel.fit("Vibe-Sync: Ending Session", style="bold red"))

    today = datetime.datetime.now()
    date_str = today.strftime("%m-%d-%Y")  # Changed to match existing format MM-DD-YYYY
    date_dir = SESSION_LOGS_DIR / date_str
    date_dir.mkdir(parents=True, exist_ok=True)

    # Determine sequence number
    existing_logs = list(date_dir.glob("*.md"))
    seq = len(existing_logs) + 1

    filename = f"{seq} - {title}.md"
    filepath = date_dir / filename

    # Read Template
    template_path = SESSION_LOGS_DIR / "TEMPLATE.md"
    if template_path.exists():
        content = template_path.read_text()
    else:
        content = "# Session Log\n..."

    # Fill basic details
    content = content.replace("MM-DD-YYYY", date_str)
    content = content.replace("N - Title", f"{seq} - {title}")

    filepath.write_text(content)

    console.print(f"[green]Created session log:[/green] {filepath}")
    console.print(
        "[yellow]Please fill in the details in the generated log file.[/yellow]"
    )

    # Update CONTEXT.md (Mock implementation)
    # real implementation would parse and update "Recent" section
    console.print(
        "[dim]Remember to update .agent/CONTEXT.md with recent progress.[/dim]"
    )


@app.command()
def update():
    """
    Mid-session synchronization.
    """
    console.print("Updating context... (Placeholder)")
    # Logic to refresh maps, etc.


if __name__ == "__main__":
    app()
