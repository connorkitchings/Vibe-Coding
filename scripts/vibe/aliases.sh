#!/bin/bash
# MADE Orchestrator Shell Aliases
# Source this file: source scripts/vibe/aliases.sh

# Core vibe command
alias vibe="uv run python scripts/vibe/made.py"

# Individual phase commands
alias vibe-sprint="vibe sprint"
alias vibe-status="vibe status"
alias vibe-context="vibe context"
alias vibe-plan="vibe plan"
alias vibe-exec="vibe exec"
alias vibe-verify="vibe verify"
alias vibe-reset="vibe reset"

# Observability commands
alias vibe-blackboard="vibe blackboard"
alias vibe-metrics="vibe metrics"

# Full sprint workflow function
vibe-full-sprint() {
    local objective="$*"
    if [ -z "$objective" ]; then
        echo "Usage: vibe-full-sprint <objective>"
        return 1
    fi

    echo "🚀 Starting full sprint: $objective"
    vibe context && vibe plan && vibe exec --interactive
}

# Quick start function
vibe-quick() {
    local objective="$*"
    if [ -z "$objective" ]; then
        echo "Usage: vibe-quick <objective>"
        return 1
    fi

    vibe sprint start "$objective"
}

# Task execution helper
vibe-task() {
    local task_id="$1"
    if [ -z "$task_id" ]; then
        echo "Usage: vibe-task <task-id>"
        return 1
    fi

    vibe exec --task "$task_id"
}

echo "✅ MADE Orchestrator aliases loaded"
echo ""
echo "Available commands:"
echo "  vibe              - Main CLI"
echo "  vibe-status       - Show sprint status"
echo "  vibe-sprint       - Sprint commands"
echo "  vibe-context      - Run context analysis (Phase 1)"
echo "  vibe-plan         - Run planning (Phase 2)"
echo "  vibe-exec         - Run execution (Phase 3)"
echo "  vibe-verify       - Run verification (Phase 4)"
echo "  vibe-reset        - Reset sprint state"
echo ""
echo "Observability commands:"
echo "  vibe-blackboard   - View agent communications"
echo "  vibe-metrics      - Show efficiency metrics"
echo ""
echo "Workflow functions:"
echo "  vibe-quick <objective>           - Start a new sprint"
echo "  vibe-full-sprint <objective>     - Run complete sprint workflow"
echo "  vibe-task <task-id>              - Execute specific task"
echo ""
