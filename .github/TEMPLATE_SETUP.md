# After Using This Template

Congratulations on creating a new repository from the SkillPilot template! Here's what to do next:

## 1. Update Repository Information

- [ ] Update `README.md` with your project name and description
- [ ] Update the `LICENSE` file with your name/organization
- [ ] Customize `.github/skills/copilot-orchestrator/SKILL.md` if needed

## 2. Set Up Your Environment

```bash
# Navigate to skills directory
cd .github/skills/copilot-orchestrator/scripts

# Install dependencies with uv
uv sync
```

## 3. Verify Prerequisites

- [ ] Python 3.11+ installed (`python --version`)
- [ ] uv installed (`uv --version`)
- [ ] GitHub Copilot CLI authenticated (`gh copilot --version`)

## 4. Test the Orchestrator

```bash
uv run python orchestrator.py "list all files in the current directory"
```

## 5. Customize for Your Use Case

### Add Custom Tools
Create new tools in `scripts/custom_tools/` following the patterns in `references/TOOL_PATTERNS.md`.

### Modify Capability Mappings
Edit `references/CAPABILITY_REGISTRY.md` to add domain-specific intent mappings.

### Adjust Token Budgets
Modify `scripts/context_manager.py` to tune compression for your codebase size.

## 6. Delete This File

Once you've completed setup, delete this `TEMPLATE_SETUP.md` file:

```bash
rm .github/TEMPLATE_SETUP.md
```

---

Happy coding with SkillPilot! 🚀
