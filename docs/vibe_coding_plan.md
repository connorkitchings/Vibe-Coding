# Unified Vibe‑Coding Project Blueprint

A flexible, structured workflow to take any idea from spark to delivery, while preserving creative momentum and AI‑powered efficiency.

---

## Phase 0: Idea Validation & Scope Check

1. **Rapid Feasibility Audit** (5–10 min)
   - **Problem Fit**: Does it solve something you genuinely care about?
   - **MVP Window**: Can you deliver a usable prototype in 2–4 weeks (part‑time)?
   - **Sustained Engagement**: Will you stay excited after week 2?
   - **Learning Benefit**: Does it stretch your skills just enough?

2. **AI‑Driven Stress Test**
   - Prompt AI:
     - “What are the hardest parts of building [idea]?”
     - “What simpler alternatives or pivots exist?”
     - “Name 3 reasons this might fail.”

3. **Go/No‑Go Checklist**
   - Clear MVP defined (1–2 sentences)
   - Can list at least 2 ways to pivot if stuck
   - No "unknown-unknowns" in risk list
   - *Exit Criteria: You can state why you are building this, what success looks like, and why now is the right time.*

---

## Phase 1: High‑Level Planning (Core Docs System)

Use three living files to capture decisions, tasks, and learnings. Store them in your repo’s `/docs` or root folder. (Consider naming: `prd.md`, `backlog.md`, `dev_log.md`.)

### 1. PRODUCT REQUIREMENTS (`prd.md`)

```markdown
PROJECT: [Name]
GOAL: (1–2 sentences)
USERS: [primary persona]
CORE FEATURES:
  - Feature A (must-have)
  - Feature B (must-have)
  - Feature C (nice-to-have)
OUT OF SCOPE:
  - ...
SUCCESS METRICS:
  - Usage criteria
  - Performance targets
```

### 2. TASK BREAKDOWN (`backlog.md`)

```markdown
SPRINT (1 week):
  [ ] Task 1 (2h)
  [ ] Task 2 (4h)
BACKLOG:
  - ...
DONE:
  - [DATE] Completed Task 1: Notes…
BLOCKERS:
  - Task X blocked by [issue]
PARKING LOT:
  - [DATE] Discarded idea: [short note]
```

**Definition of Done:** Each task must have: tests pass, lint clean, docs touched if needed.
**Tip:** Estimate in hours; keep sprints ≤ 1 week.

### 3. IMPLEMENTATION LOG (`dev_log.md`)

```markdown
[YYYY-MM-DD]
WHAT WORKED:
  - ...
WHAT DIDN’T:
  - ...
AI TRICKS:
  - Prompt: “…” → Good response on [topic]
DECISIONS:
  - Chose [library] over [alternative] because… (link commit hash)
NEXT UP:
  - ...
```

**Context Feeding:** At each session start, paste last 2–3 entries into your AI assistant.

---

## Phase 2: Conversational Requirements

- **User Journeys:** Ask AI: “Write 3 user stories for my PRD.”
- **Risk Workshop:** “Name 5 ways this could break or be misused.”
- **Constraint Map:** List what must stay vs. what can flex.

**Exit Criteria:**

- User stories written for each main persona
- Top 3 risks and mitigations listed
- Constraints and flexibilities documented

---

## Phase 3: Lightweight Architecture & Tech Stack

1. **Stack Rapid-Fire:** Ask AI: “Simplest stack to build [core feature] in Python/JS?”
2. **Component Sketch:** Draft ASCII or text diagram via AI.
3. **Decision Log:**
   - Option A vs. B → Chosen C → Why? (link commit hash)
   - Note reversibility for future pivot
   - Security/Ethics Quick Check: PII, license, misuse risk

**Checkpoints:**

- Architecture diagram created
- Stack and key libraries chosen and justified
- Security/ethics checklist reviewed

---

## Phase 4: Iterative AI-Powered Development

For each task:

1. **Session Kickoff:** Feed PRD + last dev_log + current backlog.
2. **Generate & Review:**
   - “Write a testable module for [feature], include comments and error checks.”
   - Run static analysis (ruff/flake8/eslint)
   - Add/update minimal unit test
   - Ensure pre-commit hooks pass
3. **Test & Tweak:** Break it—invalid inputs, edge cases. Ask AI: “Create tests covering happy path + 3 edge cases for [module].”
4. **Log Learnings:** Update dev_log.md with insights.

**Multi-AI Tip:** If stuck, swap models (GPT, Claude, Perplexity) on the same prompt and compare.

---

## Phase 5: MVP Delivery & Maintenance

- **MVP Definition:** Core use-case works smoothly
- **AI-Enhanced Testing:** “Generate 10 test cases for [module].”
- **Deployment Lite:** Local or free hosting (Heroku, Vercel, Colab)
- **Sustain Plan:** List monthly health-check tasks
- **CI/CD:** Set up free GitHub Actions template (`python.yml`/`node.yml`) running tests + linter on every push

**MVP Checklist:**

- All core features implemented and tested
- CI pipeline green
- Security/ethics checklist reviewed
- Monthly maintenance plan in place

---

### Operating Principles for Vibe-Coding

- **Keep Files Lean:** Only 3 core docs—update them constantly
- **Definition of Done:** Tests pass, lint clean, docs touched
- **Short Sprints:** Weekly cycles keep momentum
- **Context Discipline:** Copy/paste only what’s relevant
- **AI as Co-Pilot, Not Dictator:** Always validate hallucinations

Use this blueprint as your adaptable backbone—tweak phases, names, and deliverables to match your personal rhythm and project scale. Happy vibe-coding! 🚀

---

### Appendix: AI Prompt Library

- “Draft a PRD for [idea] aimed at a solo developer MVP.”
- “What edge cases belong in this PRD?”
- “Write 3 user stories for my PRD.”
- “Name 5 ways this could break or be misused.”
- “Simplest stack to build [core feature] in Python/JS?”
- “Create tests covering happy path + 3 edge cases for [module].”
- “Generate 10 test cases for [module].”
