<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Vibe Coding Template – Unified Improvement Guide

*(Tailored for Windsurf \& VS Code users, with an expanded S.C.A.F.F. prompt-engineering section)*

## 1. Repository Layout (ready to copy)

```
Vibe-Coding/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── improvement.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       ├── validate-links.yml
│       └── template-check.yml
│
├── .vscode/                 # VS Code fallback settings
│   └── settings.json
├── .windsurf/               # Windsurf-specific config *
│   ├── flows.yaml           # Saved AI Flows
│   ├── cascade.json         # Project-wide context rules
│   └── prompts/             # Re-usable S.C.A.F.F. prompts
│
├── scripts/
│   ├── session_setup.py
│   ├── validate_links.py
│   └── template_init.py
│
├── documents/
│   ├── Vibe-Coding-Playbook.md
│   ├── global_rules.md
│   ├── planning/
│   │   ├── prd.md
│   │   ├── project_context.md
│   │   └── implementation_schedule.md
│   └── execution/
│       ├── dev_log.md
│       ├── knowledge_base.md
│       ├── quality_gates.md
│       └── session_logs/
│
├── README.md
├── LICENSE
└── pyproject.toml
```

\* **Why `.windsurf/`?** Windsurf stores project-level AI settings locally (analogous to `.vscode`). Housing flows and prompt libraries here lets Windsurf’s Cascade modes preload your docs and S.C.A.F.F. templates automatically[^1][^2].

## 2. S.C.A.F.F. Prompt-Engineering Cheatsheet

> **S**ituation -  **C**hallenge -  **A**udience -  **F**ormat -  **F**oundations

| Section | What to include | Example excerpt |
| :-- | :-- | :-- |
| **Situation** | Project background, architecture, constraints | “Monorepo with FastAPI + React served from Docker-Compose…” |
| **Challenge** | Specific task, success criteria, performance needs | “Add optimistic UI for profile update; must keep latency < 150 ms.” |
| **Audience** | Skill level \& future maintainers | “Maintained by mid-level JS devs; code will be OSS.” |
| **Format** | Desired output structure (code block, table, diff) | “Return a unified diff against `client/src/Profile.jsx`.” |
| **Foundations** | Style guides, patterns, security or quality gates to respect | “Follow Tailwind naming rules \& pass [QG:PreCommit] checklist.” |

**Why it works** – structured prompts dramatically raise LLM output quality[^3][^4]. Research on graduated “scaffolding” shows higher-level support (full paragraph suggestions) beats ad-hoc tips for productivity gains[^5][^6].

## 3. Windsurf / VS Code AI Integration

1. **Bootstrap context**
    - Add `documents/_current_context.md` (1-2 kB summary) and emit it as a *Memory* in Windsurf or pin it in VS Code’s AI Toolkit chat[^7][^8].
2. **Reusable S.C.A.F.F. library**
    - Store each common task prompt under `.windsurf/prompts/*.md` or `.vscode/prompts/*.md`.
    - Name files `scaff_feature_dev.md`, `scaff_debugging.md`, etc.
3. **Flows \& Cascade** (Windsurf only)
    - Define a *Flow* that: pulls latest `session_logs`, loads `_current_context.md`, then launches Cascade Chat with the selected S.C.A.F.F. template.
    - Save the YAML in `.windsurf/flows.yaml` for one-click kickoff[^1].
4. **VS Code fallback**
    - Install *AI Toolkit* extension and bind *Custom Commands* that read the same prompt files[^7][^8].

## 4. Automation Scripts (skeletons)

```python
# scripts/session_setup.py
"""Print handoff & sprint focus at shell startup."""
import datetime, pathlib, textwrap
doc = pathlib.Path("documents/execution/dev_log.md")
last_entry = doc.read_text().split("[")[^1].split("]")[^0]
print(textwrap.dedent(f"""
🕒 {datetime.date.today()} | Last session: {last_entry}
Next task → see implementation_schedule.md
"""))
```

```python
# scripts/validate_links.py
"""CI helper to verify [IMPL-task:X] etc. resolve."""
# parse markdown, collect anchors, compare, exit 1 on failure
```

## 5. Quality \& Governance add-ons

| Checklist | Action |
| :-- | :-- |
| **Pre-Commit** | Add `ruff`, `black`, `prettier`, secret-scan hooks. |
| **SAIF Alignment** | Map any AI code to Google’s Secure AI Framework elements: strong foundations, detection, automated defenses, platform harmonization, adaptive controls, business-risk context[^9]. |
| **S.D.L.C. gates** | Wire `quality_gates.md` steps into the PR template; block merge unless all boxes tick. |

## 6. Quick Start Steps

1. **Clone template** → `Use this template` on GitHub.
2. **Run** `python scripts/template_init.py --project "AcmeApp"` to relabel placeholders.
3. **Launch Windsurf** → open repo → import `.windsurf` config → start **“New-Feature”** Flow.
4. **First prompt** → S.C.A.F.F. file auto-populates; fill Situation \& Challenge, press *Cascade Write*.
5. **Commit** → pass `pre-commit` hooks; link references like `[IMPL-task:3]`.

## 7. Attribution Footnotes

S.C.A.F.F. pattern adapted from Vibe-Coding Prompt Engineering System[^3]; empirical benefits of scaffolded AI assistance from CHI 2024 study on varied scaffolding levels[^5][^6]; Windsurf capabilities summarized from official tutorials and feature guides[^1][^2]. Integration notes for VS Code AI Toolkit follow Microsoft documentation[^7][^8]; security alignment references Google SAIF quick guide[^9].

### End-of-File

Copy this markdown into `Vibe-Coding-Template-Guide.md` at the repo root for immediate use and sharing.

<div style="text-align: center">⁂</div>

[^1]: <https://www.datacamp.com/tutorial/windsurf-ai-agentic-code-editor>

[^2]: <https://www.classcentral.com/course/youtube-windsurf-tutorial-for-beginners-ai-code-editor-better-than-cursor-427369>

[^3]: <https://docs.vibe-coding-framework.com/framework-components/prompt-engineering-system>

[^4]: <https://www.promptlayer.com/glossary/prompt-scaffolding>

[^5]: <https://arxiv.org/html/2402.11723v1>

[^6]: <https://arxiv.org/abs/2402.11723>

[^7]: <https://learn.microsoft.com/en-gb/windows/ai/toolkit/>

[^8]: <https://learn.microsoft.com/en-us/windows/ai/toolkit/toolkit-getting-started>

[^9]: <https://kstatic.googleusercontent.com/files/00e270b1cccb1f37302462a162c171d86f293a84de54036e0021e2fe0253cf05623bae2a62751b0840667bc6c8412fd70f45c9485972dc370be8394fae922d31>





































