# MADE Orchestrator

The **MADE (Multi-Agent Developer Environment) Orchestrator** is a coordination layer that automates multi-agent development workflows by managing handoffs between Claude Code (planning), Gemini CLI (context analysis), and Codex CLI (execution).

## Overview

MADE eliminates manual coordination friction in the "Plan -> Implement -> Review" cycle by:
- Managing shared state across agent sessions (`.vibe_state.json`)
- Generating handoff packets with scoped context
- Automating or semi-automating agent invocations
- Tracking progress in session logs

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: CONTEXT (Gemini - 1M tokens)                      │
│  • Scan entire repo structure                               │
│  • Summarize recent commits, open issues                    │
│  • Output: context summary → .vibe_state.json               │
│                            ↓                                 │
│  PHASE 2: PLAN (Claude Code - Architect)                    │
│  • Receive context summary from Phase 1                     │
│  • Design implementation approach                           │
│  • Output: PLAN.md + tasks → .vibe_state.json               │
│                            ↓                                 │
│  PHASE 3: EXECUTE (Codex CLI - Muscle)                      │
│  • For each task in dependency order:                       │
│    - Generate handoff packet                                │
│    - Invoke Codex with scoped context                       │
│  • Output: code changes + session log                       │
└─────────────────────────────────────────────────────────────┘
```

## Installation

1. Install dependencies:
```bash
uv sync
```

2. Source shell aliases (optional):
```bash
source scripts/vibe/aliases.sh
```

## Usage

### Quick Start

Start a new sprint:
```bash
vibe sprint start "Add user authentication system"
```

Run context analysis:
```bash
vibe context
```

Generate plan (manual):
```bash
vibe plan
# After creating PLAN.md:
vibe plan --load PLAN.md
```

Execute tasks:
```bash
vibe exec --interactive
```

### Full Sprint Workflow

Run all phases in sequence:
```bash
vibe sprint full "Add user authentication system"
```

### Check Status

View current sprint status:
```bash
vibe status
```

### Execute Specific Task

Execute a single task by ID:
```bash
vibe exec --task task-001
```

### Reset State

Reset sprint state:
```bash
vibe reset
```

## Shell Aliases

When you source `scripts/vibe/aliases.sh`, you get:

```bash
vibe                  # Main CLI
vibe-status          # Show sprint status
vibe-sprint          # Sprint commands
vibe-context         # Run context analysis (Phase 1)
vibe-plan            # Run planning (Phase 2)
vibe-exec            # Run execution (Phase 3)
vibe-reset           # Reset sprint state

# Workflow functions
vibe-quick <objective>           # Start a new sprint
vibe-full-sprint <objective>     # Run complete workflow
vibe-task <task-id>              # Execute specific task
```

## State Management

MADE maintains state in `.vibe_state.json` at the project root:

```json
{
  "version": "1.0",
  "sprint": {
    "id": "sprint-2026-02-10-001",
    "status": "planning|executing|paused|completed|failed",
    "objective": "User-defined sprint goal"
  },
  "context": {
    "repo_summary_path": "session_logs/2026-02-10_sprint-001_context.md",
    "token_budget_used": 45000
  },
  "plan": {
    "path": "PLAN.md",
    "tasks": [
      {"id": "task-001", "title": "...", "status": "pending"}
    ]
  },
  "session_log": "session_logs/2026-02-10_sprint-001.md"
}
```

## Agent Adapters

MADE includes adapters for three agent types:

### Claude Code Adapter
- **Role:** Architect/Planner
- **Prompt:** `.agents/prompts/made_architect.md`
- **Invocation:** Manual (prints prompt for copying)

### Gemini CLI Adapter
- **Role:** Context Analyst (1M token window)
- **Prompt:** `.agents/prompts/made_librarian.md`
- **Invocation:** Automatic via subprocess

### Codex CLI Adapter
- **Role:** Executor/Muscle
- **Prompt:** `.agents/prompts/made_executor.md`
- **Invocation:** Automatic via subprocess

## Handoff Packets

Handoff packets provide task-specific context to execution agents:

```markdown
# Handoff Packet

