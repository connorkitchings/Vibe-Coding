#!/bin/bash
# Test script for MADE Orchestrator enhancements

set -e

echo "🧪 Testing MADE Orchestrator Enhancements..."
echo ""

# Test 1: Blackboard functionality
echo "Test 1: Blackboard system"
python3 -c "
import sys
sys.path.insert(0, 'scripts')
from vibe.state import VibeState
from pathlib import Path

state = VibeState(Path.cwd())
state.load()

# Test posting to blackboard
state.post_message('test', 'test_message', 'Testing blackboard', 'info')
print('✓ Posted message to blackboard')

state.post_blocker('test', 'task-001', 'Test blocker', 'Test error')
print('✓ Posted blocker to blackboard')

state.post_insight('test', 'Test insight')
print('✓ Posted insight to blackboard')

state.post_question('test', 'Test question?', 'Test context')
print('✓ Posted question to blackboard')

# Verify retrieval
assert len(state.get_unresolved_blockers()) > 0, 'Failed to retrieve blockers'
print('✓ Retrieved unresolved blockers')

assert len(state.get_unanswered_questions()) > 0, 'Failed to retrieve questions'
print('✓ Retrieved unanswered questions')
"
echo "✅ Blackboard test passed"
echo ""

# Test 2: Metrics tracking
echo "Test 2: Metrics system"
python3 -c "
import sys
sys.path.insert(0, 'scripts')
from vibe.state import VibeState
from pathlib import Path

state = VibeState(Path.cwd())
state.load()

# Test metrics recording
state.record_token_usage('gemini', 1000)
print('✓ Recorded token usage')

state.record_agent_invocation('codex')
print('✓ Recorded agent invocation')

state.record_phase_time('test_phase', 123.45)
print('✓ Recorded phase timing')

# Verify retrieval
metrics = state.get_sprint_metrics()
assert 'token_usage' in metrics, 'Missing token usage'
assert 'agent_invocations' in metrics, 'Missing invocations'
print('✓ Retrieved metrics')

# Test task stats
state.add_task({'id': 'test-1', 'status': 'completed'})
state.add_task({'id': 'test-2', 'status': 'pending'})
state.update_task_stats()
stats = state.get('metrics.task_stats')
assert stats['total'] >= 2, 'Task stats incorrect'
print('✓ Task statistics working')
"
echo "✅ Metrics test passed"
echo ""

# Test 3: Telemetry module
echo "Test 3: Telemetry tracker"
python3 -c "
import sys
sys.path.insert(0, 'scripts')
from vibe.telemetry import TelemetryTracker
from vibe.state import VibeState
from pathlib import Path

state = VibeState(Path.cwd())
state.load()
state.start_sprint('Test sprint')

tracker = TelemetryTracker(Path.cwd())
report = tracker._generate_report(state)

assert 'metrics' in report, 'Missing metrics in report'
assert 'efficiency' in report, 'Missing efficiency in report'
assert 'blackboard' in report, 'Missing blackboard in report'
print('✓ Telemetry report generated')

# Test markdown generation
md = tracker.generate_markdown_report(state)
assert 'Token Usage' in md, 'Missing token usage section'
assert 'Efficiency Metrics' in md, 'Missing efficiency section'
print('✓ Markdown report generated')
"
echo "✅ Telemetry test passed"
echo ""

# Test 4: CLI commands
echo "Test 4: New CLI commands"
uv run python3 scripts/vibe/made.py blackboard --help > /dev/null
echo "✓ Blackboard command available"

uv run python3 scripts/vibe/made.py metrics --help > /dev/null
echo "✓ Metrics command available"

uv run python3 scripts/vibe/made.py verify --help > /dev/null
echo "✓ Verify command available"

echo "✅ CLI commands test passed"
echo ""

# Test 5: Orchestrator integration
echo "Test 5: Orchestrator integration"
python3 scripts/orchestrator.py list 2>&1 | grep -q "vibe-blackboard"
echo "✓ vibe-blackboard in orchestrator"

python3 scripts/orchestrator.py list 2>&1 | grep -q "vibe-metrics"
echo "✓ vibe-metrics in orchestrator"

python3 scripts/orchestrator.py list 2>&1 | grep -q "vibe-verify"
echo "✓ vibe-verify in orchestrator"

echo "✅ Orchestrator integration test passed"
echo ""

echo "🎉 All enhancement tests passed!"
echo ""
echo "New features available:"
echo "  • Blackboard system for inter-agent communication"
echo "  • Metrics tracking and telemetry"
echo "  • Verification command (Phase 4)"
echo "  • Enhanced executor prompt with Stop & Ask triggers"
