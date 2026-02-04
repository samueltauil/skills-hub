---
name: copilot-orchestrator
description: Universal development assistant that handles ANY coding task - implement features, build APIs, create components, write code, fix bugs, debug errors, refactor code, write tests, generate documentation, deploy apps, create pipelines, scaffold projects, migrate codebases, optimize performance, review code, and automate workflows. Use this skill for all programming, development, and software engineering requests.
license: MIT
compatibility: Requires Python 3.11+ and uv package manager.
---

# Copilot Orchestrator

A universal meta-skill that transforms **any** development request into orchestrated
GitHub Copilot SDK calls. Whether you need to implement features, fix bugs, write tests,
refactor code, generate documentation, or deploy applications - this orchestrator
handles it all by interpreting your intent and delegating to the appropriate tools.

**Use this skill when you want to:**
- Write, edit, or generate any code
- Fix errors, debug issues, or troubleshoot problems
- Refactor, restructure, or improve existing code
- Create tests, documentation, or configurations
- Deploy, automate, or scaffold projects

**Execution Paths:**
- **Simple tasks** (list files, run tests, git status) → Ephemeral skill spawned instantly
- **Complex tasks** (implement, refactor, debug) → Full SDK session with context compression

## When to Use This Skill

This skill activates automatically when you need to:

| Intent Category | Example Prompts |
|-----------------|-----------------|
| **Implement** | "build a REST API", "create a login form", "add caching layer", "implement user authentication", "make a dashboard component", "write a function to parse JSON", "develop a payment integration", "add a new endpoint", "create a service class", "build the user registration flow" |
| **Analyze** | "review this code", "find security issues", "audit dependencies", "check for bugs", "analyze the architecture", "look for memory leaks", "examine this function", "find unused imports", "search for TODO comments", "what does this code do" |
| **Generate** | "write documentation", "create README", "generate API specs", "make a schema", "create TypeScript types", "generate interfaces", "write JSDoc comments", "create OpenAPI spec", "generate migration scripts", "make a changelog" |
| **Refactor** | "restructure this module", "apply SOLID principles", "extract service", "clean up this code", "simplify this function", "rename variables", "split this file", "improve code quality", "make this more readable", "reduce duplication" |
| **Debug** | "fix this error", "why is this failing", "diagnose performance issue", "solve this bug", "help me debug", "this isn't working", "getting an error", "troubleshoot this issue", "find the problem", "figure out why it crashes" |
| **Test** | "write unit tests", "add integration tests", "improve coverage", "create test cases", "add specs for this function", "write e2e tests", "mock this dependency", "test edge cases", "add assertions", "verify this works" |
| **Deploy** | "create CI/CD pipeline", "dockerize this app", "setup Kubernetes", "configure deployment", "create GitHub Actions workflow", "setup auto-deploy", "create release pipeline", "configure staging environment", "add container support", "setup cloud deployment" |
| **Automate** | "create GitHub Action", "automate releases", "schedule backups", "create a script to", "automate this workflow", "setup pre-commit hooks", "automate code formatting", "create a cron job", "build automation pipeline", "script this process" |
| **Scaffold** | "bootstrap React app", "initialize Python project", "create monorepo", "setup new project", "create starter template", "init Node.js app", "scaffold API server", "create boilerplate", "setup workspace", "generate project structure" |
| **Migrate** | "convert to TypeScript", "upgrade framework", "modernize codebase", "port to Python 3", "update dependencies", "migrate database schema", "convert class to functional", "upgrade React version", "migrate to ESM", "update to latest API" |
| **Optimize** | "improve performance", "reduce bundle size", "optimize queries", "speed up this function", "make this faster", "reduce memory usage", "optimize imports", "improve load time", "cache this data", "minimize API calls" |
| **Files** | "list files", "show directory", "read this file", "find files matching", "search in files", "what files are here", "show me the code", "open the config", "display file contents", "look at the source" |
| **Explain** | "explain this code", "how does this work", "what is this doing", "walk me through", "describe the flow", "help me understand", "clarify this logic", "document this function", "summarize this module", "break down the architecture" |

### Activation Keywords

This skill responds to these common development terms and phrases:

**Action Verbs:** implement, build, create, add, make, develop, write, fix, debug, solve, resolve, refactor, restructure, improve, clean, test, generate, deploy, setup, configure, scaffold, bootstrap, initialize, migrate, convert, upgrade, optimize, analyze, review, audit, check, find, search, explain, show, list, read, edit, modify, change, update, delete

**Problem Indicators:** error, bug, issue, problem, failing, broken, not working, crashes, exception, undefined, null, missing, wrong, incorrect

**Task Objects:** code, function, class, component, module, API, endpoint, service, file, test, documentation, pipeline, workflow, script, project, application, database, schema, type, interface

**Questions:** why, how, what, where, which, can you, could you, help me, I need, I want

## Prerequisites

