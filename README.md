# Vibe Coding Project

Welcome to the Vibe Coding Project! This repository leverages the Vibe Coding System—a
documentation-driven workflow for efficient, high-quality software development with AI-assisted collaboration.

---

## 🚀 Project Overview

- **Goal**: [Summarize your project’s purpose and outcome. See `documents/planning/prd.md` → GOAL section.]
- **Tech Stack**: Python 3.11+, FastAPI, React 18.x, PostgreSQL, Tailwind CSS (see `documents/planning/project_context.md`)
- **Current Status**: [Reference active sprint and status from `implementation_schedule.md`]

---

## 📂 Repository Structure

- `/client`: React frontend
- `/server`: FastAPI backend
- `/documents`: All project documentation (see below)
- `/scripts`: Automation and utility scripts
- `/config`: Centralized configuration for editor, CI, and GitHub workflows (see subfolders)
  - `config/editor`: Editor settings (formerly `.vscode`)
  - `config/ci`: CI configuration (formerly `.windsurf`)
  - `config/github`: GitHub workflows and templates (formerly `.github`)

---

## 📑 Documentation Navigation

All project documentation is organized and navigable via the sidebar structure in
[`documents/docs_sidebar.json`](documents/docs_sidebar.json). This sidebar is used by VS Code,
Windsurf, and other tools for hierarchical navigation and onboarding.

- **Getting Started Guide**: [`documents/guides/getting_started.md`]
(documents/guides/getting_started.md) provides an AI-driven onboarding workflow.

<details>
<summary>Key Documents</summary>

- **CHANGELOG.md**: [`documents/execution/CHANGELOG.md`](documents/execution/CHANGELOG.md)
- **Playbook**: [`documents/playbook.md`](documents/playbook.md)
- **PRD**: [`documents/planning/prd.md`](documents/planning/prd.md)
- **Scope Appendix**: [`documents/planning/scope_appendix.md`](documents/planning/scope_appendix.md)
- **Implementation Schedule**: [`documents/planning/implementation_schedule.md`](documents/planning/implementation_schedule.md)
- **Project Context**: [`documents/planning/project_context.md`](documents/planning/project_context.md)
- **Dev Log**: [`documents/execution/dev_log.md`](documents/execution/dev_log.md)
- **Knowledge Base**: [`documents/execution/knowledge_base.md`](documents/execution/knowledge_base.md)
- **Quality Gates**: [`documents/execution/quality_gates.md`](documents/execution/quality_gates.md)
- **Guides**: [`documents/guides/`](documents/guides/)
  - **Getting Started**: [`documents/guides/getting_started.md`](documents/guides/getting_started.md)
- **Current Context**: [`documents/_current_context.md`](documents/_current_context.md)

</details>

For the full documentation tree and navigation, see [`documents/docs_sidebar.json`]
(documents/docs_sidebar.json). All documents are cross-linked using a standardized reference system
(see Playbook for details).

---

## 🛠️ Getting Started

### Installation

```bash
# Set up Python environment and install dependencies
uv venv
uv sync
```

All Python dependency management is now handled by [UV](https://github.com/astral-sh/uv). See `/pyproject.toml` for dependencies.

> **Note:** All editor and CI configuration is now centralized under `/config` (see `/config/editor`, `/config/ci`, `/config/github`).

### Linting

```bash
make lint
```

### Documentation

```bash
make docs
```

### Scripts

- All utility scripts are accessible via a unified CLI:

```bash
python scripts/cli.py --help
```

Subcommands:

- `init-session`: Initialize a new session
- `init-template`: Initialize a new template
- `check-links`: Validate documentation links

### Prerequisites

- Node.js v18+
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (for Python dependency management, replacing Poetry; see [Adopting UV and Cleaning Up Editor_CI Config Redun.md])
- [Other dependencies as listed in `pyproject.toml` and `project_context.md`]

### Setup

```bash
# Clone the repo
git clone https://github.com/connorkitchings/Vibe-Coding.git
cd Vibe-Coding

# (Optional) Set up Python environment
python -m venv venv
source venv/bin/activate
uv venv
uv pip install -r pyproject.toml  # Or use 'uv pip install -e .' if using editable mode

# Or, to install all dependencies and activate the venv in one step:
uv venv && uv pip install -r pyproject.toml

# (Optional) Set up Node environment for frontend
cd client
npm install
```

---

## 🧭 Development Workflow

- Follow the Vibe Coding System: update session logs, reference the playbook, and link all
  decisions and artifacts.
- Use the checklists in `quality_gates.md` before committing or merging code.
- Document all reusable patterns in the knowledge base.

---

## 🤝 Contributing

Please read the [global_rules.md](documents/global_rules.md) and
[quality_gates.md](documents/execution/quality_gates.md) before contributing. All contributions
should follow the standards and workflow described in the playbook.

---

## 📬 Contact

- Author: Connor Kitchings (<connor.kitchings@gmail.com>)
- For more details, see the [Vibe Coding Playbook](documents/Vibe%20Coding%20Playbook.md).

---

## 📄 License

[Specify your license here]
