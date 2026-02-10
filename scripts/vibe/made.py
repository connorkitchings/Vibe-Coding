#!/usr/bin/env python3
"""MADE (Multi-Agent Developer Environment) CLI."""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

# Handle both direct execution and module import
if __name__ == "__main__" or __package__ is None:
    # Add parent directory to path for direct execution
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from scripts.vibe.state import VibeState
    from scripts.vibe.workflows.sprint import VibeSprint
else:
    from .state import VibeState
    from .workflows.sprint import VibeSprint

app = typer.Typer(
    name="vibe",
    help="MADE (Multi-Agent Developer Environment) Orchestrator",
    no_args_is_help=True
)
console = Console()


def get_project_root() -> Path:
    """Get project root directory."""
    return Path.cwd()


@app.command()
def status():
    """Show current sprint status."""
    state = VibeState(get_project_root())
    state.load()

    if not state.has_active_sprint:
        console.print("\n[yellow]No active sprint[/yellow]")
        console.print("Start a new sprint with: [cyan]vibe sprint start[/cyan]\n")
        return

    sprint_id = state.get("sprint.id")
    sprint_status = state.get("sprint.status")
    objective = state.get("sprint.objective")

    console.print(f"\n[bold]Sprint:[/bold] {sprint_id}")
    console.print(f"[bold]Status:[/bold] {sprint_status}")
    console.print(f"[bold]Objective:[/bold] {objective}\n")

    # Show tasks
    tasks = state.get("plan.tasks", [])
    if tasks:
        table = Table(title="Tasks")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="white")
        table.add_column("Status", style="green")
        table.add_column("Agent", style="blue")

        for task in tasks:
            status_color = {
                "pending": "yellow",
                "in_progress": "blue",
                "completed": "green",
                "failed": "red"
            }.get(task.get("status", "pending"), "white")

            table.add_row(
                task.get("id", ""),
                task.get("title", ""),
                f"[{status_color}]{task.get('status', 'pending')}[/{status_color}]",
                task.get("assigned_agent", "")
            )

        console.print(table)
    else:
        console.print("[yellow]No tasks loaded yet[/yellow]")

    console.print()


@app.command()
def reset(
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation")
):
    """Reset sprint state."""
    if not force:
        confirm = typer.confirm("⚠️  This will reset all sprint state. Continue?")
        if not confirm:
            console.print("[yellow]Reset cancelled[/yellow]")
            return

    state = VibeState(get_project_root())
    state.reset()
    console.print("[green]✅ State reset successfully[/green]")


sprint_app = typer.Typer(help="Sprint workflow commands")
app.add_typer(sprint_app, name="sprint")


@sprint_app.command("start")
def sprint_start(objective: str = typer.Argument(..., help="Sprint objective")):
    """Start a new sprint."""
    sprint = VibeSprint(get_project_root())
    sprint_id = sprint.start(objective)
    console.print(f"\n[green]✅ Sprint started: {sprint_id}[/green]")
    console.print(f"[cyan]Next step: vibe context[/cyan]\n")


@sprint_app.command("full")
def sprint_full(
    objective: str = typer.Argument(..., help="Sprint objective"),
    interactive: bool = typer.Option(True, "--interactive/--auto", help="Interactive execution")
):
    """Run full sprint: context -> plan -> execute."""
    sprint = VibeSprint(get_project_root())

    # Start sprint
    sprint_id = sprint.start(objective)
    console.print(f"\n[green]✅ Sprint started: {sprint_id}[/green]\n")

    # Phase 1: Context
    if not sprint.phase_1_context():
        console.print("[red]❌ Context phase failed[/red]")
        return

    # Phase 2: Plan
    if not sprint.phase_2_plan():
        console.print("[red]❌ Planning phase failed[/red]")
        return

    # Wait for user to create plan
    console.print("\n[yellow]⏸️  Waiting for PLAN.md to be created...[/yellow]")
    input("Press Enter when PLAN.md is ready: ")

    if not sprint.load_plan():
        console.print("[red]❌ Failed to load plan[/red]")
        return

    # Phase 3: Execute
    if not sprint.phase_3_execute(interactive=interactive):
        console.print("[red]❌ Execution phase failed[/red]")
        return

    console.print("\n[green]✅ Sprint completed successfully![/green]")


@app.command()
def context():
    """Run Phase 1: Context analysis with Gemini."""
    sprint = VibeSprint(get_project_root())
    if sprint.phase_1_context():
        console.print("\n[cyan]Next step: vibe plan[/cyan]\n")
    else:
        console.print("\n[red]Context phase failed[/red]\n")


@app.command()
def plan(
    load_file: Optional[Path] = typer.Option(None, "--load", "-l", help="Load existing PLAN.md")
):
    """Run Phase 2: Planning with Claude Code."""
    sprint = VibeSprint(get_project_root())

    if load_file:
        if sprint.load_plan(load_file):
            console.print("\n[cyan]Next step: vibe exec[/cyan]\n")
        else:
            console.print("\n[red]Failed to load plan[/red]\n")
    else:
        if sprint.phase_2_plan():
            console.print("\n[cyan]After creating PLAN.md, run: vibe plan --load PLAN.md[/cyan]\n")
        else:
            console.print("\n[red]Planning phase failed[/red]\n")


@app.command()
def exec(
    task_id: Optional[str] = typer.Option(None, "--task", "-t", help="Execute specific task"),
    interactive: bool = typer.Option(True, "--interactive/--auto", help="Interactive execution")
):
    """Run Phase 3: Execution with Codex."""
    sprint = VibeSprint(get_project_root())
    if sprint.phase_3_execute(task_id=task_id, interactive=interactive):
        console.print("\n[green]✅ Execution complete![/green]\n")
    else:
        console.print("\n[red]Execution failed[/red]\n")


