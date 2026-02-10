# MADE Orchestrator

**Multi-Agent Developer Environment** - Coordination layer for multi-agent development workflows.

## Quick Start

```bash
# Install dependencies
uv sync

# Source aliases (optional)
source scripts/vibe/aliases.sh

# Start a sprint
vibe sprint start "Your objective here"

# Run phases
vibe context    # Phase 1: Context analysis (Gemini)
vibe plan       # Phase 2: Planning (Claude Code)
vibe exec       # Phase 3: Execution (Codex)

# Check status
vibe status
```

## What is MADE?

MADE automates the coordination between:
- **Claude Code** (Planning/Architecture)
- **Gemini CLI** (Large-context analysis)
- **Codex CLI** (Code execution)

It manages state, generates handoff packets, and tracks progress through a 3-phase sprint workflow.

## Documentation

See [docs/made-orchestrator.md](../../docs/made-orchestrator.md) for complete documentation.

## Architecture

```
Phase 1: CONTEXT    → Gemini analyzes entire repo (1M tokens)
Phase 2: PLAN       → Claude designs implementation
Phase 3: EXECUTE    → Codex executes tasks
```

All state stored in `.vibe_state.json` at project root.

## Files

- `made.py` - Main CLI (Typer-based)
- `state.py` - State management
- `aliases.sh` - Shell aliases
- `agents/` - Agent adapters (Claude, Gemini, Codex)
- `workflows/` - Sprint and handoff workflows

## Requirements

- Python 3.10+
- typer
- rich
- Optional: Claude Code CLI, Gemini CLI, Codex CLI

## Examples

### Full Sprint
```bash
vibe sprint full "Add user authentication"
```

### Execute Specific Task
```bash
vibe exec --task task-001
```

### Reset State
```bash
vibe reset --force
```

## Integration

MADE is integrated into the main orchestrator:
```bash
python scripts/orchestrator.py vibe status
```
