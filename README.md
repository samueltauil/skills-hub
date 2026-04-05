<p align="center">
  <img src="logo.svg" alt="Copilot Skills Hub Logo" width="200" height="200">
</p>

# Copilot Skills Hub

> Discover, browse, and install GitHub Copilot skills for your projects.

[![Website](https://img.shields.io/badge/Website-Live-success?logo=github)](https://skillshub.space)
[![Skills Count](https://img.shields.io/badge/Skills-318-blue)](./site/src/data/skills.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What is this?

**Copilot Skills Hub** is a curated catalog of GitHub Copilot skills. Skills are instruction files (SKILL.md) that teach Copilot how to handle specific development tasks — from generating commit messages to performing security audits.

### Features

- **Browse by Category** — Skills organized into 11 categories (Testing, DevOps, Documentation, etc.)
- **Search** — Find skills by name, description, or trigger keywords
- **One-Click Install** — Copy commands to add skills to your project
- **CLI Extension** — Install skills directly from the terminal with `gh skills-hub`
- **Security Scanning** — Two-pass security scanner (regex + AI) validates every skill
- **Skill Details** — See what each skill does, its triggers, and example usage

## Browse Skills

Visit the live site: **[skillshub.space](https://skillshub.space)**

Or explore the [skills registry](./skills/registry.json) directly.

### Categories

| Category | Skills | Description |
|----------|:------:|-------------|
| ✨ Code Quality | 80 | Reviews, refactoring, linting |
| 📝 Documentation | 49 | READMEs, PRDs, technical writing |
| 🔀 Git & Version Control | 43 | Commits, branching, GitHub operations |
| 🎨 Frontend & UI | 42 | React, Vue, components, design |
| 🔌 API & Backend | 33 | REST APIs, GraphQL, databases |
| 🧪 Testing | 28 | Unit tests, E2E, test automation |
| 🚀 DevOps & CI/CD | 23 | Pipelines, Docker, Kubernetes |
| 🔧 MCP Development | 6 | Model Context Protocol servers and apps |
| 📊 Diagrams | 8 | Mermaid, PlantUML, visualizations |
| 🔒 Security | 2 | Audits, vulnerabilities, secure coding |
| 📈 Data & Analytics | 4 | SQL, data pipelines, visualization |

## Install a Skill

**Skills are auto-discovered!** Just add them to `.github/skills/` and Copilot loads them automatically based on their `name` and `description` frontmatter.

### Option 1: CLI Extension (Recommended)

```bash
# Install the gh extension
gh extension install samueltauil/skills-hub

# Search for skills
gh skills-hub search git

# Install a skill
gh skills-hub install git-commit

# Browse all available skills
gh skills-hub list
```

### Option 2: Download from Website

1. Find the skill on [skillshub.space](https://skillshub.space)
2. Click **Download ZIP** or **Copy All Files** on the skill detail page
3. Extract to `.github/skills/<skill-name>/` in your project

> **Note:** No configuration needed! Copilot discovers skills automatically from `.github/skills/`.

## Project Structure

```
skills-hub/
├── .github/
│   ├── workflows/        # CI/CD for deployment & validation
│   ├── ISSUE_TEMPLATE/   # Issue templates
│   └── PULL_REQUEST_TEMPLATE/
├── site/                 # Astro static site
│   ├── src/
│   │   ├── pages/        # Site pages
│   │   ├── components/   # UI components
│   │   └── layouts/      # Page layouts
│   └── public/           # Static assets
├── skills/
│   ├── schema.json       # Skill metadata schema
│   ├── registry.json     # Manually curated skills subset
│   └── security-rules.yml # Security scan rules
├── scripts/              # Build, scan, and enrichment scripts
├── sources/              # Upstream skill sources (git submodules)
├── gh-skills-hub         # GitHub CLI extension
└── CONTRIBUTING.md       # How to add skills
```

## Contributing

We welcome skill contributions! See the full **[Contribution Guide](CONTRIBUTING.md)** for detailed instructions.

### Quick Start

1. Fork this repository
2. Add your skill to `skills/registry.json`
3. Submit a Pull Request
4. GitHub Actions validates your submission automatically

### Skill Entry Format

```json
{
  "id": "my-skill",
  "name": "My Skill",
  "description": "What this skill does...",
  "shortDescription": "One-line summary",
  "category": "code-quality",
  "author": "your-name",
  "license": "MIT",
  "triggers": ["keyword1", "keyword2"],
  "complexity": "beginner",
  "source": {
    "repo": "https://github.com/owner/repo",
    "path": "skills/my-skill/SKILL.md"
  }
}
```

## Development

### Prerequisites

- Node.js 20+
- npm

### Run Locally

```bash
npm install
cd site && npm install && cd ..
npm run dev
```

### Build for Production

```bash
npm run build
```

### Available Scripts

Run from the repository root:

| Script | Description |
|--------|-------------|
| `npm run aggregate` | Aggregate skills from submodule sources into `site/src/data/skills.json` |
| `npm run scan` | Run regex security scan on all skills; updates `verified` field |
| `npm run scan:ai` | Run regex + AI security scan (requires `GITHUB_TOKEN` and Copilot CLI) |
| `npm run enrich` | AI-enrich skill metadata using `@github/copilot-sdk` (requires Copilot CLI) |
| `npm run build` | Aggregate + scan + build the Astro site |
| `npm run dev` | Aggregate + start local dev server |

## Security Scanning

Every skill undergoes a two-pass automated security scan before being published.

### How it works

**Pass 1 — Pattern analysis** scans all skill files against 13 regex-based rules defined in [`skills/security-rules.yml`](skills/security-rules.yml):
- Shell command execution, eval, and unsafe deserialization
- Prompt injection markers and social engineering phrases
- Hardcoded secrets, credentials, and sensitive file access
- Base64 decode-and-execute, environment variable exfiltration
- Path traversal, SQL injection, and curl-pipe-to-shell patterns

**Pass 2 — AI deep scan** (opt-in) uses `@github/copilot-sdk` to semantically analyze skills for threats that regex can't catch: obfuscated malware, disguised data exfiltration, and supply chain risks.

Skills that pass the scan receive a **✅ Verified** badge on the catalog and their detail page.

### Running a scan manually

```bash
# Regex scan (default — runs as part of build)
npm run scan

# Regex + AI scan (requires GITHUB_TOKEN)
GITHUB_TOKEN=ghp_... npm run scan:ai

# Scan only (no write-back)
node scripts/scan-skills.js --output my-report.json

# Fail CI on high-severity findings
node scripts/scan-skills.js --fail-on-high
```

The scan runs automatically every time skills are synced from upstream sources (weekly via [`sync-skills.yml`](.github/workflows/sync-skills.yml)) and can also be triggered manually via the [Enrich & Scan Skills](.github/workflows/enrich-skills.yml) workflow.

## AI Enrichment

The `enrich-skills.js` script uses [`@github/copilot-sdk`](https://www.npmjs.com/package/@github/copilot-sdk) to improve skill metadata:

- **shortDescription** — a tight one-sentence summary
- **tags** — up to 5 relevant keywords
- **complexity** — `beginner`, `intermediate`, or `advanced`
- **platforms** — `windows`, `macos`, `linux`

Enrichment is incremental: skills already enriched are skipped unless `--force` is passed.

### Running enrichment manually

```bash
# Enrich up to 10 pending skills
GITHUB_TOKEN=ghp_... npm run enrich -- --limit 10

# Force re-enrich everything
GITHUB_TOKEN=ghp_... npm run enrich -- --force

# Dry-run (no writes)
GITHUB_TOKEN=ghp_... node scripts/enrich-skills.js --dry-run
```

The enrichment workflow can be triggered on-demand from the [Actions tab](../../actions/workflows/enrich-skills.yml).

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Copilot Skills Hub</strong> — Discover the right skill for every task.
</p>
