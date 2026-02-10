import json
import sys
import time
from functools import wraps
from pathlib import Path
from typing import Any, Dict, List

# Add project root to path to import scripts
# We need to find the project root dynamically
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.vibe.state import VibeState
from scripts.vibe.telemetry import TelemetryTracker


def retry_on_failure(retries=3, delay=0.1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    time.sleep(delay * (i + 1))
            raise last_exception

        return wrapper

    return decorator


class StateService:
    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.state = VibeState(project_root)
        self.project_root = project_root

    @retry_on_failure()
    def get_full_state(self) -> Dict[str, Any]:
        """Get the full current state."""
        return self.state.load()

    @retry_on_failure()
    def get_sprint_status(self) -> Dict[str, Any]:
        """Get sprint status."""
        state = self.state.load()
        return state.get("sprint", {})

    @retry_on_failure()
    def get_blackboard(self) -> Dict[str, Any]:
        """Get blackboard data."""
        state = self.state.load()
        return state.get("blackboard", {})

    def get_active_agent(self) -> Dict[str, str]:
        """Determine agent state: idle, thinking, writing."""
        try:
            state = self.state.load()
            status = state.get("sprint.status")

            agent = "idle"
            if status == "executing":
                agent = "codex"
            elif status == "planning":
                agent = "claude"
            elif status == "context":
                agent = "gemini"

            if agent == "idle":
                return {"name": "idle", "state": "idle"}

            # Check session log activity
            log_path_str = state.get("session_log")
            if log_path_str:
                log_path = self.project_root / log_path_str
                if log_path.exists():
                    mtime = log_path.stat().st_mtime
                    lag = time.time() - mtime
                    # If no write in last 15s, assume thinking
                    activity = "thinking" if lag > 15 else "writing"
                    return {"name": agent, "state": activity}

            # Default to writing if no log found (or just started)
            return {"name": agent, "state": "writing"}

        except Exception:
            return {"name": "idle", "state": "idle"}


class TelemetryService:
    def __init__(self, project_root: Path = PROJECT_ROOT):
        self.tracker = TelemetryTracker(project_root)
        self.state = VibeState(project_root)

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get current sprint metrics."""
        try:
            self.state.load()
            return self.state.get_sprint_metrics()
        except Exception:
            return {}

    def get_sprint_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get history of past sprints."""
        # List all telemetry files
        telemetry_dir = self.tracker.telemetry_dir
        if not telemetry_dir.exists():
            return []

        # Get all files first
        files = list(telemetry_dir.glob("*_telemetry.json"))
        # Sort by mtime desc to get recent ones first
        files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        # Take only the most recent 'limit' files
        recent_files = files[:limit]

        reports = []
        for report_file in recent_files:
            try:
                with open(report_file) as f:
                    reports.append(json.load(f))
            except Exception:
                continue

        # Sort by timestamp inside the file to be sure
        return sorted(reports, key=lambda x: x.get("timestamp", ""), reverse=True)
