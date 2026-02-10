#!/bin/bash
# Test script for MADE Orchestrator

set -e

echo "🧪 Testing MADE Orchestrator..."
echo ""

# Test 1: Version
echo "Test 1: Version command"
uv run python3 scripts/vibe/made.py version
echo "✅ Version test passed"
echo ""

# Test 2: Status (no active sprint)
echo "Test 2: Status command (no sprint)"
uv run python3 scripts/vibe/made.py status
echo "✅ Status test passed"
echo ""

# Test 3: Help
echo "Test 3: Help command"
uv run python3 scripts/vibe/made.py --help > /dev/null
echo "✅ Help test passed"
echo ""

# Test 4: Sprint help
echo "Test 4: Sprint subcommand help"
uv run python3 scripts/vibe/made.py sprint --help > /dev/null
echo "✅ Sprint help test passed"
echo ""

# Test 5: State file operations
echo "Test 5: State management"
python3 -c "
import sys
sys.path.insert(0, 'scripts')
from vibe.state import VibeState
from pathlib import Path

state = VibeState(Path.cwd())
state.load()
print('State loaded successfully')
state.set('test.value', 'hello')
print('State value set')
assert state.get('test.value') == 'hello', 'State get failed'
print('State value retrieved')
"
echo "✅ State management test passed"
echo ""

echo "🎉 All tests passed!"
