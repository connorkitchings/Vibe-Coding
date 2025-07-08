# Vibe-Coding Quality Gates

This document provides a comprehensive quality validation system for your Vibe Coding projects.
The objective is to maintain high code quality and ensure consistency
across projects while preserving creative momentum.
Use it as a checklist during development and before completing any significant
feature.

## Quick Reference

| Gate | Status Command | Target | Current |
|------|---------------|--------|---------|
| Ruff Linting | `ruff check .` | 0 errors | - |
| Test Coverage | `pytest --cov=src` | ≥80% | - |
| Mutation Score | `mutmut run` | ≥75% | - |
| Docs Updated | Manual check | All relevant | - |

## Checkpoint Validation System

### Pre-Commit Validation

Run these commands before each commit to ensure basic quality:

```bash
# Format code and fix linting issues
ruff check . --fix
ruff format .

# Run tests
pytest

# Check dependency security
uv audit
```

### Feature Completion Checklist

Before marking a feature as complete in the backlog, run through this checklist:

- [ ] All tests pass (`pytest`)
- [ ] Code is properly linted (`ruff check .`)
- [ ] Test coverage meets target (`pytest --cov=src`)
- [ ] Documentation updated as needed:
  - [ ] Docstrings for public functions/classes
  - [ ] README updated if applicable
  - [ ] dev_log.md updated with lessons learned
- [ ] No TODOs left in code (`grep -r "TODO" src/`)
- [ ] Dependencies documented in pyproject.toml

### Sprint Review Quality Metrics

Track these metrics at the end of each sprint:

1. **Code Health Dashboard**

```text
Sprint [YYYY-MM-DD] to [YYYY-MM-DD]
--------------------------------
Test Coverage: XX% (Target: ≥80%)
Ruff Warnings: X (Target: <10)
Mutation Score: XX% (Target: ≥75%)
Docs Updated: Yes/No
```

1. **Technical Debt Tracker**

| Type | Count | Location | Plan to Address |
|------|-------|----------|----------------|
| TODOs | X | `src/module.py:XX` | Sprint X |
| Test Gaps | X | `src/module.py` | Sprint X |
| Complex Functions (>50 lines) | X | `src/module.py:function_name` | Sprint X |

## Code Organization Compliance Tracker

### Size Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Functions (max lines) | ≤50 | - | - |
| Classes (max lines) | ≤200 | - | - |
| Files (max lines) | ≤500 | - | - |
| Line length | ≤100 | - | - |

### Command for Size Analysis

```bash
# Count lines in functions (example with tokei)
tokei -f src/

# Check line length violations
ruff check . --select E501
```

### Automated Organization Compliance Check

Create a script to automatically check compliance with code organization rules:

```python
import os
import ast
import statistics

def analyze_code_organization(directory='src/'):
    """Analyze code for compliance with organization rules."""
    results = {
        'functions': [],
        'classes': [],
        'files': [],
    }

    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith('.py'):
                continue

            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()

            # Count file lines
            file_lines = len(content.splitlines())
            results['files'].append((filepath, file_lines))

            # Parse AST to count function/method and class lines
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_lines = node.end_lineno - node.lineno
                        results['functions'].append((f"{filepath}:{node.name}", func_lines))
                    elif isinstance(node, ast.ClassDef):
                        class_lines = node.end_lineno - node.lineno
                        results['classes'].append((f"{filepath}:{node.name}", class_lines))
            except SyntaxError:
                print(f"Syntax error in {filepath}")

    return results

def print_report(results):
    """Print a compliance report based on analysis results."""
    print("=== CODE ORGANIZATION COMPLIANCE REPORT ===")

    # Function analysis
    functions = results['functions']
    if functions:
        function_lines = [lines for _, lines in functions]
        print(f"\nFUNCTIONS: {len(functions)}")
        print(f"  Average lines: {statistics.mean(function_lines):.1f}")
        print(f"  Max lines: {max(function_lines)} (Target: ≤50)")
        non_compliant = [(name, lines) for name, lines in functions if lines > 50]
        print(f"  Non-compliant: {len(non_compliant)} / {len(functions)}")
        if non_compliant:
            print("  Top offenders:")
            for name, lines in sorted(non_compliant, key=lambda x: x[1], reverse=True)[:5]:
                print(f"    {name}: {lines} lines")

    # Class analysis
    classes = results['classes']
    if classes:
        class_lines = [lines for _, lines in classes]
        print(f"\nCLASSES: {len(classes)}")
        print(f"  Average lines: {statistics.mean(class_lines):.1f}")
        print(f"  Max lines: {max(class_lines)} (Target: ≤200)")
        non_compliant = [(name, lines) for name, lines in classes if lines > 200]
        print(f"  Non-compliant: {len(non_compliant)} / {len(classes)}")
        if non_compliant:
            print("  Top offenders:")
            for name, lines in sorted(non_compliant, key=lambda x: x[1], reverse=True)[:5]:
                print(f"    {name}: {lines} lines")

    # File analysis
    files = results['files']
    if files:
        file_lines = [lines for _, lines in files]
        print(f"\nFILES: {len(files)}")
        print(f"  Average lines: {statistics.mean(file_lines):.1f}")
        print(f"  Max lines: {max(file_lines)} (Target: ≤500)")
        non_compliant = [(name, lines) for name, lines in files if lines > 500]
        print(f"  Non-compliant: {len(non_compliant)} / {len(files)}")
        if non_compliant:
            print("  Top offenders:")
            for name, lines in sorted(non_compliant, key=lambda x: x[1], reverse=True)[:5]:
                print(f"    {name}: {lines} lines")

if __name__ == "__main__":
    results = analyze_code_organization()
    print_report(results)
```

