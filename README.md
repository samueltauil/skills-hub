<p align="center">
  <img src="logo.svg" alt="Copilot Skills Hub Logo" width="200" height="200">
</p>

# Copilot Skills Hub

> Discover, browse, and install GitHub Copilot skills for your projects.

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-success?logo=github)](https://samueltauil.github.io/skills-hub)
[![Skills Count](https://img.shields.io/badge/Skills-10+-blue)](./skills/registry.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What is this?

**Copilot Skills Hub** is a curated catalog of GitHub Copilot skills. Skills are instruction files (SKILL.md) that teach Copilot how to handle specific development tasks — from generating commit messages to performing security audits.

### Features

- **Browse by Category** — Skills organized into 10+ categories (Testing, DevOps, Security, etc.)
- **Search** — Find skills by name, description, or trigger keywords
- **One-Click Install** — Copy commands to add skills to your project
- **Skill Details** — See what each skill does, its triggers, and example usage

## Browse Skills

Visit the live site: **[skills-hub.dev](https://skills-hub.dev)** *(or [samueltauil.github.io/skills-hub](https://samueltauil.github.io/skills-hub))*

Or explore the [skills registry](./skills/registry.json) directly.

### Categories

| Category | Description |
|----------|-------------|
| 🔀 Git & Version Control | Commits, branching, GitHub operations |
| ✨ Code Quality | Reviews, refactoring, linting |
| 📝 Documentation | READMEs, PRDs, technical writing |
| 📊 Diagrams | Mermaid, PlantUML, visualizations |
| 🧪 Testing | Unit tests, E2E, test automation |
| 🔌 API & Backend | REST APIs, GraphQL, databases |
| 🎨 Frontend & UI | React, Vue, components, design |
| 🚀 DevOps & CI/CD | Pipelines, Docker, Kubernetes |
| 🔒 Security | Audits, vulnerabilities, secure coding |
| 📈 Data & Analytics | Data pipelines, SQL, analytics |

## Install a Skill

### Option 1: Git Submodule (Recommended)

```bash
# Example: Install the conventional-commits skill
git submodule add https://github.com/github/awesome-copilot.git .github/skills/awesome-copilot
```

### Option 2: Direct Copy

1. Find the skill on the website
2. Click "View Raw" to see the SKILL.md
3. Copy the content to `.github/skills/<skill-name>/SKILL.md` in your project

### Option 3: Manual Download

```bash
# Download a single skill file
curl -o .github/skills/conventional-commits/SKILL.md \
  https://raw.githubusercontent.com/github/awesome-copilot/main/skills/git-commit/SKILL.md
```

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
│   └── registry.json     # Skills catalog
├── indexer/              # Python skill scraper (future)
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

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Copilot Skills Hub</strong> — Discover the right skill for every task.
</p>
