# Vibe Coding Template — AI Agent Context Brief

> **Entry point for all AI sessions.** Read this first, then load relevant skills.

---

## Project Snapshot

**Vibe Coding Template**: Multi-tool AI-assisted development template
**Stack**: Python 3.10+ · UV · Ruff · Pytest · MkDocs
**Status**: 🟢 Template Ready (2026-02-11)

### Current State

<!-- ⚠️ TEMPLATE NOTE: Update this section with your project status -->

- **Version**: 2.0 (Multi-Tool)
- **Current Focus**: Template ready for new projects
- **Next Milestone**: Adapt for specific project use
- **Previous**: MADE system removed, lean multi-tool template created

## Recent Activity
- Implemented comprehensive template improvements (Feb 2026).
- Completed all 15 improvement opportunities across 6 phases.
- Added GitHub Actions CI workflows, validation scripts, and enhanced documentation.

### Architecture

<!-- ⚠️ TEMPLATE NOTE: Update with your project architecture -->

**Template provides:**
- Multi-tool AI guidance (Claude Code, Gemini CLI, Codex CLI, Antigravity)
- Session management workflows
- Quality gates and guardrails
- Development standards
- Testing framework
- Documentation structure

---

## ⚠️ Critical Rules

1. **NEVER work on `main`**. Check branch: `git branch`. Create feature branch immediately if on main.
2. **Session logging required**. Every session creates a log in `session_logs/`.
3. **Health checks before commits**. Run: `.agent/workflows/health-check.md`
4. **No secrets in code**. Use environment variables and config files.
5. **Tests required**. Every feature needs tests. Every bug needs regression test.

<!-- ⚠️ TEMPLATE NOTE: Add project-specific critical rules here -->

---

## 5 Essential Commands

```bash
# Check branch (CRITICAL - never work on main)
git branch

# Setup (first time)
uv sync

# Development loop
uv run ruff format . && uv run ruff check .
uv run pytest

# Health check (before commits)
# Follow steps in .agent/workflows/health-check.md

# Session Management
uv run scripts/vibe_sync.py start
uv run scripts/vibe_sync.py end
```

---

## Entry Points by Task

### Starting a Session
→ **Read**: `.agent/CONTEXT.md` (this file)
→ **Then**: Load skill `.agent/skills/start-session/SKILL.md`
→ **Produces**: Planning output only (no code until user approves)

### During Development
→ **Skills**: `.agent/skills/CATALOG.md` for repeatable patterns
→ **Status**: Check `docs/implementation_schedule.md`

### Closing a Session
→ **Load skill**: `.agent/skills/end-session/SKILL.md`
→ **Required**: Create session log, health check, commit checklist
→ **Handoff**: Document context for next session

---

## Key Files (When You Need Them)

| Need | File |
|------|------|
| Agent guidance | `.agent/AGENTS.md` |
| Project overview | `README.md` |
| Full project map | `.codex/MAP.md` |
| Quick commands | `.codex/QUICKSTART.md` |
| Current priorities | `docs/implementation_schedule.md` |
| Development standards | `docs/development_standards.md` |
| Architecture decisions | `docs/architecture/adr/` |
| Session logs | `session_logs/` (read last 3-5) |

---

## Directory Structure

```
Vibe-Coding/
├── .agent/              # Skills, workflows, agent guidance
│   ├── CONTEXT.md       # This file
│   ├── skills/          # Task contracts (start/end session)
│   └── workflows/       # Health checks, automation
├── .codex/              # Quick reference (cached context)
│   ├── MAP.md           # Project tree
│   ├── QUICKSTART.md    # Essential commands
│   └── README.md        # Purpose explanation
├── src/                 # Source code
├── tests/               # Test suite
├── docs/                # Documentation
├── scripts/             # Utility scripts
├── session_logs/        # Session history
└── config/              # Configuration files
```

---

**Next**: Load skill for your current task from `.agent/skills/CATALOG.md`
