# Enhanced Documentation System

This document proposes improvements to the current three-document system (PRD, backlog,
dev_log) to create a more integrated, contextual approach to project documentation.

## Current System Overview

The existing three-document system provides a solid foundation:

- **PRD**: Product requirements and high-level goals
- **Backlog**: Task tracking and sprint management
- **Dev Log**: Session records and implementation notes

## Enhanced System Architecture

### Core Documents (Existing)

1. **PRD** - Strategy & Vision
   - Project goals and requirements
   - Visual system diagrams
   - Decision tracking table
   - Version history

2. **Backlog** - Execution & Planning
   - Sprint planning and tracking
   - Task breakdown with estimates
   - Session continuity notes
   - Retrospective data

3. **Dev Log** - Learning & Context
   - Session state tracking
   - Implementation insights
   - Code health metrics
   - Session handoffs

### New Integration Documents

1. **Knowledge Base** - Institutional Memory
   - Reusable patterns catalog
   - Technical solutions library
   - AI prompt collection
   - Monthly retrospectives

2. **Quality Gates** - Standards & Compliance
   - Checkpoint validation system
   - Code organization tracking
   - Environment standardization
   - Quality metrics dashboard

## Cross-Document Linkage System

The key improvement is explicit linkage between documents using a consistent reference system:

```text
[PRD-decision:YYYY-MM-DD] - Reference to decision in PRD
[BL-task:TaskID] - Reference to backlog task
[DL:YYYY-MM-DD] - Reference to dev log entry
[KB:PatternName] - Reference to knowledge base pattern
[QG:CheckpointName] - Reference to quality gate checkpoint
```

### Example Cross-Document Flow

1. **Product Decision** → Record in PRD with `[PRD-decision:2025-07-08]`
2. **Task Creation** → Create in backlog with reference `[PRD-decision:2025-07-08]`
3. **Implementation** → Note in dev log with `[BL-task:TaskID]`
4. **Pattern Discovery** → Document in knowledge base with `[DL:2025-07-08]`
5. **Quality Validation** → Log in quality gates with `[KB:PatternName]`

## Digital Integration Options

Consider these lightweight tools to enhance document connectivity:

1. **VS Code Workspace Integration**:

   ```json
   // .vscode/vibe-coding.code-workspace
   {
     "folders": [
       { "path": "." }
     ],
     "settings": {
       "markdown.links.openLocation": "beside",
       "markdown.extension.toc.levels": "2..3",
       "workbench.editor.enablePreview": false
     },
     "launch": {
       "configurations": [
         {
           "name": "Generate Quality Dashboard",
           "type": "python",
           "request": "launch",
           "program": "${workspaceFolder}/scripts/quality_dashboard.py"
         }
       ]
     }
   }
   ```

1. **Document Index File**:
   Create an `index.md` that serves as a central hub linking to all documentation with context.

1. **Obsidian/Foam Integration**:
   Consider using Obsidian or Foam VS Code extension for visual graph relationships between documents.

## Enhanced Session Workflow

### Session Start Protocol

1. Open `index.md` dashboard
2. Review last session handoff in `dev_log.md`
3. Check active sprint in `backlog.md`
4. Verify quality metrics in `quality_gates.md`
5. Set session goals based on priorities

### Mid-Session Context Switches

When switching context during a session:

1. Add quick handoff note in `dev_log.md` with `[BL-task:CurrentTask]`
2. Document any insights in `knowledge_base.md` if applicable
3. Update task status in `backlog.md`

### Session End Protocol

1. Complete `dev_log.md` entry with full handoff notes
2. Update `backlog.md` with progress and next steps
3. If completing a feature, verify quality gates in `quality_gates.md`
4. If applicable, update `knowledge_base.md` with patterns
5. If needed, update `PRD.md` with any decision changes

## Proposed Document Integration System

