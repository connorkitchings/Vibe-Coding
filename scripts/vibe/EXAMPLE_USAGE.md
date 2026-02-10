# MADE Orchestrator - Example Usage

## Installation

```bash
# Install dependencies
uv sync

# Source aliases (optional but recommended)
source scripts/vibe/aliases.sh
```

## Example 1: Quick Start

```bash
# Start a new sprint
vibe sprint start "Implement password reset feature"

# Check status
vibe status
```

Output:
```
✅ Sprint started: sprint-2026-02-10-143052
📋 Objective: Implement password reset feature
Next step: vibe context
```

## Example 2: Phase-by-Phase Execution

### Phase 1: Context Analysis

```bash
vibe context
```

This will:
- Invoke Gemini CLI to analyze the full repository
- Generate a context summary
- Save to `session_logs/[date]_sprint-[id]_context.md`
- Update `.vibe_state.json`

### Phase 2: Planning

```bash
vibe plan
```

This will:
- Display the architect prompt for Claude Code
- You create `PLAN.md` based on the prompt
- Load the plan:

```bash
vibe plan --load PLAN.md
```

### Phase 3: Execution

```bash
# Execute all tasks interactively
vibe exec --interactive

# Or execute a specific task
vibe exec --task task-001
```

## Example 3: Full Sprint (Automated)

```bash
vibe sprint full "Add API rate limiting"
```

This runs all three phases in sequence with minimal manual intervention.

## Example 4: State Management

### Check Current Sprint

```bash
vibe status
```

Output:
```
Sprint: sprint-2026-02-10-143052
Status: executing
Objective: Implement password reset feature

Tasks:
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┓
┃ ID       ┃ Title                    ┃ Status    ┃ Agent ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━┩
│ task-001 │ Create reset endpoint    │ completed │ codex │
│ task-002 │ Add email sending        │ pending   │ codex │
└──────────┴──────────────────────────┴───────────┴───────┘
```

### Reset State

```bash
# With confirmation
vibe reset

# Force reset
vibe reset --force
```

## Example 5: Using Shell Aliases

After sourcing aliases:

```bash
# Quick start
vibe-quick "Implement feature X"

# Check status
vibe-status

# Run phases
vibe-context
vibe-plan
vibe-exec

# Run full sprint
vibe-full-sprint "Add user notifications"

# Execute specific task
vibe-task task-003
```

## Example 6: Via Orchestrator

```bash
# List all commands
python3 scripts/orchestrator.py list

# Run via orchestrator
python3 scripts/orchestrator.py vibe-status
python3 scripts/orchestrator.py vibe-sprint start "Objective"
```

## Example Sprint Workflow

Complete example from start to finish:

```bash
# 1. Start sprint
vibe sprint start "Add user profile editing"

# 2. Run context analysis
vibe context
# Gemini analyzes the repo and creates context summary

# 3. Generate plan
vibe plan
# Claude prompt is displayed, you create PLAN.md

# 4. Load plan
vibe plan --load PLAN.md
# Plan is parsed and tasks are loaded

# 5. Check loaded tasks
vibe status
# Shows all tasks from the plan

# 6. Execute tasks
vibe exec --interactive
# Executes each task, prompting for confirmation

# 7. Verify completion
vibe status
# Shows completed tasks

# 8. Review session log
cat session_logs/2026-02-10_sprint-*.md
```

## Example State File

After running a sprint, `.vibe_state.json` looks like:

```json
{
  "version": "1.0",
  "sprint": {
    "id": "sprint-2026-02-10-143052",
    "status": "executing",
    "objective": "Implement password reset feature"
  },
  "context": {
    "repo_summary_path": "session_logs/2026-02-10_sprint-143052_context.md",
    "token_budget_used": 45000
  },
  "plan": {
    "path": "PLAN.md",
    "tasks": [
      {
        "id": "task-001",
        "title": "Create password reset endpoint",
        "status": "completed",
        "assigned_agent": "codex",
        "description": "...",
        "files_to_modify": ["src/auth.py"],
        "acceptance_criteria": ["Tests pass", "Endpoint returns 200"]
      }
    ]
  },
  "session_log": "session_logs/2026-02-10_sprint-143052.md"
}
```

## Example Session Log

`session_logs/2026-02-10_sprint-143052.md`:

```markdown
---
date: 2026-02-10
sprint_id: sprint-2026-02-10-143052
objective: Implement password reset feature
agents_used: [gemini, claude, codex]
status: in_progress
---

# Sprint: sprint-2026-02-10-143052

## Objective
Implement password reset feature

## Phase 1: Context (Gemini)
Status: completed
Token budget: 45,000 / 1,000,000
Summary: session_logs/2026-02-10_sprint-143052_context.md

## Phase 2: Planning (Claude)
Status: completed
Plan: PLAN.md
Tasks: 3 total

## Phase 3: Execution (Codex)
Status: in_progress

### Task: Create password reset endpoint
- **ID:** task-001
- **Status:** completed
- **Files:** src/auth.py, tests/test_auth.py

### Task: Add email sending
- **ID:** task-002
- **Status:** pending
```

## Error Handling Examples

### CLI Not Available

If Gemini CLI is not available:

```bash
vibe context
```

Output:
```
⚠️  Gemini CLI not available. Using manual fallback.
================================================================================
MANUAL INVOCATION REQUIRED
================================================================================
[Prompt displayed for manual execution]
================================================================================

Execute the above prompt manually and paste the result.
Press Enter when done (or 'skip' to skip this step):
```

### Task Failure

If a task fails during execution:

```bash
vibe exec --task task-002
```

Output:
```
🎯 Executing: Add email sending
⚙️  Invoking Codex CLI for execution...
❌ Task failed: Codex CLI timed out after 10 minutes
```

Recover:
```bash
# Fix the issue, then retry
vibe exec --task task-002
```

## Tips

1. **Always source aliases** for the best experience:
   ```bash
   source scripts/vibe/aliases.sh
   ```

2. **Check status frequently** to track progress:
   ```bash
   vibe-status
   ```

3. **Use interactive mode** for safety:
   ```bash
   vibe exec --interactive
   ```

4. **Review session logs** to understand what happened:
   ```bash
   ls -la session_logs/
   cat session_logs/2026-02-10_sprint-*.md
   ```

5. **Reset state** if things get stuck:
   ```bash
   vibe reset --force
   ```
