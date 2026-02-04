---
name: shell-executor
description: Execute shell commands (bash/PowerShell) from natural language requests.
license: MIT
compatibility: Requires Python 3.11+
---

# Shell Executor

A specialized skill for executing shell commands based on natural language.

This skill was **generated from the copilot-orchestrator** as an example of
how ephemeral skills can be persisted for reuse.

## Capabilities

- **list_files**: List directory contents
- **run_command**: Execute arbitrary shell commands
- **check_status**: Check git status, process status, etc.

## Example Requests

| You Say | Command Executed |
|---------|-----------------|
| "list files here" | `ls -la` / `Get-ChildItem` |
| "show all python files" | `find . -name '*.py'` / `Get-ChildItem -Filter *.py -Recurse` |
| "git status" | `git status` |
| "current directory" | `pwd` / `Get-Location` |

## How It Works

```python
# The skill parses natural language into commands
request = "list all javascript files"
command = parse_to_command(request)  
# → "Get-ChildItem -Recurse -Filter *.js" (Windows)
# → "find . -name '*.js'" (Unix)

# Execute and return results
result = subprocess.run(command, capture_output=True)
return {"stdout": result.stdout, "success": result.returncode == 0}
```

## Creating Your Own Shell Skill

To persist an ephemeral shell skill:

```python
from orchestrator import EphemeralSkillSpawner
from pathlib import Path

spawner = EphemeralSkillSpawner(workspace=Path.cwd())

# Create a custom shell skill
spawner.persist_skill("shell", "my-project-commands")
```

This creates `.github/skills/my-project-commands/SKILL.md`.

## Safety Notes

- Commands are sandboxed to the workspace directory
- Timeout of 30 seconds prevents runaway processes
- Only whitelisted command patterns are allowed by default