1. **Python 3.11+** installed and available in PATH
2. **uv** package manager ([installation](https://docs.astral.sh/uv/getting-started/installation/))
3. **GitHub Copilot CLI** installed via `gh extension install github/gh-copilot` or standalone
4. **GitHub Copilot SDK** (`pip install github-copilot-sdk`) - [GitHub Repo](https://github.com/github/copilot-sdk)

## How It Works

### Step 1: Task Classification

When you make a request, the orchestrator classifies it into a capability type:

```python
# The orchestrator maps your intent to an SDK configuration
task_type = classify_task("implement user authentication with OAuth2")
# → TaskType.IMPLEMENT with features: ["oauth2", "authentication", "security"]
```

### Step 2: Context Compression

Large contexts are semantically compressed to fit within token budgets:

```python
# Before: 50,000 tokens of codebase context
# After: 8,000 tokens of relevant, compressed context
compressed = await context_manager.prepare_context(
    task_type=task_type,
    request="add user authentication",
    focus_files=["models.py", "routes.py"],
    budget=TokenBudget(input_max=8000, output_max=4000)
)
```

### Step 3: Dynamic Tool Assembly

Tools are assembled based on what the task requires:

```python
# For "implement feature" tasks, these tools are auto-registered:
tools = tool_factory.for_task(
    task_type=TaskType.IMPLEMENT,
    features=["file_write", "code_analysis", "test_runner"]
)
```

### Step 4: SDK Session Execution

The orchestrator creates a Copilot SDK session with optimal configuration:

```python
session = await client.create_session({
    "model": select_model(task_type),  # gpt-4.1 for code, claude-sonnet-4.5 for reasoning
    "streaming": True,
    "tools": tools,
    "system_message": generate_system_prompt(task_type, compressed.metadata)
})

response = await session.send_and_wait({
    "prompt": build_prompt(original_request, compressed.context)
})
```

### Step 5: Artifact Collection

Generated artifacts (code, docs, configs) are tracked during tool execution and returned in the session info:

```python
# Artifacts are automatically tracked when write_file tool executes
result = await orchestrator.execute(request)
for artifact in result.artifacts:
    print(f"Created: {artifact.path} ({artifact.artifact_type})")
# → Created: src/auth.py (code)
# → Created: tests/test_auth.py (test)
```

## Execution

Run the orchestrator directly:

```bash
# Install dependencies (first time only)
cd .github/skills/copilot-orchestrator/scripts
uv sync

# Execute with a task
uv run python orchestrator.py "implement a REST endpoint for user registration"

# Override task classification
uv run python orchestrator.py --task-type implement "add validation to User model"

# Specify workspace directory
uv run python orchestrator.py --workspace /path/to/project "why is my test failing"

# Resume a previous session
uv run python orchestrator.py --resume session_abc123xyz

# Verbose mode with JSON output (for skill handler)
uv run python orchestrator.py --verbose --output-json "list files"
```

## Configuration

The orchestrator respects environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `COPILOT_MODEL` | `gpt-4.1` | Default model for SDK sessions |
| `COPILOT_TOKEN_BUDGET` | `8000` | Max input tokens per session |
| `COPILOT_STREAMING` | `true` | Enable streaming responses |
| `COPILOT_DEBUG` | `false` | Enable debug logging |

## Context Transfer Protocol

The orchestrator uses a structured context envelope for SDK communication:

```json
{
  "task_id": "01919e17-7c9f-7f0c-8d9a-3b4c5d6e7f8a",
  "task_type": "implement",
  "original_request": "add user authentication",
  "compressed_context": { "chunks": [...], "total_tokens": 4500 },
  "token_budget": {"input_max": 8000, "output_max": 4000, "input_used": 4500},
  "selected_tools": ["read_file", "write_file", "search_code"],
  "model": "gpt-4.1",
  "created_at": "2026-02-04T10:30:00Z"
}
```

See [references/CONTEXT_PROTOCOL.md](references/CONTEXT_PROTOCOL.md) for full specification.

## Extending the Orchestrator

### Adding Custom Tools

Create a new tool in `scripts/custom_tools/`:

```python
from tool_factory import register_tool, ToolSchema

@register_tool(
    name="my_custom_tool",
    description="Does something specialized",
    task_types=[TaskType.IMPLEMENT, TaskType.AUTOMATE]
)
async def my_custom_tool(params: MyParams) -> dict:
    """
    Custom tool implementation.

    Args:
        params: Validated parameters from Pydantic model

    Returns:
        Result dictionary to send back to SDK
    """
    # Your implementation here
    return {"result": "success", "data": ...}
```

### Adding Capability Mappings

Edit [references/CAPABILITY_REGISTRY.md](references/CAPABILITY_REGISTRY.md) to map new
intents to SDK configurations.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Copilot CLI not found" | Install CLI: `gh extension install github/gh-copilot` |
| "Authentication failed" | Run `copilot auth login` |
| "Token budget exceeded" | Reduce context with `--max-context 4000` |
| "Tool execution failed" | Check tool logs in `.github/skills/copilot-orchestrator/logs/` |
| "Session timeout" | Increase timeout with `--timeout 120` |

## References

- [Context Protocol Specification](references/CONTEXT_PROTOCOL.md)
- [Tool Patterns Library](references/TOOL_PATTERNS.md)
- [Capability Registry](references/CAPABILITY_REGISTRY.md)
- [Ephemeral Skill Template](templates/ephemeral_skill.md)

## Architecture

```
scripts/
├── __init__.py          # Package initializer
├── orchestrator.py      # Main entry point, CLI, and SDK bridge
├── context_manager.py   # Semantic compression and token budgeting
├── tool_factory.py      # Dynamic tool schema generation and built-in tools
├── models.py            # Pydantic models for type safety
└── pyproject.toml       # Dependencies (uv)
```

The orchestrator is designed for transparency - all code is heavily commented
to enable understanding, debugging, and extension.
