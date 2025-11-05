# Agent Skills Catalog

## Overview
This directory contains "Skills" - modular capabilities that agents can use to perform complex tasks.

## Available Skills

| Skill Name | Description | Key Files |
|------------|-------------|-----------|
| `context-audit` | Scans repo to estimate token usage and identify large files | `.agents/skills/context-audit.py` |
| `web-init` | *Placeholder* Scaffolds a new web frontend | `.agents/skills/web_init.py` |

## Creating a New Skill
1. Create a directory: `.agents/skills/<skill-slug>/`
2. Add `SKILL.md` with instructions.
3. Add any support scripts or templates.
