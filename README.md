<p align="center">
  <img src="logo.svg" alt="Copilot Skills Hub Logo" width="200" height="200">
</p>

# Copilot Skills Hub

> Discover, browse, and install GitHub Copilot skills for your projects.

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-success?logo=github)](https://samueltauil.github.io/skills-hub)
[![Skills Count](https://img.shields.io/badge/Skills-225-blue)](./site/src/data/skills.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What is this?

**Copilot Skills Hub** is a curated catalog of GitHub Copilot skills. Skills are instruction files (SKILL.md) that teach Copilot how to handle specific development tasks — from generating commit messages to performing security audits.

### Features

- **Browse by Category** — Skills organized into 11 categories (Testing, DevOps, Documentation, etc.)
- **Search** — Find skills by name, description, or trigger keywords
- **One-Click Install** — Copy commands to add skills to your project
- **Skill Details** — See what each skill does, its triggers, and example usage

## Browse Skills

Visit the live site: **[samueltauil.github.io/skills-hub](https://samueltauil.github.io/skills-hub)**

Or explore the [skills registry](./skills/registry.json) directly.

### Categories

| Category | Skills | Description |
|----------|:------:|-------------|
| ✨ Code Quality | 58 | Reviews, refactoring, linting |
| 📝 Documentation | 41 | READMEs, PRDs, technical writing |
| 🔀 Git & Version Control | 35 | Commits, branching, GitHub operations |
| 🎨 Frontend & UI | 20 | React, Vue, components, design |
| 🔌 API & Backend | 26 | REST APIs, GraphQL, databases |
| 🧪 Testing | 20 | Unit tests, E2E, test automation |
| 🚀 DevOps & CI/CD | 12 | Pipelines, Docker, Kubernetes |
| 🔧 MCP Development | 6 | Model Context Protocol servers and apps |
| 📊 Diagrams | 5 | Mermaid, PlantUML, visualizations |
| 🔒 Security | 1 | Audits, vulnerabilities, secure coding |
| 📈 Data & Analytics | 1 | SQL, data pipelines, visualization |

## Install a Skill

**Skills are auto-discovered!** Just add them to `.github/skills/` and Copilot loads them automatically based on their `name` and `description` frontmatter.

### Option 1: Git Submodule (Recommended)

```bash
# Example: Install the conventional-commits skill
git submodule add https://github.com/example/skill-repo.git .github/skills/conventional-commits
```

### Option 2: Direct Copy

1. Find the skill on the website
2. Download or copy the skill folder
3. Place it in `.github/skills/<skill-name>/` in your project
4. Ensure the folder contains a `SKILL.md` file

### Option 3: Manual Download

```bash
# Create skill directory and download SKILL.md
mkdir -p .github/skills/conventional-commits
curl -o .github/skills/conventional-commits/SKILL.md \
  https://raw.githubusercontent.com/example/skill-repo/main/SKILL.md
```

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
│   └── registry.json     # Manually curated skills subset
├── sources/              # Upstream skill sources (git submodules)
├── scripts/              # Sync and utility scripts
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

- Node.js 18+
- pnpm (or npm/yarn)

### Run Locally

```bash
cd site
pnpm install
pnpm dev
```

### Build for Production

```bash
pnpm build
```

### Available Scripts

Run from the repository root:

| Script | Description |
|--------|-------------|
| `npm run aggregate` | Aggregate skills from submodule sources into `site/src/data/skills.json` |
| `npm run scan` | Run security scan on all skills; updates `verified` field and embeds scan results |
| `npm run enrich` | AI-enrich skill metadata using `@github/copilot-sdk` (requires Copilot CLI) |
| `npm run build` | Aggregate + scan + build the Astro site |
| `npm run dev` | Aggregate + start local dev server |

## Security Scanning

Every skill is automatically scanned for potentially dangerous patterns using rules defined in [`skills/security-rules.yml`](skills/security-rules.yml).

Skills that pass the scan receive a **✅ Verified** badge on the catalog and their detail page.

### How it works

1. The scanner reads all code blocks from each skill's `SKILL.md` file
2. Each block is matched against the rules in `security-rules.yml`
3. Results are written back to `skills.json` (the `securityScan` and `verified` fields)
4. The site is rebuilt to reflect the updated badges

### Running a scan manually

```bash
# Scan and update skills.json
npm run scan

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
