# Getting Started

Welcome to a new project with **Vibe Coding**! This guide uses AI to:

1. Introspect the repository structure.
2. Ask targeted questions to understand your project.
3. Scaffold key documents (e.g., PRD) before any code.

---

## 1. Repository Introspection

```bash
python scripts/init_template.py introspect --output structure.json
```

This creates `structure.json` describing:

- Top-level folders/files
- Existing documentation
- Detected tech stack (e.g., presence of `client/`, `server/`)

---

## 2. AI-Assisted Project Discovery

The CLI will:

- Prompt for project name, goals, and team context
- Generate a draft PRD and planning artifacts

---

## 3. Next Steps

- Review generated docs in `documents/planning/`
- Use `make install` and `make lint` to set up and check your environment
- Explore scripts using `python scripts/cli.py --help`

---

For more, see the [Vibe Coding Template – Review, Simplification Oppo.md](../../Vibe%20Coding%20Template%20%E2%80%93%20Review%2C%20Simplification%20Oppo.md).
