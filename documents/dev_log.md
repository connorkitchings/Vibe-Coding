## Developer Session Entry Template

### [YYYY-MM-DD]

#### 🔄 STATE OF CODEBASE

- **Active Branch:** [branch name]
- **Current Focus:** [module/component name]
- **Pending PRs/Issues:** [list or links]
- **Test Status:** [passing/failing, coverage %]
- **Key Files Modified:** [list with paths]

#### ✅ WHAT WORKED

- [Notes on what went well]

#### ❌ WHAT DIDN'T

- [Notes on what didn't work]

#### 🤖 AI TRICKS

- Prompt: "[Prompt used]" → [Result/insight]

#### 🔀 DECISIONS

- Chose [library/tool] over [alternative] because... (link commit hash or PR)

#### 📊 CODE HEALTH

- **Ruff Warnings:** [count]
- **Test Coverage:** [percentage]
- **Technical Debt Added:** [description if any]
- **Technical Debt Resolved:** [description if any]

#### 📘 LEARNINGS & PATTERNS

- [Reusable pattern discovered]
- [Useful technique to remember]

#### 🏁 SESSION HANDOFF

- **Stopping Point:** [exact description of where work stopped]
- **Next Immediate Task:** [concrete next step with enough detail to start immediately]
- **Known Issues:** [bugs or problems to be aware of]
- **Context Links:** [links to relevant docs, discussions, or resources]

#### 📝 NEXT UP

- [Planned next steps with priority]

---

## Historical Entries

(Add future session entries below using the template above)

---

# Project Context

## Overview

- Brief description of the project and its main goal.
- Key features or modules.

## Architecture

- High-level architecture summary (list major components/services).
- Folder structure explanation (e.g., `/src`, `/tests`, `/components`).

## Technology Stack

- Languages, frameworks, and libraries used.
- Version requirements (e.g., Node.js 18+, Python 3.11).

## Setup Instructions

- Environment setup commands.
- How to install dependencies and run the project.

## Version Control Best Practices

### Branch Naming Convention

```bash
# Feature development
feature/user-auth
feature/payment-integration

# Bug fixes
bugfix/login-validation
bugfix/memory-leak-fix

# Hotfixes for production
hotfix/security-patch
hotfix/critical-bug

# Release preparation
release/v1.2.0
```

### Commit Message Format

```bash
# Format: <type>: <description>
feat: add user authentication endpoint
fix: resolve login validation bug
docs: update API documentation
test: add user registration tests
refactor: simplify database connection logic
style: fix code formatting issues
chore: update dependencies
```

### Code Review Process (Solo Projects)

#### AI-Assisted Review Checklist

- [ ] **Security Review:** "Review this code for security vulnerabilities"
- [ ] **Performance Review:** "Identify potential performance bottlenecks"
- [ ] **Code Quality:** "Review for bugs, readability, and maintainability"
- [ ] **Test Coverage:** "Suggest additional test cases for this code"

#### Manual Review Checklist

- [ ] Error handling implemented
- [ ] Input validation present
- [ ] Code follows project style guide
- [ ] Documentation updated
- [ ] No hardcoded secrets or credentials
- [ ] Edge cases considered

#### Review Prompts

```markdown
# Security Review
"Review this [language] code for security vulnerabilities, focusing on input validation,
authentication, and data sanitization: [code]"

# Performance Review
"Analyze this code for performance issues and suggest optimizations: [code]"

# Code Quality Review
"Review this code for bugs, readability issues, and suggest improvements: [code]"
```

## Coding Standards

- Naming conventions (e.g., snake_case for variables).
- File organization rules.
- Style guide references.

## Contact & Ownership

- Main contributors or maintainers.
- How to get support or ask questions.
