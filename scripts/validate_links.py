#!/usr/bin/env python3
# validate_links.py - Check cross-document references

import re
import sys
from collections import defaultdict


def extract_references(content):
    """Extract all references from content."""
    patterns = {
        "prd": r"\[PRD-decision:(\d{4}-\d{2}-\d{2})\]",
        "backlog": r"\[BL-task:([A-Za-z0-9-]+)\]",
        "devlog": r"\[DL:(\d{4}-\d{2}-\d{2})\]",
        "kb": r"\[KB:([A-Za-z0-9-]+)\]",
        "qg": r"\[QG:([A-Za-z0-9-]+)\]",
    }

    refs = {}
    for ref_type, pattern in patterns.items():
        refs[ref_type] = re.findall(pattern, content)

    return refs


def validate_references():
    """Validate all cross-document references."""
    doc_paths = {
        "prd": "../documents/prd.md",
        "backlog": "../documents/backlog.md",
        "devlog": "../documents/dev_log.md",
        "kb": "../documents/knowledge_base.md",
        "qg": "../documents/quality_gates.md",
    }

    # Read all documents
    docs = {}
    for doc_type, path in doc_paths.items():
        try:
            with open(path) as f:
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
    prd_decisions = set(re.findall(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|", docs["prd"]))
    for doc_type, refs in references.items():
        if doc_type != "prd":
            for date in refs.get("prd", []):
                if date not in prd_decisions:
                    invalid_refs[doc_type].append(f"PRD-decision:{date}")

    # Backlog tasks referenced should exist in backlog
    backlog_tasks = set(
        re.findall(r"- \[ \] \*\*([A-Za-z0-9-]+)\*\*:", docs["backlog"])
    )
    for doc_type, refs in references.items():
        if doc_type != "backlog":
            for task in refs.get("backlog", []):
                if task not in backlog_tasks:
                    invalid_refs[doc_type].append(f"BL-task:{task}")

    # Dev log dates referenced should exist in dev log
    devlog_dates = set(re.findall(r"## \[(\d{4}-\d{2}-\d{2})\]", docs["devlog"]))
    for doc_type, refs in references.items():
        if doc_type != "devlog":
            for date in refs.get("devlog", []):
                if date not in devlog_dates:
                    invalid_refs[doc_type].append(f"DL:{date}")

    # KB patterns referenced should exist in knowledge base
    kb_patterns = set(re.findall(r"### Pattern: \[(.*?)\]", docs["kb"]))
    for doc_type, refs in references.items():
        if doc_type != "kb":
            for pattern in refs.get("kb", []):
                if pattern not in kb_patterns:
                    invalid_refs[doc_type].append(f"KB:{pattern}")

    # QG checkpoints referenced should exist in quality gates
    qg_checkpoints = set(re.findall(r"### ([A-Za-z0-9-]+)", docs["qg"]))
    for doc_type, refs in references.items():
        if doc_type != "qg":
            for checkpoint in refs.get("qg", []):
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


def main():
    print("\n📝 Validating cross-document references...\n")
    is_valid = validate_references()
    print("\n✅ Validation complete!")
    if is_valid:
        print("🎉 All references are valid.")
    else:
        print("⚠️ Some references are invalid. Please fix them for better traceability.")

    return 0 if is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
