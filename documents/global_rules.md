# Enhanced Vibe‑Coding Project Blueprint

A flexible, structured workflow to take any idea from spark to delivery,
while preserving creative momentum and AI-powered efficiency.

---

## Phase 0: Idea Validation & Scope Check

1. **Rapid Feasibility Audit** (5–10 min)
   - **Problem Fit**: Does it solve something you genuinely care about?
   - **MVP Window**: Can you deliver a usable prototype in 2–4 weeks (part‑time)?
   - **Sustained Engagement**: Will you stay excited after week 2?
   - **Learning Benefit**: Does it stretch your skills just enough?

2. **AI‑Driven Stress Test**
   - Prompt AI:
     - "What are the hardest parts of building [idea]?"
     - "What simpler alternatives or pivots exist?"
     - "Name 3 reasons this might fail."

3. **Go/No‑Go Checklist**
   - Clear MVP defined (1–2 sentences)
   - Can list at least 2 ways to pivot if stuck
   - No "unknown-unknowns" in risk list
   - *Exit Criteria: You can state why you are building this, what success looks like,
     and why now is the right time.*

---

## Phase 1: High‑Level Planning (Core Docs System)

Use three living files—PRD, implementation schedule, and dev log—to capture decisions, tasks, and learnings.
Place them in `/docs` or the repo root (`prd.md`, `implementation_schedule.md`, `dev_log.md`).

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

### 2. ENHANCED IMPLEMENTATION SCHEDULE (`implementation_schedule.md`)

```markdown
| ID | Deliverable | Owner | Est (h) | Dependencies | Risk | Start | End | Status | DoD | Rollback |
|----|-------------|-------|---------|--------------|------|-------|-----|--------|-----|----------|
| 1  | MVP endpoint | @dev | 4 | - | L | 2025-07-15 | 2025-07-15 | ⬜ Todo | Tests pass, API docs updated | Use mock data |
| 2  | UI stub      | @dev | 6 | ID:1 | M | 2025-07-15 | 2025-07-16 | ⬜ Todo | Components render, basic interactions work | Static mockup |
| 3  | User test 1  | @dev | 2 | ID:2 | L | 2025-07-16 | 2025-07-16 | ⬜ Todo | 3 users test core flow, feedback documented | Skip if timeline tight |

Legend: ⬜ Todo · 🔄 In-Progress · ✅ Done · ⏸ Blocked
Risk: H(igh) · M(edium) · L(ow)
```

**Definition of Done (Global):** Tests pass, lint clean, docs touched if needed, security checklist reviewed.
**Tip:** Estimate in hours; keep sprints ≤ 1 week.

### 3. ENHANCED IMPLEMENTATION LOG (`dev_log.md`)

```markdown
[YYYY-MM-DD]

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
```

**Checkpoints:**

- User stories written for each main persona
- Top 3 risks and mitigations listed
- Data privacy/PII handling requirements documented
- Constraints and flexibilities documented

---

## Phase 2: User Story Validation (30-60 min)

1. **Story Generation** (AI-assisted)
   - "Write 3-5 user stories for [primary persona] using [core features]"
   - Include acceptance criteria for each story
   - Prioritize by user impact and development effort

2. **Assumption Testing**
   - List 3 biggest assumptions about user behavior
   - Design quick validation methods (surveys, conversations, mockups)
   - Document findings in PRD

3. **Validation Checkpoints**
   - At least 2 potential users have seen the concept
   - Core user flow validated (even with paper prototypes)
   - Major assumptions tested or documented as risks

---

## Phase 3: Lightweight Architecture & Tech Stack (1-2 hours)

### **Version Control Setup** (15 min)

```bash
# Branch naming convention
feature/user-auth
bugfix/login-validation
hotfix/security-patch

# Commit message format
feat: add user authentication endpoint
fix: resolve login validation bug
docs: update API documentation
test: add user registration tests
```

### **Architecture & Stack Selection** (45-60 min)

1. **Stack Rapid-Fire:** Ask AI: "Simplest stack to build [core feature] in Python/JS?"
2. **Component Sketch:** Draft ASCII or text diagram via AI.
3. **Decision Log:**
   - Option A vs. B → Chosen C → Why? (link commit hash)
   - Note reversibility for future pivot

### **Code Review Process Setup** (15 min)

Even for solo projects:

