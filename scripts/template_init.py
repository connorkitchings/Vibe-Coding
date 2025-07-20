"""Script to relabel placeholders for new projects."""

import argparse
import os
import re


def relabel_project(root, old, new):
    for dirpath, _, files in os.walk(root):
        for fname in files:
            if (
                fname.endswith(".md")
                or fname.endswith(".py")
                or fname.endswith(".json")
            ):
                path = os.path.join(dirpath, fname)
                with open(path, encoding="utf-8") as f:
                    content = f.read()
                content = re.sub(re.escape(old), new, content)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Relabel all occurrences of the default project name in .md, .py, and .json files."
    )
    parser.add_argument(
        "--project",
        required=True,
        help="New project name (will replace all occurrences of 'Vibe Coding Project')",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory to start relabeling (default: current directory)",
    )
    parser.add_argument(
        "--old",
        default="Vibe Coding Project",
        help="Placeholder to replace (default: 'Vibe Coding Project')",
    )
    args = parser.parse_args()
    relabel_project(args.root, args.old, args.project)
    print(f"✔️ Relabeling complete: '{args.old}' → '{args.project}' in {args.root}")
