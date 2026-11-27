<p align="center">
  <img src="logo.svg" alt="Copilot Skills Hub Logo" width="200" height="200">
</p>

# Copilot Skills Hub

> Discover, browse, and install GitHub Copilot skills for your projects.

[![Website](https://img.shields.io/badge/Website-Live-success?logo=github)](https://skillshub.space)
[![Skills Count](https://img.shields.io/badge/Skills-1154-blue)](./site/src/data/skills.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What is this?

**Copilot Skills Hub** is a curated catalog of GitHub Copilot skills. Skills are instruction files (SKILL.md) that teach Copilot how to handle specific development tasks — from generating commit messages to performing security audits.

### Features

- **Browse by Category** — Skills organized into 12 categories (Testing, DevOps, Documentation, etc.)
- **Search & Filters** — Search by name, description, tag or source, then narrow by category, source or verified status. Filtered views are reflected in the URL so you can share them
- **Agent Plugins** — Every publishable skill is packaged as an [Agent Plugin](https://agent-plugins.org) and listed in a plugin marketplace you can add to GitHub Copilot CLI or VS Code
- **One-Click Install** — Copy commands to add skills to your project
- **CLI Extension** — Install skills directly from the terminal with `gh skills-hub`
- **Security Scanning** — Two-pass security scanner (regex + AI) validates every skill
- **Skill Details** — See what each skill does, its triggers, and example usage

## Browse Skills

Visit the live site: **[skillshub.space](https://skillshub.space)**

Or explore the [skills registry](./skills/registry.json) directly.

### Sources

Skills are synced weekly from official upstream repositories (git submodules under [`sources/`](./sources)):

- **GitHub & Microsoft:** [github/awesome-copilot](https://github.com/github/awesome-copilot), [microsoft/azure-skills](https://github.com/microsoft/azure-skills), [dotnet/skills](https://github.com/dotnet/skills)
- **AI providers:** [anthropics/skills](https://github.com/anthropics/skills), [openai/skills](https://github.com/openai/skills), [google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills), [huggingface/skills](https://github.com/huggingface/skills), [modelcontextprotocol/ext-apps](https://github.com/modelcontextprotocol/ext-apps)
- **Cloud & platforms:** [google/skills](https://github.com/google/skills), [cloudflare/skills](https://github.com/cloudflare/skills), [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills), [firebase/agent-skills](https://github.com/firebase/agent-skills), [docker/skills](https://github.com/docker/skills), [pulumi/agent-skills](https://github.com/pulumi/agent-skills)
- **Data & observability:** [supabase/agent-skills](https://github.com/supabase/agent-skills), [mongodb/agent-skills](https://github.com/mongodb/agent-skills), [neondatabase/agent-skills](https://github.com/neondatabase/agent-skills), [elastic/agent-skills](https://github.com/elastic/agent-skills), [grafana/skills](https://github.com/grafana/skills), [getsentry/skills](https://github.com/getsentry/skills)
- **App development:** [stripe/ai](https://github.com/stripe/ai), [expo/skills](https://github.com/expo/skills), [callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills), [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)

Only skills under redistributable licenses (MIT, Apache-2.0, BSD, ISC, CC-BY-4.0) are published; skills with proprietary or unrecognized license files are skipped. When two sources publish a skill with the same name, the later source's ID is prefixed with its author (e.g. `anthropic-webapp-testing`).

To add a source: `git submodule add <repo-url> sources/<name>`, then add an entry to `SOURCES` in [`scripts/aggregate-skills.js`](scripts/aggregate-skills.js) with the skill directory `paths` (`*` matches one directory level) and the repository's default license.

### Categories

| Category | Skills | Description |
|----------|:------:|-------------|
| ✨ Code Quality | 270 | Reviews, refactoring, linting |
| 📝 Documentation | 129 | READMEs, PRDs, technical writing |
| 🔀 Git & Version Control | 117 | Commits, branching, GitHub operations |
| 🎨 Frontend & UI | 179 | React, Vue, components, design |
| 🔌 API & Backend | 188 | REST APIs, GraphQL, databases |
| 🧪 Testing | 97 | Unit tests, E2E, test automation |
| 🚀 DevOps & CI/CD | 114 | Pipelines, Docker, Kubernetes |
| 🔧 MCP Development | 7 | Model Context Protocol servers and apps |
| 📊 Diagrams | 14 | Mermaid, PlantUML, visualizations |
| 🔒 Security | 15 | Audits, vulnerabilities, secure coding |
| 📈 Data & Analytics | 23 | SQL, data pipelines, visualization |
| 📄 Office Documents | 1 | Spreadsheets, presentations, documents |

## Install a Skill

### Option 1: Agent Plugin marketplace (Recommended)

This repository is a plugin marketplace. Each skill is published as its own plugin under [`plugins/`](./plugins), and the catalog lives in [`.github/plugin/marketplace.json`](.github/plugin/marketplace.json). The plugin name is the skill ID shown on the website.

**GitHub Copilot CLI**

```bash
# Add the marketplace once
copilot plugin marketplace add samueltauil/skills-hub

# Browse what's available
copilot plugin marketplace browse skills-hub

# Install a skill as a plugin
copilot plugin install git-commit@skills-hub
```

**VS Code**

1. Turn on the `chat.plugins.enabled` setting.
2. Add the marketplace: open the Agent Customizations editor and add `samueltauil/skills-hub` as a marketplace, or add it to your settings:

   ```json
   "chat.plugins.marketplaces": ["samueltauil/skills-hub"]
   ```

3. Search for a skill and install it. Every skill page on [skillshub.space](https://skillshub.space) also has an **Install in VS Code** button.

### Option 2: CLI Extension

Skills installed this way go into `.github/skills/`, where Copilot discovers them automatically from their `name` and `description` frontmatter.

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

### Option 3: Download from Website

1. Find the skill on [skillshub.space](https://skillshub.space)
2. Click **Download ZIP** or **Copy All Files** on the skill detail page
3. Extract to `.github/skills/<skill-name>/` in your project

> **Note:** No configuration needed! Copilot discovers skills automatically from `.github/skills/`.

## Project Structure

```
skills-hub/
├── .github/
│   ├── plugin/
│   │   └── marketplace.json  # Agent Plugin marketplace (generated)
│   ├── workflows/        # CI/CD for deployment & validation
│   ├── ISSUE_TEMPLATE/   # Issue templates
│   └── PULL_REQUEST_TEMPLATE/
├── plugins/              # One Agent Plugin per skill (generated, do not edit)
│   └── <skill-id>/
│       ├── plugin.json   # Agent Plugins manifest
│       ├── README.md     # Install instructions
│       ├── LICENSE       # Upstream license notice
│       └── skills/<skill-name>/SKILL.md
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
├── scripts/              # Build, scan, enrichment and plugin scripts
│   └── schemas/          # Vendored Agent Plugins JSON schema
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
| `npm run build:plugins` | Regenerate `plugins/` and `.github/plugin/marketplace.json` from `skills.json` |
| `npm run check:plugins` | Fail if the generated plugins or marketplace are out of date |
| `npm run validate:plugins` | Validate the marketplace and every plugin against the Agent Plugins spec |
| `npm test` | Run the plugin tooling unit tests |
| `npm run build` | Aggregate + scan + build and validate plugins + build the Astro site |
| `npm run dev` | Aggregate + start local dev server |

## Agent Plugins

Skills Hub follows the [Agent Plugins](https://agent-plugins.org) specification so skills can be installed and updated through standard plugin tooling.

- [`scripts/build-plugins.js`](scripts/build-plugins.js) turns every skill in `site/src/data/skills.json` into `plugins/<skill-id>/` with a `plugin.json` manifest, a README, the upstream license notice and the skill files under `skills/<skill-name>/`. It also writes the marketplace catalog to `.github/plugin/marketplace.json`.
- Plugin versions start at `1.0.0` and get a patch bump whenever the packaged content changes (tracked by a content hash in `extensions["space.skillshub"]`). The marketplace version is bumped whenever its entries change, so plugin and marketplace versions always move together.
- Skills that can't meet the spec (for example a description longer than 1024 characters) are skipped with a warning and stay available through the other install options.
- [`scripts/validate-plugins.js`](scripts/validate-plugins.js) checks the marketplace (names, owners, relative sources, version and description parity with each `plugin.json`), every manifest (closed schema, kebab-case name matching its directory, semver), each bundled `SKILL.md` (frontmatter name and description limits), licenses and symlinks.

The [Validate Plugins](.github/workflows/validate-plugins.yml) workflow runs on every pull request that touches plugins or the scripts that generate them. It runs the unit tests and the validator, validates every `plugin.json` against the official JSON schema, and checks that the generated output is up to date. The sync and enrichment workflows regenerate plugins automatically, so you never need to edit files under `plugins/` by hand.

```bash
npm run build:plugins     # regenerate plugins and marketplace
npm run validate:plugins  # validate against the spec
npm run check:plugins     # verify nothing is stale
npm test                  # unit tests
```

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