- **AI-Assisted Review:** "Review this code for bugs, performance issues, and style"
- **Checklist Review:** Security, error handling, test coverage
- **Future Self Review:** Comment unclear code immediately

**Security/Ethics Quick Check:** PII handling, license compliance, misuse risk assessment

**Checkpoints:**

- Architecture diagram created
- Stack and key libraries chosen and justified
- Security/ethics checklist reviewed
- Git workflow established
- Code review process defined

---

## Phase 4: Iterative AI-Powered Development with User Testing

### **Development Cycle** (per task)

1. **Session Kickoff:** Feed PRD + last dev_log + current backlog.
2. **Generate & Review:**
   - "Write a testable module for [feature], include comments and error checks."
   - Run static analysis (ruff/flake8/eslint)
   - Add/update minimal unit test
   - AI code review: "Review this code for bugs, performance issues, and style"
   - Ensure pre-commit hooks pass
3. **Test & Tweak:** Break it—invalid inputs, edge cases. Ask AI:
   "Create tests covering happy path + 3 edge cases for [module]."
4. **Log Learnings:** Update dev_log.md with insights.

### **User Testing Checkpoints**

**After Core Features (Week 1):**

- **Quick User Test:** 2-3 users try core flow
- **Feedback Collection:** What's confusing? What's missing?
- **Iteration:** Fix critical usability issues

**Mid-Development (Week 2):**

- **Feature Validation:** Test new features with 3-5 users
- **A/B Test Key Decisions:** UI layouts, feature priorities
- **Pivot Assessment:** Are we building the right thing?

**Pre-Launch (Week 3):**

- **End-to-End User Testing:** Full user journey
- **Edge Case Testing:** Error scenarios, edge cases
- **Polish Based on Feedback:** Final UX improvements

### **Testing Integration**

```markdown
# Add to implementation_schedule.md
| ID | Deliverable | Type | Users | Success Criteria |
|----|-------------|------|-------|------------------|
| 3  | Core flow test | Usability | 3 | Users complete signup→action in <2 min |
| 7  | Feature validation | A/B Test | 5 | 80% prefer new UI layout |
| 12 | Pre-launch test | End-to-end | 5 | <1 critical bug per user session |
```

**Multi-AI Tip:** If stuck, swap models (GPT, Claude, Perplexity) on the same prompt and compare.

---

## Phase 5: MVP Delivery & Maintenance

- **MVP Definition:** Core use-case works smoothly
- **AI-Enhanced Testing:** "Generate 10 test cases for [module]."
- **Deployment Lite:** Local or free hosting (Heroku, Vercel, Colab)
- **Sustain Plan:** List monthly health-check tasks
- **CI/CD Pipeline:** GitHub Actions template (`python.yml`/`node.yml`) running tests + linter on
every push

**MVP Checklist:**

- All core features implemented and tested
- User testing feedback incorporated
- CI pipeline green
- Security/ethics checklist reviewed
- Monthly maintenance plan in place

---

### Operating Principles for Vibe-Coding

- **Keep Files Lean:** Only 3 core docs—update them constantly
- **Definition of Done:** Tests pass, lint clean, docs touched, user-tested
- **Short Sprints:** Weekly cycles keep momentum
- **Context Discipline:** Copy/paste only what's relevant
- **AI as Co-Pilot, Not Dictator:** Always validate hallucinations
- **User-Centric:** Test early, test often, pivot when needed

Use this blueprint as your adaptable backbone—tweak phases, names, and deliverables to match your personal
rhythm and project scale. Happy vibe-coding! 🚀

---

### Appendix: AI Prompt Library

**Planning:**

- "Draft a PRD for [idea] aimed at a solo developer MVP."
- "What edge cases belong in this PRD?"
- "Write 3 user stories for my PRD."
- "Name 5 ways this could break or be misused."

**Development:**

- "Simplest stack to build [core feature] in Python/JS?"
- "Create tests covering happy path + 3 edge cases for [module]."
- "Generate 10 test cases for [module]."
- "Review this code for bugs, performance issues, and style."

**User Testing:**

- "Design 3 quick user tests for [feature]."
- "What questions should I ask users testing [workflow]?"
- "How can I validate [assumption] with minimal effort?"

**Code Review:**

- "Review this code for security vulnerabilities."
- "Suggest improvements for code readability and maintainability."
- "Identify potential performance bottlenecks in this code."
