The Vibe Coding System Playbook

> 📚 For a high-level overview and entry point to all documentation, see [README.md](../README.md).
> 📁 /documents: Contains all Vibe Coding System documentation.

A structured, flexible workflow for taking an idea from concept to delivery, designed for
efficient and context-aware collaboration between a developer and an AI assistant.

## Core Principles

- **Keep It Lean:** Focus on a few core, high-signal documents.
- **Short Sprints:** Maintain momentum with weekly or bi-weekly cycles.
- **Context Discipline:** Only provide relevant documents to focus AI collaboration.
- **User-Centric:** Test with real users early and often.
- **AI as Co-Pilot:** Use AI for generation, review, and ideation, but always validate its output.
- **Continuous Documentation:** Documentation is a continuous process that preserves context and decisions.

---

1. The Documentation Ecosystem
This system is built on a set of specialized Markdown documents designed to separate concerns
and maintain clarity.

2.1. Strategic & Planning Documents
Document

Purpose

When to Use

prd.md

The "What" & "Why": Defines project goals, user personas, core features, scope, and success
metrics. The single source of truth for the project's vision.

At project inception. During planning phases. When a feature's purpose is in question.

implementation_schedule.md

The "When" & "How": A tactical plan for execution. Tracks deliverables, tasks, sprints,
dependencies, risks, and user testing schedules.

For sprint planning. For daily task management. To assess project velocity and risks.

project_context.md

The "Foundation": A static reference for the project's technical landscape. Contains setup,
architecture, tech stack, and coding standards.

When onboarding. When architectural questions arise. For environment setup.

2.2. Execution & Learning Documents
Document

Purpose

When to Use

dev_log.md

The "Session History": A chronological log of development sessions. Captures what was done,
decisions made, and a handoff for the next session.

At the beginning and end of every single coding session. This is the most frequently updated document.

knowledge_base.md

"Institutional Memory": A curated collection of reusable patterns, solutions, and valuable AI
prompts discovered during the project.

When a reusable solution is created. When a particularly effective AI prompt is found.

quality_gates.md

"The Standard": A checklist and dashboard for ensuring quality, from code style and test
coverage to security validation.

Before committing code. During code reviews. Before deploying a new feature.

1. The Cross-Document Linkage System
To connect these documents into a cohesive whole, we will use a standardized reference system.

[PRD-decision:YYYY-MM-DD]: Links to a specific decision in the prd.md.

[IMPL-task:ID]: Links to a task in the implementation_schedule.md.

[LOG:YYYY-MM-DD]: Links to a specific dev_log.md entry.

[KB:PatternName]: Links to a pattern in the knowledge_base.md.

[QG:CheckpointName]: Links to a checkpoint in the quality_gates.md.

1. The Phased Workflow
Phase 0: Idea Validation & Scope Check (1-2 Hours)
Feasibility Audit: Is the idea viable, exciting, and achievable within a reasonable timeframe?

AI Stress Test: Prompt the AI to identify potential failures, hard parts, and simpler alternatives.

Go/No-Go: Create the initial prd.md with a clear, one-sentence goal.

Phase 1: High-Level Planning & Setup (2-3 Hours)
Flesh out prd.md: Define user stories, features, and success metrics.

Create implementation_schedule.md: Plan the first sprint and list backlog items.

Establish project_context.md: Define the initial tech stack, architecture, and standards.

Set up Version Control: Initialize git repository with branch and commit message conventions.

Phase 2: Iterative Development & User Testing (Ongoing)
Session Kickoff:

Review the "Session Handoff" from the last dev_log.md entry.

Review the current tasks in implementation_schedule.md.

Action: Provide the AI with the relevant documents for the day's task.

Development Cycle (per task):

Generate code and tests with AI assistance.

Review and validate AI output.

Run code against quality_gates.md checklists.

User Testing: Integrate feedback loops as defined in the implementation_schedule.md.

Session End:

Update the dev_log.md with a new entry, paying close attention to the "Session Handoff"
section.

Update the implementation_schedule.md with task progress.

Add any new patterns to the knowledge_base.md.

Phase 3: MVP Delivery & Maintenance
Final Review: Ensure all core features from the prd.md are complete and tested.

Deployment: Deploy the MVP.

Retrospective: Review the dev_log.md and implementation_schedule.md to analyze the development process.

1. Automation & Tooling
To enhance efficiency, we can develop helper scripts:

session_context.py: A script that runs at the start of a session to pull the latest handoff
notes, current sprint tasks, and recent decisions into the terminal.

validate_links.py: A pre-commit hook or CI check to ensure that all cross-document references are valid.