## Task Context
**Task ID:** task-001
**Title:** Implement user authentication

## Task Description
[Detailed task description]

## Dependencies
- task-000 (database schema)

## Files to Modify
- `src/auth.py`
- `tests/test_auth.py`

## Acceptance Criteria
- [ ] User can register with email/password
- [ ] Passwords are hashed with bcrypt
- [ ] Tests pass

## Repository Context (Summary)
[Relevant context from Phase 1]

## Full Plan Reference
[Excerpt from PLAN.md]
```

## Session Logs

Each sprint creates a session log in `session_logs/`:

```
session_logs/2026-02-10_sprint-001.md
```

Format:
```markdown
---
date: 2026-02-10
sprint_id: sprint-2026-02-10-001
objective: Add user authentication
agents_used: [gemini, claude, codex]
status: completed
---

## Phase 1: Context (Gemini)
- Token budget: 45,000 / 1,000,000
- Summary: session_logs/2026-02-10_sprint-001_context.md

## Phase 2: Planning (Claude)
- Plan: PLAN.md
- Tasks: 5 total

## Phase 3: Execution (Codex)
### Task 1: Setup auth module
- Status: completed
- Files: src/auth.py, tests/test_auth.py
```

## Hybrid Automation

MADE uses a **hybrid approach** to agent invocation:

- **Auto-invoke:** Gemini CLI and Codex CLI (if available)
- **Manual fallback:** If CLI unavailable, prints prompt for manual execution
- **Interactive confirmation:** Prompts for confirmation between phases

This ensures workflows never block on missing dependencies.

## Development

### Directory Structure

```
scripts/vibe/
├── __init__.py
├── made.py              # Main CLI (Typer-based)
├── state.py             # State management
├── aliases.sh           # Shell aliases
├── agents/
│   ├── __init__.py
│   ├── base.py          # BaseAgent protocol
│   ├── claude.py        # Claude Code adapter
│   ├── gemini.py        # Gemini CLI adapter
│   └── codex.py         # Codex CLI adapter
└── workflows/
    ├── __init__.py
    ├── sprint.py        # Vibe Sprint workflow
    └── handoff.py       # Handoff packet generation
```

### Extending MADE

To add a new agent adapter:

1. Create adapter in `scripts/vibe/agents/`
2. Inherit from `BaseAgent`
3. Implement `is_available()` and `invoke()`
4. Add prompt template in `.agents/prompts/`

Example:
```python
from .base import BaseAgent, AgentResponse

class MyAdapter(BaseAgent):
    def is_available(self) -> bool:
        # Check if CLI is available
        pass

    def invoke(self, prompt: str, context: dict) -> AgentResponse:
        # Invoke agent
        pass
```

## Troubleshooting

### State Corruption

If `.vibe_state.json` becomes corrupted:
```bash
vibe reset --force
```

### Agent Unavailable

If an agent CLI is unavailable, MADE will:
1. Print the prompt for manual execution
2. Wait for user to paste results
3. Continue workflow

### Task Execution Fails

If a task fails during execution:
```bash
# Fix the issue, then resume specific task
vibe exec --task task-001
```

## Integration with Orchestrator

MADE commands are integrated into `scripts/orchestrator.py`:

```python
COMMANDS = {
    "vibe": "uv run python scripts/vibe/made.py",
    "vibe-status": "uv run python scripts/vibe/made.py status",
    # ... other commands
}
```

Run via orchestrator:
```bash
python scripts/orchestrator.py vibe status
```

## Future Enhancements

- [ ] Plan parsing improvements (better PLAN.md parser)
- [ ] Task dependency resolution
- [ ] Parallel task execution
- [ ] Agent output validation
- [ ] Rollback/undo support
- [ ] Web UI for sprint monitoring
- [ ] Integration with GitHub Issues
- [ ] Automatic git commit messages
