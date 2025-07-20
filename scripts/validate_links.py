"""CI helper to verify [IMPL-task:X] etc. resolve."""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "documents"
PATTERNS = [
    re.compile(r"\[IMPL-task:(\w+)\]"),
    re.compile(r"\[PRD-decision:(\d{4}-\d{2}-\d{2})\]"),
    re.compile(r"\[KB:([\w-]+)\]"),
    re.compile(r"\[QG:([\w-]+)\]"),
    re.compile(r"\[LOG:(\d{4}-\d{2}-\d{2})\]"),
]

# Collect all markdown files
files = list(DOCS.rglob("*.md")) + [ROOT / "README.md"]
anchors = set()
for file in files:
    with open(file, encoding="utf-8") as f:
        for line in f:
            for pat in PATTERNS:
                for m in pat.finditer(line):
                    anchors.add(m.group(0))

# Check that all anchors resolve (dummy logic: just print them for now)
for anchor in anchors:
    print(f"Found anchor: {anchor}")

# TODO: Implement full cross-doc anchor resolution logic