@app.command()
def verify():
    """Run verification: Check implementation against plan (Phase 4)."""
    from .agents.claude import ClaudeAdapter

    state = VibeState(get_project_root())
    state.load()

    if not state.has_active_sprint:
        console.print("[yellow]No active sprint to verify[/yellow]")
        return

    # Get plan and recent changes
    plan_path = state.get("plan.path")
    if not plan_path or not Path(plan_path).exists():
        console.print("[yellow]No plan found to verify against[/yellow]")
        return

    with open(plan_path) as f:
        plan_content = f.read()

    console.print("\n[cyan]🔍 Running architectural verification...[/cyan]\n")

    # Generate verification prompt
    claude = ClaudeAdapter(get_project_root())
    verify_prompt = f"""# Architectural Verification

You are reviewing the implementation against the original plan.

## Original Plan
```markdown
{plan_content[:2000]}
```

## Your Task
Review the git diff and verify:
1. **Architectural Intent** - Does the implementation follow the planned architecture?
2. **Pattern Consistency** - Are existing patterns maintained?
3. **Scope Adherence** - Is the implementation within the planned scope?
4. **Technical Debt** - Any shortcuts taken that need addressing?

Run `git diff main` to see all changes, then provide:

### Verification Report
- [ ] Architectural intent maintained
- [ ] Patterns consistent
- [ ] Scope appropriate
- [ ] No critical technical debt

### Issues Found
[List any deviations or concerns]

### Recommendations
[Suggestions for improvement or follow-up tasks]
"""

    response = claude.invoke(verify_prompt, {})
    console.print("[green]✅ Verification prompt generated[/green]")
    console.print("\n[cyan]Review the changes and create a verification report[/cyan]\n")


@app.command()
def blackboard(
    show_type: str = typer.Option("all", "--type", "-t", help="Show: all, blockers, questions, insights, messages")
):
    """View blackboard communications between agents."""
    state = VibeState(get_project_root())
    state.load()

    console.print("\n[bold]📋 Agent Blackboard[/bold]\n")

    if show_type in ["all", "blockers"]:
        blockers = state.get("blackboard.blockers", [])
        if blockers:
            console.print("[bold red]⚠️  Blockers[/bold red]")
            for i, blocker in enumerate(blockers):
                status = "✓ Resolved" if blocker.get("resolved") else "⚠️  UNRESOLVED"
                console.print(f"\n{i+1}. [{blocker['agent'].upper()}] {status}")
                console.print(f"   Task: {blocker['task_id']}")
                console.print(f"   Description: {blocker['description']}")
                if blocker.get('error'):
                    console.print(f"   Error: {blocker['error'][:100]}...")
                console.print(f"   Time: {blocker['timestamp']}")
            console.print()

    if show_type in ["all", "questions"]:
        questions = state.get("blackboard.questions", [])
        if questions:
            console.print("[bold yellow]❓ Questions[/bold yellow]")
            for i, q in enumerate(questions):
                status = "✓ Answered" if q.get("answered") else "❓ UNANSWERED"
                console.print(f"\n{i+1}. [{q['agent'].upper()}] {status}")
                console.print(f"   Question: {q['question']}")
                if q.get('context'):
                    console.print(f"   Context: {q['context'][:100]}...")
                console.print(f"   Time: {q['timestamp']}")
            console.print()

    if show_type in ["all", "insights"]:
        insights = state.get("blackboard.insights", [])
        if insights:
            console.print("[bold blue]💡 Insights[/bold blue]")
            for i, insight in enumerate(insights):
                console.print(f"\n{i+1}. [{insight['agent'].upper()}]")
                console.print(f"   {insight['insight']}")
                console.print(f"   Time: {insight['timestamp']}")
            console.print()

    if show_type in ["all", "messages"]:
        messages = state.get("blackboard.messages", [])
        if messages:
            console.print("[bold]📨 Messages[/bold]")
            for i, msg in enumerate(messages[-10:]):  # Show last 10
                severity_color = {
                    "info": "white",
                    "warning": "yellow",
                    "error": "red"
                }.get(msg.get("severity", "info"), "white")
                console.print(f"\n{i+1}. [{msg['agent'].upper()}] {msg['type']}")
                console.print(f"   [{severity_color}]{msg['content']}[/{severity_color}]")
                console.print(f"   Time: {msg['timestamp']}")
            console.print()

    # Show summary
    unresolved = len(state.get_unresolved_blockers())
    unanswered = len(state.get_unanswered_questions())
    if unresolved > 0 or unanswered > 0:
        console.print(f"[bold yellow]⚠️  Attention needed: {unresolved} blockers, {unanswered} questions[/bold yellow]\n")


@app.command()
def metrics():
    """Show sprint efficiency metrics and telemetry."""
    from .telemetry import TelemetryTracker

    state = VibeState(get_project_root())
    state.load()

    if not state.has_active_sprint:
        console.print("[yellow]No active sprint[/yellow]")
        return

    tracker = TelemetryTracker(get_project_root())
    report_md = tracker.generate_markdown_report(state)

    console.print("\n" + report_md + "\n")

    # Offer to save report
    if typer.confirm("Save telemetry report?"):
        report_path = tracker.save_sprint_report(state)
        console.print(f"\n[green]✅ Report saved to: {report_path}[/green]\n")


@app.command()
def version():
    """Show version information."""
    console.print("MADE Orchestrator v1.0.0")


def main():
    """Entry point for CLI."""
    app()


if __name__ == "__main__":
    main()