```ascii
┌─────────────────────────┐       ┌─────────────────────────┐
│                         │       │                         │
│        PRD.md           │◄─────►│       backlog.md        │
│    (What & Why)         │       │     (When & Who)        │
│                         │       │                         │
└───────────┬─────────────┘       └───────────┬─────────────┘
            │                                 │
            │                                 │
            ▼                                 ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│                         │       │                         │
│     knowledge_base.md   │◄─────►│       dev_log.md        │
│    (Patterns & Wisdom)  │       │     (How & Details)     │
│                         │       │                         │
└───────────┬─────────────┘       └───────────┬─────────────┘
            │                                 │
            │                                 │
            └───────────────┬────────────────┘
                            │
                            ▼
                ┌─────────────────────────┐
                │                         │
                │     quality_gates.md    │
                │     (Validation)        │
                │                         │
                └─────────────────────────┘
```

## Automation Opportunities

1. **Session Context Script**

Create a script to automatically gather context at session start:

```python
#!/usr/bin/env python3
# session_context.py - Gather context for coding session

import os
import datetime
import re
from collections import defaultdict

def extract_last_dev_log_entry():
    """Extract the most recent dev log entry."""
    with open('documents/dev_log.md', 'r') as f:
        content = f.read()

    entries = re.split(r'## \[\d{4}-\d{2}-\d{2}\]', content)
    if len(entries) > 1:
        return entries[1].strip()
    return "No recent dev log entries found."

def extract_sprint_tasks():
    """Extract current sprint tasks from backlog."""
    with open('documents/backlog.md', 'r') as f:
        content = f.read()

    sprint_match = re.search(r'## ACTIVE SPRINT:.*?## ', content, re.DOTALL)
    if sprint_match:
        sprint_content = sprint_match.group(0)
        tasks = re.findall(r'- \[ \] (.*?)$', sprint_content, re.MULTILINE)
        return tasks
    return []

def extract_recent_decisions():
    """Extract recent decisions from PRD."""
    with open('documents/prd.md', 'r') as f:
        content = f.read()

    decision_section = re.search(r'## DECISION LOG.*?(?:##|$)', content, re.DOTALL)
    if decision_section:
        decisions = re.findall(r'\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(.*?)\s*\|',
                               decision_section.group(0))
        return decisions[-3:] if decisions else []  # Return last 3 decisions
    return []

def main():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    print(f"\n=== VIBE CODING SESSION CONTEXT: {today} ===\n")

    # Last session handoff
    print("LAST SESSION HANDOFF:")
    dev_log = extract_last_dev_log_entry()
    handoff_section = re.search(r'### 🏁 SESSION HANDOFF(.*?)###', dev_log, re.DOTALL)
    if handoff_section:
        print(handoff_section.group(1).strip())
    else:
        print("No handoff information found.")

    # Current sprint tasks
    print("\nCURRENT SPRINT TASKS:")
    tasks = extract_sprint_tasks()
    if tasks:
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
    else:
        print("No active sprint tasks found.")

    # Recent decisions
    print("\nRECENT DECISIONS:")
    decisions = extract_recent_decisions()
    if decisions:
        for date, decision in decisions:
            print(f"[{date}] {decision}")
    else:
        print("No recent decisions found.")

    # Code health
    print("\nCODE HEALTH:")
    print("Run 'python scripts/code_health.py' for detailed report")

    print("\n=== SESSION GOALS ===")
    print("1. ")
    print("2. ")
    print("3. ")

if __name__ == "__main__":
    main()
```

1. **Documentation Linkage Validator**

Create a script to verify cross-document references:

