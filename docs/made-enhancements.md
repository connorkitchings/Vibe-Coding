# MADE Orchestrator Enhancements

## Overview

These enhancements transform MADE from a basic orchestration tool into a production-grade multi-agent system with observability, inter-agent communication, and quality controls.

## 1. The Blackboard System 📋

### Problem Solved
Agents need to communicate blockers, insights, and questions without just updating task status.

### Implementation

The blackboard provides four communication channels:

```python
# Post a blocker (e.g., Codex can't install a dependency)
state.post_blocker(
    agent="codex",
    task_id="task-001",
    description="Cannot install numpy>=2.0",
    error="Package not found in PyPI"
)

# Post a question (e.g., unclear requirements)
state.post_question(
    agent="codex",
    question="Should we use JWT or session-based auth?",
    context="Plan.md mentions 'authentication' but not specifics"
)

# Post an insight (e.g., discovered pattern)
state.post_insight(
    agent="gemini",
    insight="Repository uses factory pattern extensively in services/"
)

# Post a message (general communication)
state.post_message(
    agent="claude",
    message_type="warning",
    content="Task complexity higher than estimated",
    severity="warning"
)
```

### Usage

View the blackboard:
```bash
# View all communications
vibe blackboard

# View only blockers
vibe blackboard --type blockers

# View unanswered questions
vibe blackboard --type questions
```

### State Structure

```json
{
  "blackboard": {
    "messages": [
      {
        "timestamp": "2026-02-10T14:30:00",
        "agent": "codex",
        "type": "info",
        "content": "Starting task execution",
        "severity": "info"
      }
    ],
    "blockers": [
      {
        "timestamp": "2026-02-10T14:35:00",
        "agent": "codex",
        "task_id": "task-001",
        "description": "Missing dependency",
        "error": "ModuleNotFoundError: No module named 'pandas'",
        "resolved": false
      }
    ],
    "insights": [
      {
        "timestamp": "2026-02-10T14:20:00",
        "agent": "gemini",
        "insight": "Codebase follows DDD architecture"
      }
    ],
    "questions": [
      {
        "timestamp": "2026-02-10T14:25:00",
        "agent": "codex",
        "question": "Use async or sync database calls?",
        "context": "Plan doesn't specify",
        "answered": false
      }
    ]
  }
}
```

### Benefits

1. **Architect sees problems** - Blockers are visible for re-planning
2. **Context for next phase** - Insights inform future decisions
3. **Async communication** - Agents don't need to be running simultaneously
4. **Audit trail** - Full history of inter-agent communication

## 2. Observability Metrics (The Vibe Score) 📊

### Problem Solved
Need to measure if multi-agent approach is actually more efficient.

### Metrics Tracked

1. **Token Usage**
   - Per agent (Gemini, Claude, Codex)
   - Total tokens consumed
   - Tokens per task

2. **Task Statistics**
   - Total tasks
   - Completed, failed, pending
   - Success rate percentage

3. **Phase Timing**
   - Duration of each phase
   - Time per task
   - Total sprint duration

4. **Agent Efficiency**
   - Invocations per agent
   - Tasks per agent run
   - Cost per task

### Usage

View current sprint metrics:
```bash
vibe metrics
```

Example output:
```markdown
# Sprint Efficiency Report

**Sprint ID:** sprint-2026-02-10-143052
**Objective:** Add user authentication
**Status:** completed

## Token Usage

| Agent   | Tokens  | Invocations | Tokens/Invocation |
|---------|---------|-------------|-------------------|
| Gemini  | 45,000  | 1           | 45,000           |
| Claude  | 8,500   | 1           | 8,500            |
| Codex   | 12,300  | 3           | 4,100            |
| **Total** | **65,800** | - | - |

## Task Statistics

- **Total Tasks:** 5
- **Completed:** 4
- **Failed:** 1
- **Success Rate:** 80.0%

## Efficiency Metrics

- **Estimated Cost:** $0.13
- **Cost per Task:** $0.03
- **Tokens per Task:** 16,450
- **Tasks per Codex Run:** 1.33

## Phase Timing

- **Context Analysis:** 2m 15s
- **Planning:** 45s
- **Execution:** 8m 30s
```

### Telemetry Storage

Metrics are saved to `session_logs/telemetry/`:

```
session_logs/telemetry/
├── sprint-2026-02-10-143052_telemetry.json
└── sprint-2026-02-10-150331_telemetry.json
```

### Comparison Analysis

Compare multiple sprints:
```python
from vibe.telemetry import TelemetryTracker

tracker = TelemetryTracker(project_root)
comparison = tracker.compare_sprints([
    "sprint-2026-02-10-143052",
    "sprint-2026-02-10-150331"
])

# Shows averages:
# - avg_cost_per_sprint
# - avg_tokens_per_sprint
# - avg_success_rate
```

