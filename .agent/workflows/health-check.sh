#!/bin/bash
# Health Check Workflow
# Runs pre-commit quality checks: formatting, linting, and tests

set -e  # Exit on first error

echo "🏥 Running health checks..."
echo ""

# Check 1: Code Formatting
echo "📐 Checking code formatting..."
uv run ruff format .
echo "✅ Formatting complete"
echo ""

# Check 2: Linting
echo "🔍 Running linter..."
uv run ruff check .
echo "✅ Linting passed"
echo ""

# Check 3: Tests
echo "🧪 Running tests..."
uv run pytest -q
echo "✅ Tests passed"
echo ""

echo "✨ All health checks passed!"
echo ""
echo "Ready to commit. Next steps:"
echo "  1. Review changes: git status"
echo "  2. Stage files: git add <files>"
echo "  3. Commit: git commit -m 'type: description'"
