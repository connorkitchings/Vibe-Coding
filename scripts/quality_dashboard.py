#!/usr/bin/env python3
# quality_dashboard.py - Track code health metrics over time

import datetime
import json
import os

# Define quality thresholds
THRESHOLDS = {
    "test_coverage": {"excellent": 90, "good": 80, "warning": 70, "poor": 60},
    "ruff_warnings": {"excellent": 0, "good": 5, "warning": 10, "poor": 20},
    "function_size": {"excellent": 25, "good": 40, "warning": 50, "poor": 60},
    "class_size": {"excellent": 100, "good": 150, "warning": 200, "poor": 250},
    "file_size": {"excellent": 200, "good": 350, "warning": 500, "poor": 600},
    "mutmut_score": {"excellent": 90, "good": 75, "warning": 60, "poor": 50},
}


def get_status_emoji(value, metric, reverse=False):
    """Return emoji based on threshold values."""
    thresholds = THRESHOLDS.get(metric, {})
    if not thresholds:
        return "❓"

    if reverse:
        if value <= thresholds.get("excellent", 0):
            return "🌟"
        elif value <= thresholds.get("good", 0):
            return "✅"
        elif value <= thresholds.get("warning", 0):
            return "⚠️"
        else:
            return "❌"
    else:
        if value >= thresholds.get("excellent", 100):
            return "🌟"
        elif value >= thresholds.get("good", 80):
            return "✅"
        elif value >= thresholds.get("warning", 60):
            return "⚠️"
        else:
            return "❌"


def collect_test_coverage():
    """Collect test coverage metrics."""
    # In a real project, you would parse pytest-cov output or coverage.py data
    # For this template, we'll simulate the data
    return {
        "total": 0,  # Placeholder value
        "modules": {},  # Placeholder for module-specific coverage
    }


def count_ruff_warnings():
    """Count ruff linting warnings."""
    # In a real project, you would run ruff and parse output
    # For this template, we'll simulate the data
    return {
        "total": 0,  # Placeholder value
        "by_type": {},  # Placeholder for warning types
    }


def analyze_code_organization():
    """Analyze code organization metrics."""
    # In a real project, you would analyze actual Python files
    # For this template, we'll simulate the data
    return {
        "function_sizes": {},
        "class_sizes": {},
        "file_sizes": {},
        "avg_function_size": 0,
        "avg_class_size": 0,
        "avg_file_size": 0,
        "max_function_size": 0,
        "max_class_size": 0,
        "max_file_size": 0,
    }


def get_mutation_score():
    """Get mutation testing score."""
    # In a real project, you would parse mutmut output
    # For this template, we'll simulate the data
    return {
        "score": 0,  # Placeholder value
        "killed_mutants": 0,
        "total_mutants": 0,
    }


def save_metrics(metrics):
    """Save metrics to history file."""
    history_file = "../documents/data/quality_history.json"
    os.makedirs(os.path.dirname(history_file), exist_ok=True)

    # Load existing history if available
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file) as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

    # Add new metrics
    history.append(
        {"date": datetime.datetime.now().strftime("%Y-%m-%d"), "metrics": metrics}
    )

    # Save history
    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)


def generate_ascii_chart(history, metric, label, reverse=False):
    """Generate simple ASCII chart for metric history."""
    if not history:
        return f"No history data for {label}"

    values = [entry["metrics"].get(metric, 0) for entry in history]
    dates = [entry["date"] for entry in history]

    if not values:
        return f"No {label} data found in history"

    # Generate simple chart
    chart = f"\n{label} Over Time:\n\n"

    # Find min and max for scaling
    min_val = min(values)
    max_val = max(values)
    range_val = max(max_val - min_val, 1)  # Avoid division by zero

    # Chart height
    height = 10

    # Generate chart rows
    for h in range(height, 0, -1):
        row = "    "
        for val in values:
            normalized = (val - min_val) / range_val
            marker = "█" if normalized * height >= h else " "
            row += marker + " "

        # Add y-axis label every few rows
        if h == height:
            row += f" {max_val}"
        elif h == 1:
            row += f" {min_val}"

        chart += row + "\n"

    # Add x-axis
    chart += "    " + "▔" * (len(values) * 2) + "\n"

    # Add date markers for first and last
    if len(dates) >= 2:
        chart += f"    {dates[0]}{' ' * (len(values) * 2 - len(dates[0]) - len(dates[-1]))}{dates[-1]}\n"

    return chart


