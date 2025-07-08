#!/usr/bin/env python3
# session_context.py - Gather context for coding session

import datetime
import re


def extract_last_dev_log_entry():
    """Extract the most recent dev log entry."""
    try:
        with open("../documents/dev_log.md") as f:
            content = f.read()

        entries = re.split(r"## \[\d{4}-\d{2}-\d{2}\]", content)
        if len(entries) > 1:
            return entries[1].strip()
        return "No recent dev log entries found."
    except FileNotFoundError:
        return "Dev log file not found."


def extract_sprint_tasks():
    """Extract current sprint tasks from backlog."""
    try:
        with open("../documents/backlog.md") as f:
            content = f.read()

        sprint_match = re.search(r"## ACTIVE SPRINT:.*?(?:##|$)", content, re.DOTALL)
        if sprint_match:
            sprint_content = sprint_match.group(0)
            tasks = re.findall(r"- \[ \] (.*?)$", sprint_content, re.MULTILINE)
            return tasks
        return []
    except FileNotFoundError:
        return []


def extract_recent_decisions():
    """Extract recent decisions from PRD."""
    try:
        with open("../documents/prd.md") as f:
            content = f.read()

        decision_section = re.search(r"## DECISION LOG.*?(?:##|$)", content, re.DOTALL)
        if decision_section:
            decisions = re.findall(
                r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(.*?)\s*\|", decision_section.group(0)
            )
            return decisions[-3:] if decisions else []  # Return last 3 decisions
        return []
    except FileNotFoundError:
        return []


def extract_code_health():
    """Extract code health metrics."""
    metrics = {
        "test_coverage": "Not available",
        "ruff_warnings": "Not available",
        "mutmut_score": "Not available",
    }

    # In a real project, these would be extracted from test reports,
    # linting output, and mutation testing results

    return metrics


def find_cross_references():
    """Find cross-document references that might be relevant."""
    all_references = []

    # In a real project, you would scan through recent entries and
    # extract references using regex patterns

    return all_references


def main():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    print(f"\n{'=' * 50}")
    print(f"VIBE CODING SESSION CONTEXT: {today}")
    print(f"{'=' * 50}\n")

    # Last session handoff
    print("\033[1m🏁 LAST SESSION HANDOFF:\033[0m")
    dev_log = extract_last_dev_log_entry()
    handoff_section = re.search(
        r"### 🏁 SESSION HANDOFF(.*?)(?:###|$)", dev_log, re.DOTALL
    )
    if handoff_section:
        print(handoff_section.group(1).strip())
    else:
        print("No handoff information found.")

    # Current sprint tasks
    print("\n\033[1m📋 CURRENT SPRINT TASKS:\033[0m")
    tasks = extract_sprint_tasks()
    if tasks:
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
    else:
        print("No active sprint tasks found.")

    # Recent decisions
    print("\n\033[1m🤔 RECENT DECISIONS:\033[0m")
    decisions = extract_recent_decisions()
    if decisions:
        for date, decision in decisions:
            print(f"[{date}] {decision}")
    else:
        print("No recent decisions found.")

    # Code health
    print("\n\033[1m🔍 CODE HEALTH:\033[0m")
    health = extract_code_health()
    print(f"Test Coverage: {health['test_coverage']}")
    print(f"Ruff Warnings: {health['ruff_warnings']}")
    print(f"Mutation Score: {health['mutmut_score']}")

    # Cross-references
    print("\n\033[1m🔗 RELEVANT CROSS-REFERENCES:\033[0m")
    refs = find_cross_references()
    if refs:
        for ref in refs:
            print(f"- {ref}")
    else:
        print("No relevant cross-references found.")

    # Set session goals
    print("\n\033[1m🎯 SESSION GOALS (fill in):\033[0m")
    print("1. ")
    print("2. ")
    print("3. ")

    print("\n💡 Start your session by updating the dev_log.md with today's entry.\n")


if __name__ == "__main__":
    main()
