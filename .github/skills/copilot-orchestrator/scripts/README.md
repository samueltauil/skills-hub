# Copilot Orchestrator Scripts

This directory contains the Python implementation of the Copilot Orchestrator skill.

## Overview

The orchestrator is a universal meta-skill that transforms any development request into orchestrated GitHub Copilot SDK calls.

## Modules

| File | Description |
|------|-------------|
| `orchestrator.py` | Main entry point, CLI, and SDK bridge |
| `context_manager.py` | Semantic compression and token budgeting |
| `tool_factory.py` | Dynamic tool schema generation and built-in tools |
| `models.py` | Pydantic models for type safety |

## Usage

```bash
# Install dependencies
uv sync

# Execute with a task
uv run python orchestrator.py "implement a REST endpoint"

# With options
uv run python orchestrator.py --task-type implement "add validation"
uv run python orchestrator.py --workspace /path/to/project "fix tests"
uv run python orchestrator.py --verbose --output-json "list files"
```

## Requirements

- Python 3.11+
- uv package manager

## Dependencies

See `pyproject.toml` for the full list of dependencies including:
- `github-copilot-sdk` - Core SDK integration
- `pydantic` - Type-safe data validation
- `structlog` - Structured logging
- `httpx` - Async HTTP client
- `rich` - Terminal output
- `tiktoken` - Token counting