### Benefits

1. **Cost tracking** - Know what sprints cost in API usage
2. **Agent comparison** - See which agent is most efficient
3. **Process improvement** - Identify bottlenecks
4. **ROI measurement** - Prove multi-agent value

## 3. The Verification Phase (Phase 4) ✅

### Problem Solved
Code runs and tests pass, but does it match the architectural intent?

### Implementation

The verify command generates an architectural review prompt:

```bash
vibe verify
```

This creates a prompt for Claude (the Architect) to:
1. Review git diff against original PLAN.md
2. Check architectural intent maintained
3. Verify pattern consistency
4. Identify technical debt
5. Suggest improvements

### Verification Checklist

```markdown
### Verification Report
- [ ] Architectural intent maintained
- [ ] Patterns consistent
- [ ] Scope appropriate
- [ ] No critical technical debt

### Issues Found
[List deviations]

### Recommendations
[Improvements needed]
```

### Usage in Sprint

Complete 4-phase workflow:
```bash
vibe context   # Phase 1: Context
vibe plan      # Phase 2: Planning
vibe exec      # Phase 3: Execution
vibe verify    # Phase 4: Verification
```

### Benefits

1. **Catches architectural drift** - Code works but violates patterns
2. **Quality gate** - Human review of AI-generated code
3. **Learning loop** - Insights feed back into future sprints
4. **Documentation** - Verification report explains decisions

## 4. Stop & Ask Trigger (Hallucination Prevention) 🚨

### Problem Solved
Autonomous executors can get stuck in "fix-the-fix-that-fixes-the-fix" loops, wasting tokens.

### Implementation

The executor prompt now includes explicit stop conditions:

```markdown
### 🚨 STOP & ASK TRIGGER

**If any of these conditions occur, STOP and post to blackboard:**

1. **Test Failure Loop** - Test fails 3 times with different fixes
   → Post BLOCKER, EXIT execution

2. **Dependency Issues** - Can't resolve dependency after 2 attempts
   → Post BLOCKER with error, EXIT

3. **Unclear Requirements** - Acceptance criteria ambiguous
   → Post QUESTION, PAUSE

4. **Architectural Conflict** - Implementation conflicts with patterns
   → Post INSIGHT, PAUSE for review
```

### How It Works

When Codex hits a trigger:

1. Updates `.vibe_state.json` directly:
```json
{
  "blackboard": {
    "blockers": [{
      "agent": "codex",
      "task_id": "task-003",
      "description": "Test fails 3 times: test_auth_invalid_token",
      "error": "AssertionError: Expected 401, got 500"
    }]
  }
}
```

2. Exits execution cleanly
3. Architect sees blocker on next `vibe status` or `vibe blackboard`
4. Can re-plan approach in PLAN.md
5. Resume with `vibe exec --task task-003`

### Benefits

1. **Prevents token waste** - Stops before spending 50k tokens on loops
2. **Human intervention** - Complex problems need human insight
3. **Better debugging** - Clear error context for architect
4. **Graceful degradation** - System doesn't fail, it pauses

### Example Scenario

```
❌ Task failed 3 times: test_authentication
🚨 STOP & ASK triggered!
📋 Posted blocker to blackboard
⏸️  Execution paused

Run 'vibe blackboard' to see the blocker
Run 'vibe verify' to review implementation
```

## Integration with Existing System

All enhancements integrate seamlessly:

### State File (`.vibe_state.json`)

```json
{
  "version": "1.0",
  "sprint": {...},
  "context": {...},
  "plan": {...},
  "blackboard": {        // ← NEW
    "messages": [],
    "blockers": [],
    "insights": [],
    "questions": []
  },
  "metrics": {           // ← NEW
    "token_usage": {...},
    "task_stats": {...},
    "phase_times": {},
    "agent_invocations": {...}
  }
}
```

### CLI Commands

```bash
vibe status        # Shows unresolved blockers/questions
vibe blackboard    # View agent communications
vibe metrics       # Show efficiency report
vibe verify        # Run architectural verification
```

### Aliases

```bash
vibe-blackboard    # Quick access to blackboard
vibe-metrics       # Quick metrics view
vibe-verify        # Quick verification
```

### Orchestrator

```bash
python scripts/orchestrator.py vibe-blackboard
python scripts/orchestrator.py vibe-metrics
```

## Workflow Examples

### Complete Sprint with Observability