```python
#!/usr/bin/env python3
# validate_links.py - Check cross-document references

import os
import re
import sys
from collections import defaultdict

def extract_references(content):
    """Extract all references from content."""
    patterns = {
        'prd': r'\[PRD-decision:(\d{4}-\d{2}-\d{2})\]',
        'backlog': r'\[BL-task:([A-Za-z0-9-]+)\]',
        'devlog': r'\[DL:(\d{4}-\d{2}-\d{2})\]',
        'kb': r'\[KB:([A-Za-z0-9-]+)\]',
        'qg': r'\[QG:([A-Za-z0-9-]+)\]'
    }

    refs = {}
    for ref_type, pattern in patterns.items():
        refs[ref_type] = re.findall(pattern, content)

    return refs

def validate_references():
    """Validate all cross-document references."""
    doc_paths = {
        'prd': 'documents/prd.md',
        'backlog': 'documents/backlog.md',
        'devlog': 'documents/dev_log.md',
        'kb': 'documents/knowledge_base.md',
        'qg': 'documents/quality_gates.md'
    }

    # Read all documents
    docs = {}
    for doc_type, path in doc_paths.items():
        try:
            with open(path, 'r') as f:
                docs[doc_type] = f.read()
        except FileNotFoundError:
            print(f"Warning: {path} not found")
            docs[doc_type] = ""

    # Extract references from each document
    references = {}
    for doc_type, content in docs.items():
        references[doc_type] = extract_references(content)

    # Validate references
    invalid_refs = defaultdict(list)

    # PRD decisions referenced in other docs should exist in PRD
    prd_decisions = set(re.findall(r'\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([^|]+)\s*\|', docs['prd']))
    for doc_type, refs in references.items():
        if doc_type != 'prd':
            for date in refs.get('prd', []):
                if date not in [d for d, _ in prd_decisions]:
                    invalid_refs[doc_type].append(f"PRD-decision:{date}")

    # Backlog tasks referenced should exist in backlog
    backlog_tasks = set(re.findall(r'- \[ \] \*\*\[.*?\]\*\*: (.*?) \(', docs['backlog']))
    for doc_type, refs in references.items():
        if doc_type != 'backlog':
            for task in refs.get('backlog', []):
                if task not in backlog_tasks:
                    invalid_refs[doc_type].append(f"BL-task:{task}")

    # Dev log dates referenced should exist in dev log
    devlog_dates = set(re.findall(r'## \[(\d{4}-\d{2}-\d{2})\]', docs['devlog']))
    for doc_type, refs in references.items():
        if doc_type != 'devlog':
            for date in refs.get('devlog', []):
                if date not in devlog_dates:
                    invalid_refs[doc_type].append(f"DL:{date}")

    # KB patterns referenced should exist in knowledge base
    kb_patterns = set(re.findall(r'### Pattern: \[(.*?)\]', docs['kb']))
    for doc_type, refs in references.items():
        if doc_type != 'kb':
            for pattern in refs.get('kb', []):
                if pattern not in kb_patterns:
                    invalid_refs[doc_type].append(f"KB:{pattern}")

    # QG checkpoints referenced should exist in quality gates
    qg_checkpoints = set(re.findall(r'### ([A-Za-z0-9-]+)', docs['qg']))
    for doc_type, refs in references.items():
        if doc_type != 'qg':
            for checkpoint in refs.get('qg', []):
                if checkpoint not in qg_checkpoints:
                    invalid_refs[doc_type].append(f"QG:{checkpoint}")

    # Print results
    if any(invalid_refs.values()):
        print("Invalid references found:")
        for doc_type, refs in invalid_refs.items():
            if refs:
                print(f"  In {doc_paths[doc_type]}:")
                for ref in refs:
                    print(f"    - {ref}")
        return False
    else:
        print("All cross-document references are valid!")
        return True

if __name__ == "__main__":
    sys.exit(0 if validate_references() else 1)
```

## Benefits of Enhanced System

1. **Seamless Context Preservation**
   - Explicit handoffs between sessions
   - Clear links between decisions and implementation
   - Historical tracking of project evolution

2. **Reduced Cognitive Load**
   - Standardized reference system
   - Central starting points for any session
   - Automation for context gathering

3. **Better Knowledge Transfer**
   - Reusable patterns explicitly documented
   - Cross-project learning facilitated
   - AI context feeding standardized

4. **Improved Quality Assurance**
   - Explicit validation checkpoints
   - Code health consistently tracked
   - Visual quality metrics over time

## Implementation Plan

1. **Immediate Improvements**:
   - Start using cross-document linking notation
   - Implement the session start/end protocols
   - Create index.md dashboard

2. **Medium-Term Enhancements**:
   - Set up VS Code workspace configuration
   - Implement session context script
   - Build quality dashboard

3. **Long-Term Optimization**:
   - Add automated link validation
   - Consider tooling integration (Obsidian/Foam)
   - Evaluate effectiveness and refine system
