# Contributing to Skills Hub

Thank you for your interest in contributing to the Copilot Skills Hub! This guide will walk you through adding a new skill to the registry.

## Table of Contents

- [What is a Skill?](#what-is-a-skill)
- [Before You Start](#before-you-start)
- [Adding a New Skill](#adding-a-new-skill)
- [Skill Entry Format](#skill-entry-format)
- [Categories](#categories)
- [Validation](#validation)
- [Review Process](#review-process)

---

## What is a Skill?

A **skill** is a `SKILL.md` file that provides instructions to GitHub Copilot for handling specific development tasks. When a skill is installed in a project, Copilot reads the instructions and applies them when relevant triggers are detected.

### Example Skill Use Cases

- Generate conventional commits
- Create API endpoints with best practices
- Write unit tests following specific patterns
- Perform security audits
- Generate documentation

---

## Before You Start

### Requirements

1. **Your skill must be hosted in a public GitHub repository**
2. The skill file must be named `SKILL.md`
3. The skill must follow the [SKILL.md format](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)

### Quality Guidelines

- Skills should be **focused** — one skill, one purpose
- Instructions should be **clear and actionable**
- Include **trigger keywords** so users know when the skill activates
- Provide **examples** in your SKILL.md when helpful
- Test your skill before submitting

---

## Adding a New Skill

### Step 1: Prepare Your Skill Repository

Ensure your skill is hosted in a public GitHub repository with this structure:

```
your-repo/
├── SKILL.md          # Required: The skill instructions
├── README.md         # Recommended: Description and usage
└── examples/         # Optional: Example outputs
```

### Step 2: Fork the Skills Hub Repository

1. Go to [github.com/samueltauil/skills-hub](https://github.com/samueltauil/skills-hub)
2. Click **Fork** in the top-right corner
3. Clone your fork locally:

```bash
git clone https://github.com/YOUR_USERNAME/skills-hub.git
cd skills-hub
```

### Step 3: Add Your Skill to the Registry

1. Open `skills/registry.json`
2. Add your skill to the `skills` array
3. Follow the [Skill Entry Format](#skill-entry-format) below

### Step 4: Submit a Pull Request

1. Commit your changes:

```bash
git add skills/registry.json
git commit -m "feat: add <skill-name> skill"
git push origin main
```

2. Go to your fork on GitHub
3. Click **"Contribute"** → **"Open pull request"**
4. Fill out the PR template with details about your skill
5. Submit the PR

---

## Skill Entry Format

Each skill in `registry.json` must follow this structure:

```json
{
  "id": "my-skill-name",
  "name": "My Skill Name",
  "description": "A detailed description of what this skill does and when it's useful. 2-3 sentences recommended.",
  "shortDescription": "One-line summary for cards",
  "category": "code-quality",
  "author": "your-github-username",
  "license": "MIT",
  "triggers": ["keyword1", "keyword2", "phrase to trigger"],
  "complexity": "beginner",
  "source": {
    "repo": "https://github.com/owner/repository",
    "path": "SKILL.md"
  }
}
```

### Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| `id` | ✅ | Unique identifier (lowercase, hyphens only) |
| `name` | ✅ | Human-readable name |
| `description` | ✅ | Full description (100-300 chars) |
| `shortDescription` | ✅ | One-line summary (50-80 chars) |
| `category` | ✅ | One of the [valid categories](#categories) |
| `author` | ✅ | Your GitHub username |
| `license` | ✅ | License (MIT, Apache-2.0, etc.) |
| `triggers` | ✅ | Keywords that activate the skill |
| `complexity` | ✅ | `beginner`, `intermediate`, or `advanced` |
| `source.repo` | ✅ | Full GitHub repository URL |
| `source.path` | ✅ | Path to SKILL.md in the repo |

### Complexity Levels

- **beginner** — Simple, single-purpose skills
- **intermediate** — Multi-step workflows, some configuration
- **advanced** — Complex patterns, requires domain expertise

---

## Categories

Your skill must belong to one of these categories:

| Category ID | Name | Description |
|-------------|------|-------------|
| `api-backend` | API & Backend | REST APIs, GraphQL, databases, servers |
| `code-quality` | Code Quality | Reviews, refactoring, linting, formatting |
| `data-analytics` | Data & Analytics | SQL, data pipelines, visualization |
| `devops-cicd` | DevOps & CI/CD | Pipelines, Docker, Kubernetes, deployments |
| `diagrams` | Diagrams | Mermaid, PlantUML, architecture diagrams |
| `documentation` | Documentation | READMEs, PRDs, API docs, technical writing |
| `frontend-ui` | Frontend & UI | React, Vue, CSS, components, accessibility |
| `git-version-control` | Git & Version Control | Commits, branching, merges, GitHub operations |
| `mcp-development` | MCP Development | Model Context Protocol servers and apps |
| `security` | Security | Audits, vulnerabilities, secure coding |
| `testing` | Testing | Unit tests, integration tests, E2E, TDD |

**Need a new category?** Open an issue to discuss before adding skills.

---

## Validation

When you submit a PR, GitHub Actions will automatically:

1. ✅ Validate JSON syntax
2. ✅ Check against the schema
3. ✅ Verify no duplicate skill IDs
4. ✅ Validate source URLs

If validation fails, check the PR comments for details on what to fix.

### Local Validation

You can validate locally before submitting:

```bash
# Install ajv-cli
npm install -g ajv-cli ajv-formats

# Validate registry against schema
ajv validate -s skills/schema.json -d skills/registry.json
```

---

## Review Process

1. **Automated checks** — Must pass before review
2. **Maintainer review** — We check quality, descriptions, and uniqueness
3. **Feedback** — We may request changes
4. **Merge** — Once approved, your skill goes live!

### Review Timeline

- Most PRs are reviewed within **3-5 business days**
- Simple additions are faster; complex ones may take longer

---

## Questions?

- Open a [GitHub Issue](https://github.com/samueltauil/skills-hub/issues)
- Check existing skills in `registry.json` for examples

---

## License

By contributing to Skills Hub, you agree that your contributions will be licensed under the [MIT License](LICENSE).

Thank you for contributing! 🎉
