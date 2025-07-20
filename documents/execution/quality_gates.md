Quality Gates
This document contains the checklists and standards that ensure every piece of work is high-quality,
consistent, and secure before it's integrated.

1. Pre-Commit Checklist
Run this checklist before every git commit.

[ ] Code is formatted: Ran black . or prettier --write .

[ ] Linter passes: Ran ruff . or eslint . with zero errors.

[ ] Code is self-documented: Variables and functions have clear, intention-revealing names.

[ ] No commented-out code: Dead code has been removed.

[ ] No hardcoded secrets: API keys, passwords, etc., are loaded from environment variables.

[ ] Commit message is descriptive: Follows the convention in project_context.md.

1. Pre-Merge Checklist (Pull Request)
Run this more thorough checklist before merging a feature branch into main.

[ ] All Pre-Commit checks pass.

[ ] Feature works as intended: Manually tested the primary user flow.

[ ] Unit tests are written and passing: All new logic is covered by tests.

[ ] Test coverage has not decreased: Run coverage report.

[ ] Relevant documentation is updated: prd.md, project_context.md, or README.md have been updated if
necessary.

[ ] Security checklist is reviewed: See section 3 below.

[ ] No "TODO" comments remain: All temporary todos have been resolved or converted to tasks in implementation_schedule.md.

1. Security Review Checklist
A mandatory review for any feature handling user input, authentication, or data.

Input & Data Validation
[ ] All user-provided data is sanitized and validated on the server-side.

[ ] SQL injection is prevented (using parameterized queries/ORMs).

[ ] Cross-Site Scripting (XSS) is prevented (output is properly encoded/escaped).

Authentication & Authorization
[ ] Passwords are not stored in plain text (hashed and salted).

[ ] Endpoints correctly verify that the user is authenticated.

[ ] Endpoints correctly verify that the user is authorized to access/modify the specific resource.

Error Handling & Logging
[ ] Error messages shown to users are generic and do not leak internal system details (e.g., stack traces).

[ ] Sensitive information (passwords, API keys) is not present in logs.

1. Definition of Done (DoD)
This is the global standard for any task to be marked as "Done" in the implementation_schedule.md.

A task is considered Done only when:

All code has been merged into the main branch.

All checks in the Pre-Merge Checklist are complete.

The feature has been deployed to a staging or production environment.

The corresponding task in implementation_schedule.md is marked as ✅ Done.
