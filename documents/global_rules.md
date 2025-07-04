# Global Windsurf Rules for Vibe-Coding Projects

## Core Development Philosophy

**Primary Goal:** Maintain creative momentum while ensuring code quality and project sustainability.

**Stack Preferences:**

- **Backend/Scripts:** Python 3.9+ (prefer 3.11+ for performance)
- **Web Apps:** Streamlit for rapid prototypes, React for production-ready UIs
- **Data:** Pandas, SQLite for local, PostgreSQL for production
- **Testing:** pytest with coverage reporting
- **Linting:** ruff (replaces black + flake8 + isort)

---

## Project Structure Rules

### 1. Mandatory File Structure

Every project must have:

```plaintext
project_root/
├── docs/
│   ├── prd.md          # Product Requirements Document
│   ├── backlog.md      # Task management
│   └── dev_log.md      # Implementation log
├── src/                # Source code
├── tests/              # Test files
├── .pre-commit-config.yaml
├── pyproject.toml      # Project config
└── README.md
```

### 2. Documentation Standards

- **PRD:** Must fit on one screen, update before any major pivot
- **Backlog:** Weekly sprint cycles, tasks estimated in hours (≤8h each)
- **Dev Log:** Update after every coding session, include AI prompts that worked
- **README:** Include setup instructions, core features, and contribution guidelines

---

## Code Quality Gates

### 1. Pre-Commit Hooks (Non-Negotiable)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
  - repo: https://github.com/pyupio/safety-db
    rev: master
    hooks:
      - id: safety
  # pip-audit replaced by uv audit (https://github.com/astral-sh/uv)
  # To audit dependencies, use:
  #   uv audit
  # Optionally, add a custom script or pre-commit hook for uv audit if desired.

```

### 2. Testing Requirements

- **Minimum:** One test per public function/method
- **Coverage:** Aim for 80%+ on core modules
- **Test Types:** Unit tests (fast), integration tests (realistic data)
- **Property-Based:** Use Hypothesis for critical logic
- **Mutation Testing:** mutmut score ≥ 75% for core modules
- **AI Assistance:** Use "Generate tests for [function] covering happy path + 3 edge cases"

### 3. Code Organization

- **Functions:** Max 50 lines, single responsibility
- **Classes:** Max 200 lines, clear purpose documented
- **Files:** Max 500 lines, split if larger
- **Line Length:** PEP 8 ≤ 100 chars (ruff default)
- **Dependencies:** Use [uv](https://github.com/astral-sh/uv) for dependency management. Pin major versions,
  document why each is needed.
  - Install dependencies: `uv pip install -r pyproject.toml`
  - Create virtual environment: `uv venv .venv`
  - Audit dependencies: `uv audit`
  - (If you don't have uv: `pip install uv` or see uv install instructions)

---

## Development Workflow Rules

### 1. Session Startup Protocol

1. Load last 2 dev_log entries
2. Review current sprint in backlog.md
3. Set 2-hour focus blocks with 15-min breaks
4. Update dev_log before ending session

### 2. Feature Development Cycle

1. **Plan:** Break feature into ≤4h tasks
2. **Code:** Write tests first or alongside code
3. **Review:** Run full test suite + linting
4. **Document:** Update relevant docs
5. **Commit:** Use Conventional Commits (e.g., `feat:`, `fix:`, `docs:`), link to issues

### 3. AI Collaboration Guidelines

- **Context Feeding:** Always include PRD + current task + recent dev_log
- **Prompt Templates:** Use standardized prompts from appendix
- **Validation:** Always test AI-generated code before committing

---

## Tech Stack Decision Matrix

### Web Framework Selection

| Requirement | Use Streamlit | Use React |
|-------------|---------------|-----------|
| Quick prototype | ✅ | ❌ |
| Complex UI/UX | ❌ | ✅ |
| Real-time features | ❌ | ✅ |
| Data visualization | ✅ | ⚠️ |
| Mobile responsive | ❌ | ✅ |
| Team collaboration | ❌ | ✅ |

### Database Selection

- **SQLite:** Prototypes, single-user apps
- **PostgreSQL:** Multi-user, production apps
- **JSON files:** Configuration, small datasets (<1MB)

---

## Project Lifecycle Checkpoints

### Phase 0: Idea Validation (30 minutes max)

- [ ] MVP fits in 2-4 weeks part-time
- [ ] Clear problem statement exists
- [ ] Tech stack decision made using matrix above
- [ ] Success criteria defined (measurable)
- [ ] Data privacy/PII handling requirements documented in data_dictionary/README.md

### Phase 1: Setup (2 hours max)

- [ ] Project structure created
- [ ] Core docs (PRD, backlog, dev_log) initialized
- [ ] Development environment configured
- [ ] First commit pushed with project skeleton

### Phase 2-4: Development Sprints (weekly cycles)

- [ ] Sprint planning: tasks ≤8h each
- [ ] Daily progress: update backlog status
- [ ] Sprint review: what worked/didn't work
- [ ] Sprint retrospective: update dev_log with learnings

### Phase 5: MVP Release

- [ ] All core features tested and working
- [ ] Documentation updated for users
- [ ] Deployment automated (GitHub Actions)
- [ ] Maintenance plan documented

---

## Emergency Protocols

### When Stuck (>2 hours on one issue)

1. Document the problem in dev_log
2. Try different AI model/prompt approach
3. Break problem into smaller pieces
4. Ask for help (Stack Overflow, Discord, etc.)
5. Consider simplifying requirements

### Technical Debt Spike

1. Identify and document the debt item in dev_log and backlog
2. Time-box the fix (e.g., 2 hours max)
3. If not resolved, log a ticket in backlog and revisit next sprint

### When Losing Motivation

1. Review original PRD - why did you start?
2. Celebrate completed tasks in backlog
3. Reduce scope to regain momentum
4. Take a longer break (1-2 days)
5. Consider pivoting if passion is gone

### When Requirements Change

1. Update PRD immediately
2. Assess impact on current sprint
3. Re-prioritize backlog
4. Document decision rationale
5. Communicate changes if team project

---

## Success Metrics

### Project Health Indicators

- **Green:** Tests passing, docs current, regular commits, ruff warnings < 10, test coverage > 80%
- **Yellow:** 1-2 weeks since last commit, docs slightly stale, ruff warnings < 30, test coverage 60-80%
- **Red:** Broken tests, outdated docs, no commits >3 weeks, ruff warnings ≥ 30, test coverage < 60%

### Personal Productivity Metrics

- **Sprint Velocity:** Average tasks completed per week
- **Code Quality:** Test coverage %, ruff warnings, mutation score
- **Learning Velocity:** New techniques documented in dev_log

---

## AI Prompt Templates (Quick Reference)

### Planning Phase

- "Draft a PRD for [idea] aimed at a solo developer MVP in Python"
- "Break down [feature] into tasks taking 2-4 hours each"
- "What are 5 potential risks for this project and how to mitigate them?"

### Development Phase

- "Write a testable Python function for [feature] with docstrings and error handling"
- "Create pytest tests for [function] covering happy path + 3 edge cases"
- "Review this code for Python best practices and suggest improvements"
- "Refactor this 200-line file into smaller modules without breaking tests"

### Debugging Phase

- "Help debug this Python error: [paste error + relevant code]"
- "Suggest 3 ways to optimize this slow function: [paste code]"
- "What edge cases am I missing for this input validation?"

---

*Remember: These rules are guidelines to maintain quality and momentum. Adapt them based on project
needs, but always maintain the core principle of balancing creativity with sustainability.
This ensures a healthy project and a happy developer.*
