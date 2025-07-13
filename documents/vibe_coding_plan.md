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

*See separate PRD template document*

### 2. IMPLEMENTATION SCHEDULE (`implementation_schedule.md`)

*See separate implementation schedule template with enhanced dependency tracking, risk levels, and rollback plans*

### 3. DEVELOPER LOG (`dev_log.md`)

*See separate dev log template with enhanced session handoff and code review processes*

**Phase 1 Checkpoints:**

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

3. **User Story Format**

   ```markdown
   As a [user type], I want [functionality] so that [benefit/value].

   Acceptance Criteria:
   - [ ] User can [specific action]
   - [ ] System responds with [expected behavior]
   - [ ] Error handling covers [edge cases]
   ```

**Phase 2 Checkpoints:**

- At least 2 potential users have seen the concept
- Core user flow validated (even with paper prototypes)
- Major assumptions tested or documented as risks

---

## Phase 3: Lightweight Architecture & Tech Stack (1-2 hours)

### **Version Control Setup** (15 min)

*See dev_log.md for complete branch naming and commit message standards*

### **Architecture & Stack Selection** (45-60 min)

1. **Stack Rapid-Fire:** Ask AI: "Simplest stack to build [core feature] in Python/JS?"
2. **Component Sketch:** Draft ASCII or text diagram via AI.
3. **Decision Log:**
   - Option A vs. B → Chosen C → Why? (link commit hash)
   - Note reversibility for future pivot

### **Code Review Process Setup** (15 min)

*See dev_log.md for complete AI-assisted review checklist and prompts*

**Security/Ethics Quick Check:** PII handling, license compliance, misuse risk assessment

**Phase 3 Checkpoints:**

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

### **User Testing Integration**

*See implementation_schedule.md for detailed user testing schedule template*

**Multi-AI Tip:** If stuck, swap models (GPT, Claude, Perplexity) on the same prompt and compare.

---

## Phase 5: MVP Delivery & Maintenance

- **MVP Definition:** Core use-case works smoothly
- **AI-Enhanced Testing:** "Generate 10 test cases for [module]."
- **Deployment Lite:** Local or free hosting (Heroku, Vercel, Colab)
- **Sustain Plan:** List monthly health-check tasks
- **CI/CD Pipeline:** GitHub Actions template (`python.yml`/`node.yml`) running tests + linter on every push

**MVP Checklist:**

- All core features implemented and tested
- User testing feedback incorporated
- CI pipeline green
- Security/ethics checklist reviewed
- Monthly maintenance plan in place

---

## Emergency Protocols

### **When Stuck (>2 days)**

1. **AI Model Rotation:** Try different models on the same problem
2. **Scope Reduction:** Can you solve 50% of the problem?
3. **Community Help:** Post specific questions on relevant forums
4. **Mentor Consultation:** Reach out to experienced developers

### **When Motivation Drops**

1. **Quick Win:** Pick smallest possible deliverable
2. **User Feedback:** Show current progress to potential users
3. **Pivot Assessment:** Is the core idea still exciting?
4. **Break Documentation:** Update what you've learned so far

### **When Scope Creeps**

1. **Feature Freeze:** No new features until MVP done
2. **User Story Prioritization:** What's truly essential?
3. **Technical Debt Review:** Are shortcuts causing the creep?
4. **Timeline Reality Check:** Extend deadline or cut features

---

### Operating Principles for Enhanced Vibe-Coding

- **Keep Files Lean:** Only 3 core docs—update them constantly
- **Definition of Done:** Tests pass, lint clean, docs touched, user-tested
- **Short Sprints:** Weekly cycles keep momentum
- **Context Discipline:** Copy/paste only what's relevant
- **AI as Co-Pilot, Not Dictator:** Always validate hallucinations
- **User-Centric:** Test early, test often, pivot when needed
- **Code Quality:** Every commit should improve or maintain quality

Use this blueprint as your adaptable backbone—tweak phases, names, and deliverables to match your personal
rhythm and project scale. Happy vibe-coding! 🚀

---

### Appendix: AI Prompt Library

**Planning:**

- "Draft a PRD for [idea] aimed at a solo developer MVP."
- "What edge cases belong in this PRD?"
- "Write 3-5 user stories for [primary persona] using [core features]"
- "Name 5 ways this could break or be misused."

**Development:**

- "Simplest stack to build [core feature] in Python/JS?"
- "Create tests covering happy path + 3 edge cases for [module]."
- "Generate 10 test cases for [module]."
- "Write a testable module for [feature], include comments and error checks."

**Code Review:**

- "Review this code for security vulnerabilities, focusing on input validation and data sanitization."
- "Analyze this code for performance issues and suggest optimizations."
- "Review this code for bugs, readability issues, and suggest improvements."
- "Suggest additional test cases for this code."

**User Testing:**

- "Design 3 quick user tests for [feature]."
- "What questions should I ask users testing [workflow]?"
- "How can I validate [assumption] with minimal effort?"
- "Create a user testing script for [specific user flow]."

**Architecture:**

- "Design a simple architecture for [system description]."
- "What are the pros and cons of [technology A] vs [technology B] for [use case]?"
- "Create an ASCII diagram showing how [components] interact."