def main():
    print("\n📊 VIBE CODING QUALITY DASHBOARD 📊\n")
    print(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Collect metrics
    coverage = collect_test_coverage()
    ruff_warnings = count_ruff_warnings()
    code_org = analyze_code_organization()
    mutation = get_mutation_score()

    # Combine metrics
    metrics = {
        "test_coverage": coverage["total"],
        "ruff_warnings": ruff_warnings["total"],
        "avg_function_size": code_org["avg_function_size"],
        "avg_class_size": code_org["avg_class_size"],
        "avg_file_size": code_org["avg_file_size"],
        "max_function_size": code_org["max_function_size"],
        "max_class_size": code_org["max_class_size"],
        "max_file_size": code_org["max_file_size"],
        "mutmut_score": mutation["score"],
    }

    # Display current metrics
    print("\n🧪 TEST COVERAGE:")
    print(
        f"Overall: {coverage['total']}% {get_status_emoji(coverage['total'], 'test_coverage')}"
    )

    print("\n🔍 CODE QUALITY:")
    print(
        f"Ruff Warnings: {ruff_warnings['total']} {get_status_emoji(ruff_warnings['total'], 'ruff_warnings', reverse=True)}"
    )
    print(
        f"Mutation Score: {mutation['score']}% {get_status_emoji(mutation['score'], 'mutmut_score')}"
    )

    print("\n📏 CODE ORGANIZATION:")
    print(
        f"Avg Function Size: {code_org['avg_function_size']} lines {get_status_emoji(code_org['avg_function_size'], 'function_size', reverse=True)}"
    )
    print(
        f"Avg Class Size: {code_org['avg_class_size']} lines {get_status_emoji(code_org['avg_class_size'], 'class_size', reverse=True)}"
    )
    print(
        f"Avg File Size: {code_org['avg_file_size']} lines {get_status_emoji(code_org['avg_file_size'], 'file_size', reverse=True)}"
    )
    print(
        f"Max Function Size: {code_org['max_function_size']} lines {get_status_emoji(code_org['max_function_size'], 'function_size', reverse=True)}"
    )
    print(
        f"Max Class Size: {code_org['max_class_size']} lines {get_status_emoji(code_org['max_class_size'], 'class_size', reverse=True)}"
    )
    print(
        f"Max File Size: {code_org['max_file_size']} lines {get_status_emoji(code_org['max_file_size'], 'file_size', reverse=True)}"
    )

    # Save metrics for history
    save_metrics(metrics)

    # Load history and generate charts
    history_file = "../documents/data/quality_history.json"
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file) as f:
                history = json.load(f)

            # Show history charts
            print("\n📈 TREND ANALYSIS:")
            print(generate_ascii_chart(history, "test_coverage", "Test Coverage"))
            print(
                generate_ascii_chart(
                    history, "ruff_warnings", "Ruff Warnings", reverse=True
                )
            )
            print(generate_ascii_chart(history, "mutmut_score", "Mutation Score"))
        except (json.JSONDecodeError, FileNotFoundError):
            print("\nNo history data available yet.")
    else:
        print("\nNo history data available yet.")

    print("\n💡 RECOMMENDATIONS:")
    print("- Template mode: Add actual metrics to replace placeholder data")
    print("- Run this script after each sprint to track quality trends")
    print("- Consider adding this to your CI pipeline")


if __name__ == "__main__":
    main()
