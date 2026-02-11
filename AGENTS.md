# AGENTS.md — Multi-Tool AI Guidance

> **Purpose:** Universal guidance for AI coding tools (Claude Code, Gemini CLI, Codex CLI, Antigravity). Read this first when starting any session.

**Last Updated:** 2026-02-11
**Template Version:** 2.0 (Multi-Tool)

---

## 🚨 Critical Rules (MUST READ)

### Branch Safety
- **NEVER work on `main` branch**
- Check current branch: `git branch`
- Create feature branch immediately if on main: `git checkout -b feat/<name>`

### Session Logging
- **Every session MUST create a log** in `session_logs/MM-DD-YYYY/N - Title.md`
- Use session start/end skills from `.agent/skills/`
- Update `docs/implementation_schedule.md` after completing tasks

### Project-Specific "NEVER" Rules
<!-- ⚠️ TEMPLATE NOTE: Add your project's critical constraints here -->

**Example constraints (replace with yours):**
- Never commit secrets or API keys
- Never modify database schemas without migration
- Never push directly to `main`
- Never skip tests before committing

---

## Session Management

### Boot Order (Read in this exact order)

When starting a new session, load files in this sequence:

1. **AGENTS.md** (this file) — Critical rules and overview
2. **README.md** — Project overview and quick start
3. **.agent/CONTEXT.md** — Current project state and status
4. **session_logs/** (last 3-5) — Recent development context
5. **docs/implementation_schedule.md** — Current priorities

**Do NOT pre-load other docs.** Open files on-demand when needed.

### Starting a Session

Load `.agent/skills/start-session/SKILL.md` to:
1. Verify you're on a feature branch (not `main`)
2. Load minimal context (Tier 1 files only)
3. Review recent session logs
4. Produce planning-only output with roadmap options
5. Wait for user approval before implementing

**Critical:** DO NOT implement code during the planning phase.

### Ending a Session

Load `.agent/skills/end-session/SKILL.md` to:
1. Create session log in `session_logs/MM-DD-YYYY/N - Title.md`
2. Run health check: `.agent/workflows/health-check.sh`
3. Update `docs/implementation_schedule.md` if tasks completed
4. Propose commit message (don't commit without approval)
5. Document handoff for next session

---

## Project Overview

### What This Template Provides

<!-- ⚠️ TEMPLATE NOTE: Update this section with your project specifics -->

This is a **Vibe Coding template** for AI-assisted development. It provides:
- Multi-tool AI guidance (Claude Code, Gemini, Codex, Antigravity)
- Session management workflows
- Quality gates and guardrails
- Development standards and checklists

**Technologies:** Python 3.10+ · UV · Ruff · Pytest · MkDocs

### Essential Commands

```bash
# Setup
uv sync

# Development loop
uv run ruff format . && uv run ruff check .
uv run pytest

# Health check (before commits)
sh .agent/workflows/health-check.sh
```

**See `.codex/QUICKSTART.md` for full command reference.**

---

## Roles & Routing (Lightweight)

Use these "hats" to structure work. Keep scopes separate.

- **Navigator** — Triage, plan (3-7 lines), route to specialist · Context: ≤2.5k tokens
- **DataOps** — Data pipelines, schemas, validation, idempotence · Context: ≤2k tokens
- **Feature/Core** — Business logic, transforms, prevent data leakage · Context: ≤2k tokens
- **Web/UI** — Frontend, API endpoints, happy path first · Context: ≤2k tokens
- **DevEx/CI** — Tests, linting, CI jobs, fast feedback loops · Context: ≤2k tokens
- **Docs/PM** — Documentation, planning, minimal diffs only · Context: ≤2k tokens

### Handoff Packet Template

When routing between roles:

```
Task: [Outcome-based title]
DoD: [Specific success criteria]
Files: [Relevant paths with line numbers]
Constraints: [Timebox, scope limits]
Artifacts: [Expected outputs]
Rollback: [Plan if failure]
```

**Escalate** if unsure after 2 attempts.

---

## Quality Gates

### Pre-Commit Checklist
- [ ] Code formatted: `uv run ruff format .`
- [ ] Linting passes: `uv run ruff check .`
- [ ] Tests pass: `uv run pytest`
- [ ] No secrets in code
- [ ] Branch is not `main`

### Pre-Merge Checklist
- [ ] All pre-commit checks pass
- [ ] Session log created
- [ ] Documentation updated if behavior changed
- [ ] Implementation schedule updated
- [ ] Tests cover new code (no coverage decrease)

### Definition of Done
A task is **Done** only when:
- Code merged to `main` and CI passes
- Tests cover new logic
- Docs updated where relevant
- Task status updated in implementation schedule

---

## Guardrails

### Human Review Required (Stop & Ask)
- Schema or API contract changes
- Secrets, auth, or infrastructure configuration
- Database migrations
- Dependency upgrades beyond patch version
- Deployment configuration changes
- Test changes that alter public behavior
- Ambiguous acceptance criteria

### Anti-Patterns (Don't)

**Process:**
- ❌ Loading all docs upfront "just in case"
- ❌ Implementing without user approval
- ❌ Working on `main` branch
- ❌ Skipping session logs
- ❌ Proposing changes without running current state first
- ❌ Pasting full file contents instead of diffs

**Technical:**
- ❌ Hardcoding values that should be in config
- ❌ Committing secrets or credentials
- ❌ Skipping tests
- ❌ Creating intermediate tables/files unnecessarily
- ❌ Continuing past 2 failed attempts without escalating

---

## Context Management

### Context Budget

- **Navigator:** ≤2.5k tokens (initial triage)
- **Specialist:** ≤2k tokens (deep dive)
- **Per-session total:** Prefer ≤10k tokens, max 50k tokens

### Tiered Loading

**Tier 1 - Minimal (ALWAYS load first):**
- AGENTS.md (this file)
- README.md
- .agent/CONTEXT.md
- Last 3-5 session logs

**Tier 2 - Task-specific (load as needed):**
- docs/implementation_schedule.md
- docs/development_standards.md
- docs/checklists.md
- Specific code files being modified

**Tier 3 - Deep dive (on-demand only):**
- docs/architecture/
- Full module exploration
- Historical decision logs

### What NOT to Read Automatically
- `artifacts/`, `.venv/`, `.git/`, `**__pycache__/`
- `notebooks/` (only when debugging exploration)
- `session_logs/` older than 3-5 entries
- Files > 200 KB
- Files unchanged in last 30 days

---

## Troubleshooting

### Quick Diagnostics

**Lint fails:**
```bash
uv run ruff check . --fix
uv run ruff format .
```

**Tests fail locally:**
```bash
uv run pytest -vv -k <test_pattern>  # Verbose
uv run pytest --lf                   # Last failed
```

**Import errors:**
```bash
uv sync
```

**Context drift:**
1. Summarize progress in session log
2. Clear chat history
3. Resume from session log + boot order docs

**Stuck > 30 minutes:**
1. Document blockers in session log
2. Create handoff packet
3. Flag for human review

**See `docs/troubleshooting.md` for full triage matrix.**

---

## Multi-Tool Compatibility

This template works with **Claude Code, Gemini CLI, Codex CLI, and Antigravity**. All tools:
- Read `AGENTS.md` (via tool-specific entry points or directly)
- Share same session logging format
- Use same quality gates and essential commands
- Follow same guardrails

**Tool-specific entry points:**
- **Claude Code**: `CLAUDE.md` → `AGENTS.md`
- **Gemini CLI**: `GEMINI.md` → `AGENTS.md`
- **Codex/Antigravity**: `AGENTS.md` directly

---

## Key Files Reference

| Need | File |
|------|------|
| Start here | `AGENTS.md` (this file) |
| Project overview | `README.md` |
| Current status | `.agent/CONTEXT.md` |
| Quick commands | `.codex/QUICKSTART.md` |
| Project map | `.codex/MAP.md` |
| Current priorities | `docs/implementation_schedule.md` |
| Standards | `docs/development_standards.md` |
| Checklists | `docs/checklists.md` |
| Recent work | `session_logs/` (last 3-5) |
| Skills catalog | `.agent/skills/CATALOG.md` |
| Troubleshooting | `docs/troubleshooting.md` |

---

## When to Update This File

Update AGENTS.md when:
- Adding/removing agent roles
- Modifying escalation triggers or quality gates
- Changing core workflow (session templates, routing)
- Adding new safety guardrails
- Updating tooling in command palette
- Project-specific critical rules change

Keep changes atomic. Document rationale in git commit message.

---

**Remember:** Load minimal context. Plan before implementing. Keep changes small and testable. Log every session.
