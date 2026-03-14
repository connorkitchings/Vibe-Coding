# Agent Playbook

This playbook maintains the evolving knowledge, strategic constraints, and execution patterns for this repository. It acts as the dynamic memory for the Agentic Context Engineering (ACE) framework.

## [RULES]
1. **Branch Protection**: NEVER commit directly to `main`. Always check `git branch` and create a feature branch.
2. **Session Persistence**: Every session must conclude with a documented log in `session_logs/`.
3. **Mandatory Health Checks**: Code must pass `uv run ruff check .` and `uv run pytest` before any commit.
4. **Secret Zero**: Never hardcode credentials. Always utilize environment variables.
5. **Test Coverage Policy**: Every new feature requires tests. Every bug fix requires a regression test.

## [STRATEGIES]
1. **Template Adaptation & Initialization**: When setting up a new project from this template, first execute setup scripts, adapt the Context Router (`.agent/CONTEXT.md`), and selectively prune boilerplate code (e.g., in `notebooks/` and `models/`).
2. **Multi-Tool Synergy**: Write deterministic, self-contained scripts and follow strict formatting (`ruff`) to ensure the codebase remains navigable and modifiable by any supported AI CLI (Gemini, Claude Code, Codex).
3. **Continuous Context Maintenance**: Regularly run health checks and session handoff routines to ensure that the context files accurately reflect the current state of the architecture.

## [SUCCESS_PATTERNS]
- **Markdown Ingestion**: Leverage the integrated `markdown.new` URL-to-Markdown utility for fetching clean documentation over raw web scraping.
- **Workflow Automation**: Use `uv run scripts/vibe_sync.py start|end` to correctly manage session context and logs.
- **Incremental Validation**: Run `make validate` locally before triggering CI/CD workflows to prevent noisy pipeline failures.