```bash
# Start sprint
vibe sprint start "Add API caching"

# Phase 1: Context (Gemini analyzes)
vibe context
# ⏱️  Duration: 2m 15s
# 📊 Tokens: 45,000

# Phase 2: Plan (Claude designs)
vibe plan
# Create PLAN.md based on prompt
vibe plan --load PLAN.md
# 📊 Tokens: 8,500

# Phase 3: Execute (Codex implements)
vibe exec --interactive
# Task 1: ✅ Completed (1m 30s, 4,100 tokens)
# Task 2: ❌ Failed - BLOCKER posted
#   → "Redis connection string not in config"

# Check blackboard
vibe blackboard --type blockers
# Shows: Missing Redis config

# Fix config, resume
vibe exec --task task-002
# Task 2: ✅ Completed

# Phase 4: Verify (Claude reviews)
vibe verify
# Reviews implementation against PLAN.md

# Check final metrics
vibe metrics
# Cost: $0.13
# Success rate: 100%
# Tokens: 65,800
```

### Handling Blockers

```bash
# During execution, Codex hits a blocker
vibe exec
# 🚨 STOP & ASK: Test failure loop detected
# 📋 Blocker posted to blackboard

# View blocker
vibe blackboard --type blockers
# [CODEX] UNRESOLVED
#   Task: task-003
#   Description: Test fails 3 times
#   Error: AssertionError in test_caching

# Architect reviews
vibe verify
# Identifies: Caching logic conflicts with existing pattern

# Update PLAN.md with revised approach
# Resume execution
vibe exec --task task-003
# ✅ Completed with revised approach
```

### Sprint Efficiency Analysis

```bash
# After multiple sprints
vibe metrics

# Compare sprints
python3 -c "
from vibe.telemetry import TelemetryTracker
from pathlib import Path

tracker = TelemetryTracker(Path.cwd())
comparison = tracker.compare_sprints([
    'sprint-2026-02-10-143052',
    'sprint-2026-02-10-150331',
    'sprint-2026-02-10-153421'
])

print('Average cost per sprint:', comparison['averages']['avg_cost_per_sprint'])
print('Average success rate:', comparison['averages']['avg_success_rate'])
"

# Result shows:
# - Gemini context analysis: ~$0.09/sprint
# - Claude planning: ~$0.02/sprint
# - Codex execution: ~$0.03/task
# - Overall efficiency improving over time
```

## Testing

Run enhancement tests:
```bash
bash scripts/vibe/test_enhancements.sh
```

Verifies:
- ✅ Blackboard posting/retrieval
- ✅ Metrics tracking
- ✅ Telemetry generation
- ✅ CLI commands
- ✅ Orchestrator integration

## API Reference

### VibeState Methods

```python
# Blackboard
state.post_message(agent, type, content, severity)
state.post_blocker(agent, task_id, description, error)
state.post_insight(agent, insight)
state.post_question(agent, question, context)
state.get_unresolved_blockers() -> List[Dict]
state.get_unanswered_questions() -> List[Dict]
state.resolve_blocker(index, resolution)

# Metrics
state.record_token_usage(agent, tokens)
state.record_agent_invocation(agent)
state.record_phase_time(phase, duration_seconds)
state.update_task_stats()
state.get_sprint_metrics() -> Dict
```

### TelemetryTracker Methods

```python
tracker = TelemetryTracker(project_root)

# Generate reports
tracker.save_sprint_report(state) -> Path
tracker.generate_markdown_report(state) -> str

# Compare sprints
tracker.compare_sprints(sprint_ids) -> Dict
```

## Best Practices

1. **Check blackboard regularly**
   ```bash
   vibe-status  # Shows blocker/question count
   ```

2. **Review metrics after each sprint**
   ```bash
   vibe-metrics
   ```

3. **Run verification before closing sprint**
   ```bash
   vibe-verify
   ```

4. **Address blockers before next phase**
   ```bash
   vibe blackboard --type blockers
   # Fix issues
   # Resume execution
   ```

5. **Track cost trends**
   ```bash
   # Save telemetry for each sprint
   vibe metrics  # Press 'y' to save
   ```

## Future Enhancements

Based on these foundations:

- [ ] **Auto-resolution** - AI suggests blocker resolutions
- [ ] **Cost budgets** - Halt sprint if token budget exceeded
- [ ] **Learning loops** - Feed metrics back into planning
- [ ] **Parallel execution** - Run independent tasks concurrently
- [ ] **Agent coordination** - Multiple Codex instances for different tasks
- [ ] **Quality gates** - Auto-fail if success rate < threshold
- [ ] **Anomaly detection** - Flag unusual token usage patterns

## Summary

These enhancements provide:

✅ **Observability** - Know what's happening and why
✅ **Communication** - Agents signal problems clearly
✅ **Quality Control** - Verification prevents drift
✅ **Cost Tracking** - Measure efficiency objectively
✅ **Reliability** - Stop & Ask prevents runaway failures

The result: A production-grade multi-agent orchestration system with the observability and controls needed for real-world usage.
