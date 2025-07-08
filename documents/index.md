# Vibe-Coding Project Hub

This hub connects all documentation for your vibe-coding projects. Use this as your starting point
for each coding session.

## Core Documentation

| Document | Purpose | When to Update |
|----------|---------|---------------|
| [📝 PRD](prd.md) | Product requirements and decisions | Before feature changes |
| [📋 Backlog](backlog.md) | Task tracking and sprint management | Daily |
| [📓 Dev Log](dev_log.md) | Session records and implementation notes | Every session |

## Integration Documentation

| Document | Purpose | When to Update |
|----------|---------|---------------|
| [🧠 Knowledge Base](knowledge_base.md) | Patterns, solutions, and lessons learned | When discovering reusable patterns |
| [✓ Quality Gates](quality_gates.md) | Standards and compliance tracking | Before completing features |
| [📊 Enhanced System](enhanced_documentation_system.md) | Documentation system guide | When refining processes |

## Session Start Checklist

1. Read your [last dev log entry](dev_log.md)
2. Check [current sprint](backlog.md#active-sprint-yyyy-mm-dd-to-yyyy-mm-dd) status
3. Review any [pending decisions](prd.md#decision-log)
4. Set goals for this session

## Quick Reference: Cross-Document Linking

Use these reference formats to maintain traceability:

- `[PRD-decision:YYYY-MM-DD]` - Reference to decision in PRD
- `[BL-task:TaskID]` - Reference to backlog task
- `[DL:YYYY-MM-DD]` - Reference to dev log entry
- `[KB:PatternName]` - Reference to knowledge base pattern
- `[QG:CheckpointName]` - Reference to quality gate checkpoint

## Project Health Dashboard

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Test Coverage | ≥80% | - | - |
| Ruff Warnings | <10 | - | - |
| Mutation Score | ≥75% | - | - |
| Open Tasks | - | - | - |
| Days Since Last Commit | <7 | - | - |

## Tools & Scripts

- [Run Session Context](../scripts/session_context.py) - Gather context for current session
- [Validate Links](../scripts/validate_links.py) - Check cross-document references
- [Generate Quality Dashboard](../scripts/quality_dashboard.py) - Track code health metrics

---

*Last Updated: [Template Version]*

*Project Status: [Template - No Active Project]*
