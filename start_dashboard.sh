#!/bin/bash
set -e

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🚀 Starting Vibe Dashboard..."
echo "📂 Project Root: $PROJECT_ROOT"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ pv not found. Please install uv."
    exit 1
fi

# Run the FastAPI app using uvicorn
# We use --reload for development
export PYTHONPATH=$PROJECT_ROOT:$PYTHONPATH
uv run uvicorn src.vibe_coding.dashboard.main:app --reload --port 8000 --host 0.0.0.0
