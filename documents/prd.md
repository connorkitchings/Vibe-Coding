# Product Requirements Document (PRD)

## PROJECT

[Project Name]

## GOAL

(1–2 sentences summarizing the purpose and outcome)

*For architecture, tech stack, and setup details, see [`project_context.md`](project_context.md).*

## USERS

- [Primary persona(s)]

## CORE FEATURES

- Feature A (must-have)
- Feature B (must-have)
- Feature C (nice-to-have)

## OUT OF SCOPE

- [Items/features not included]

## SUCCESS METRICS

- Deliverables tracked and up-to-date in `implementation_schedule.md`

- [Usage criteria]
- [Performance targets]

## SYSTEM DIAGRAM

```ascii
# Insert ASCII diagram of system components here
# Example:
+-------------+      +------------+     +------------+
| Web UI      | ---> | API Server | --> | Database   |
+-------------+      +------------+     +------------+
```

## DATA FLOW

```ascii
# Insert data flow diagram here
# Example:
[User Input] --> [Validation] --> [Processing] --> [Storage]
```

## EDGE CASES & RISKS

- [Describe edge cases and risks identified]

## DEPENDENCY GRAPH

- Feature A depends on: [components/libraries]
- Feature B depends on: [components/libraries]

## DECISION LOG

| Date | Decision | Alternatives | Rationale | Commit/PR | Reversible? |
|------|----------|--------------|-----------|-----------|-------------|
| YYYY-MM-DD | [Decision made] | [Other options] | [Why] | [Link] | Yes/No |

## VERSION HISTORY

| Version | Date | Summary of Changes | Author |
|---------|------|---------------------|--------|
| v0.1 | YYYY-MM-DD | Initial draft | [Name] |