## Development Environment Standardization

### Environment Setup Checklist

- [ ] Python version: 3.11+ confirmed
- [ ] Virtual environment created: `uv venv .venv`
- [ ] Dependencies installed: `uv pip install -r pyproject.toml`
- [ ] Pre-commit hooks installed: `pre-commit install`
- [ ] Security checks: `uv audit` passes
- [ ] VS Code settings configured for project (settings.json)
- [ ] Test suite confirmed working: `pytest`

### VS Code Configuration Template

```json
{
    "python.linting.enabled": true,
    "python.linting.lintOnSave": true,
    "editor.formatOnSave": true,
    "editor.rulers": [100],
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true,
            "source.fixAll": true
        }
    }
}
```

### Project Onboarding Script

```bash
#!/bin/bash
# setup.sh - Standardized environment setup for Vibe-Coding projects

echo "Setting up development environment..."

# Check Python version
python_version=$(python --version 2>&1 | cut -d' ' -f2)
required_version="3.11.0"

# Check if version meets requirement
if [ $(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1) !=
"$required_version" ]; then
    echo "Error: Python $required_version or higher required. Found $python_version"
    echo "Please install the correct Python version and try again."
    exit 1
fi

# Install uv if not available
if ! command -v uv &> /dev/null; then
    echo "Installing uv package manager..."
    pip install uv
fi

# Create virtual environment
echo "Creating virtual environment..."
uv venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
uv pip install -r pyproject.toml

# Install pre-commit hooks
echo "Setting up pre-commit hooks..."
pip install pre-commit
pre-commit install

# Run security audit
echo "Running security audit..."
uv audit

# Create .vscode directory if not exists
if [ ! -d .vscode ]; then
    mkdir .vscode
    echo "Created .vscode directory"
fi

# Create VS Code settings
cat > .vscode/settings.json << EOL
{
    "python.linting.enabled": true,
    "python.linting.lintOnSave": true,
    "editor.formatOnSave": true,
    "editor.rulers": [100],
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true,
            "source.fixAll": true
        }
    }
}
EOL
echo "VS Code settings configured"

# Run initial tests
echo "Running test suite..."
python -m pytest

echo "Environment setup complete!"
echo "Activate with: source .venv/bin/activate"
```

## Continuous Integration Template

```yaml
# .github/workflows/python-test.yml
name: Python Tests

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11']

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install uv
        uv pip install -r pyproject.toml

    - name: Lint with ruff
      run: |
        pip install ruff
        ruff check .
        ruff format . --check

    - name: Test with pytest
      run: |
        pytest --cov=src

    - name: Security audit
      run: |
        uv audit
```

## Quality Monitoring Dashboard

Create a quality dashboard script to track progress over time:

```python
# scripts/quality_dashboard.py
import json
import datetime
import matplotlib.pyplot as plt
import os

def load_history():
    """Load quality metrics history from JSON file."""
    if os.path.exists('quality_history.json'):
        with open('quality_history.json', 'r') as f:
            return json.load(f)
    return {'dates': [], 'coverage': [], 'lint_warnings': [], 'mutation_score': []}

def save_metrics(coverage, lint_warnings, mutation_score):
    """Save current metrics to history."""
    history = load_history()

    today = datetime.datetime.now().strftime('%Y-%m-%d')

    history['dates'].append(today)
    history['coverage'].append(coverage)
    history['lint_warnings'].append(lint_warnings)
    history['mutation_score'].append(mutation_score)

    with open('quality_history.json', 'w') as f:
        json.dump(history, f)

    print(f"Metrics saved for {today}")

def generate_dashboard():
    """Generate visual dashboard of quality metrics over time."""
    history = load_history()

    if not history['dates']:
        print("No quality history available yet.")
        return

    plt.figure(figsize=(12, 8))

    # Coverage plot
    plt.subplot(3, 1, 1)
    plt.plot(history['dates'], history['coverage'], 'b-', marker='o')
    plt.axhline(y=80, color='r', linestyle='--', alpha=0.7)  # Target line
    plt.title('Test Coverage %')
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)

    # Lint warnings plot
    plt.subplot(3, 1, 2)
    plt.plot(history['dates'], history['lint_warnings'], 'r-', marker='o')
    plt.axhline(y=10, color='r', linestyle='--', alpha=0.7)  # Target line
    plt.title('Ruff Warnings Count')
    plt.grid(True, alpha=0.3)

    # Mutation score plot
    plt.subplot(3, 1, 3)
    plt.plot(history['dates'], history['mutation_score'], 'g-', marker='o')
    plt.axhline(y=75, color='r', linestyle='--', alpha=0.7)  # Target line
    plt.title('Mutation Score %')
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('quality_dashboard.png')
    plt.close()

    print("Dashboard generated at quality_dashboard.png")

if __name__ == "__main__":
    # Example usage
    coverage = float(input("Enter current test coverage %: "))
    lint_warnings = int(input("Enter current lint warning count: "))
    mutation_score = float(input("Enter current mutation score %: "))

    save_metrics(coverage, lint_warnings, mutation_score)
    generate_dashboard()
```
