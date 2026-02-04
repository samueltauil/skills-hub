# Context Protocol Specification

> **Version:** 1.0.0  
> **Last Updated:** 2024

This document defines the context transfer protocol for the Copilot Orchestrator skill. 
It specifies how context is gathered, compressed, and transmitted to the SDK for optimal LLM performance.

---

## Overview

Context is the critical bridge between user intent and LLM understanding. The protocol ensures:

1. **Relevance**: Only pertinent context reaches the model
2. **Efficiency**: Token budget is optimized through compression
3. **Recoverability**: Sessions can be resumed via checkpoints
4. **Transparency**: Context decisions are inspectable and debuggable

```
┌────────────────────────────────────────────────────────────────────┐
│                     CONTEXT FLOW                                   │
│                                                                    │
│   User Intent ──▶ [Gatherer] ──▶ [Prioritizer] ──▶ [Compressor]   │
│                        │              │                 │          │
│                        ▼              ▼                 ▼          │
│                   Raw Chunks    Scored Chunks    Compressed        │
│                   (unlimited)   (ranked)         (within budget)   │
│                                                        │          │
│                                                        ▼          │
│                                                 Prompt Ready       │
└────────────────────────────────────────────────────────────────────┘
```

---

## Context Envelope Structure

The `TaskEnvelope` is the canonical data structure for transferring task context:

```python
@dataclass
class TaskEnvelope:
    # Classification
    task_type: TaskType
    
    # User Input
    user_request: str          # Natural language request
    original_input: str        # Unprocessed input (for history)
    
    # Context
    context: CompressedContext # Gathered & compressed context
    
    # Execution
    tools: list[ToolDefinition]  # Available tools
    artifacts: list[Artifact]    # Generated outputs
    
    # Metadata
    session_id: str
    created_at: datetime
    token_budget: TokenBudget
```

### Token Budget Allocation

Default allocation strategy:

| Component | Percentage | Default Tokens |
|-----------|------------|----------------|
| System prompt | 10% | 800 |
| Context | 50% | 4,000 |
| User request | 10% | 800 |
| Response buffer | 30% | 2,400 |
| **Total** | 100% | 8,000 |

Override via:
```python
envelope.token_budget = TokenBudget(
    total=16000,
    input_allocation_pct=0.7
)
```

---

## Context Chunks

A `ContextChunk` represents a discrete unit of context:

```python
@dataclass
class ContextChunk:
    content: str           # The actual content
    source: str            # file path, url, "workspace", etc.
    chunk_type: str        # "file", "structure", "dependency", "history"
    priority: ContextPriority
    tokens: int            # Pre-computed token count
    metadata: dict         # Additional info (language, last_modified, etc.)
```

### Priority Levels

| Priority | Score | Use Case |
|----------|-------|----------|
| CRITICAL | 1000 | Must include (open file, error location) |
| HIGH | 800 | Strongly relevant (related files, recent changes) |
| MEDIUM | 500 | Useful (utility files, configs) |
| LOW | 200 | Nice to have (documentation, examples) |
| MINIMAL | 100 | Filler (indirect dependencies) |

---

## Gathering Strategy

The `ContextGatherer` collects context based on task type:

### Task-Specific Gathering

| Task Type | Gather Priority |
|-----------|-----------------|
| IMPLEMENT | Target file/location, interfaces, related files, tests |
| DEBUG | Error location, stack trace files, recent changes |
| REFACTOR | File to refactor, dependents, test coverage |
| TEST | Module under test, existing tests, fixtures |
| ANALYZE | Full codebase structure, dependencies, patterns |

### Gathering Functions

```python
class ContextGatherer:
    async def gather_files(
        self,
        patterns: list[str],
        max_files: int = 50
    ) -> list[ContextChunk]:
        """Gather files matching glob patterns."""
        
    async def gather_structure(
        self,
        depth: int = 3
    ) -> ContextChunk:
        """Gather workspace directory structure."""
        
    async def gather_dependencies(self) -> ContextChunk:
        """Analyze and gather dependency information."""
        
    async def gather_git_context(
        self,
        commits: int = 5
    ) -> list[ContextChunk]:
        """Gather recent git history."""
```

---

## Prioritization Algorithm

The `ContextPrioritizer` scores and ranks chunks:

```python
def score_chunk(self, chunk: ContextChunk, envelope: TaskEnvelope) -> float:
    """
    Score formula:
    
    base_score = PRIORITY_BASE[chunk.priority]
    
    modifiers:
        + task_relevance_boost (if chunk matches task type patterns)
        + recency_boost (if recently modified)
        + mention_boost (if referenced in user request)
        - size_penalty (for very large chunks)
    
    final_score = base_score + sum(modifiers)
    """
```

### Task Type Boosters

| Task Type | Boost Pattern | Bonus |
|-----------|---------------|-------|
| DEBUG | Error/exception files | +300 |
| TEST | Test files, fixtures | +250 |
| IMPLEMENT | Target module/class | +400 |
| REFACTOR | Dependencies | +200 |

---

## Compression Strategy

The `ContextCompressor` fits context within token budget:

### Algorithm

```python
def compress(chunks: list[ContextChunk], budget: int) -> CompressedContext:
    """
    1. Sort chunks by score (descending)
    2. Initialize compressed = []
    3. For each chunk:
       a. If fits in remaining budget:
          - Include fully
       b. Else if partially fits and is code:
          - Apply smart truncation (keep imports, signatures)
       c. Else:
          - Skip
    4. Return compressed context with utilization metrics
    """
```

### Smart Truncation

For code files that don't fit fully:

1. **Keep structure** - Imports, class signatures, function signatures
2. **Remove bodies** - Replace with `# ... (N lines)`
3. **Preserve context** - Keep docstrings and type hints
4. **Add summary** - Note what was truncated

Example:
```python
# Original (500 tokens)
import os
from typing import List

class UserService:
    """Manages user operations."""
    
    def __init__(self, db: Database):
        self.db = db
        self._cache = {}
        # ... lots of init code
    
    def get_user(self, user_id: str) -> User:
        """Fetch user by ID."""
        # ... implementation
        return user

# Truncated (150 tokens)
import os
from typing import List

class UserService:
    """Manages user operations."""
    
    def __init__(self, db: Database): ...  # 15 lines
    
    def get_user(self, user_id: str) -> User:
        """Fetch user by ID."""
        ...  # 10 lines
```

---

## Session Checkpoints

Enable resume capability via `ContextCheckpoint`:

### Checkpoint Structure

```json
{
  "session_id": "session_abc123",
  "timestamp": "2024-01-15T10:30:00Z",
  "task_type": "implement",
  "user_request": "add user authentication",
  "state": "running",
  "context_summary": {
    "chunks_included": 12,
    "tokens_used": 3500,
    "utilization": 0.875
  },
  "artifacts": [
    {"type": "file", "path": "src/auth.py"}
  ],
  "conversation_history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

### Checkpoint API

```python
checkpoint = ContextCheckpoint(storage_dir=Path(".copilot/sessions"))

# Save
checkpoint.save(session_id, {
    "task_type": envelope.task_type.value,
    "user_request": envelope.user_request,
    "context": envelope.context.model_dump(),
    "artifacts": [a.model_dump() for a in envelope.artifacts]
})

# Restore
state = checkpoint.restore(session_id)
```

---

## Prompt Assembly

The `build_prompt()` method assembles the final prompt:

```python
def build_prompt(envelope: TaskEnvelope) -> str:
    """
    Structure:
    
    1. Context Header
       "Here is the relevant context for your task:"
    
    2. Workspace Structure (if available)
       "## Project Structure\n{tree}"
    
    3. File Contents (prioritized)
       "## {filename}\n```{lang}\n{content}\n```"
    
    4. Additional Context
       "## Dependencies\n{deps}"
    
    5. User Request
       "---\n## Request\n{request}"
    
    6. Task Instructions
       "As a {task_type} task, please..."
    """
```

---

## Best Practices

### Do ✓

- **Pre-compute tokens** - Count once, reference many times
- **Chunk intelligently** - Split large files at logical boundaries
- **Track sources** - Always know where context came from
- **Measure utilization** - Log how much budget was used
- **Handle failures** - Gracefully degrade if gathering fails

### Don't ✗

- **Over-gather** - Only collect what you need
- **Ignore limits** - Respect token budgets strictly
- **Mix concerns** - Keep chunks single-purpose
- **Forget metadata** - Source info enables debugging
- **Block on I/O** - Use async for file operations

---

## Debugging Context Issues

### Common Problems

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Model misunderstands request | Insufficient context | Increase budget, adjust priorities |
| Slow response | Too much context | Reduce max_files, increase compression |
| Missing file content | File not gathered | Check glob patterns, add explicit paths |
| Truncated important code | Wrong prioritization | Boost priority for critical files |

### Debug Logging

Enable verbose context logging:
```python
import structlog
structlog.configure(
    processors=[structlog.processors.JSONRenderer()],
)

# In your code
logger.debug(
    "context_compressed",
    chunks_in=len(raw_chunks),
    chunks_out=len(compressed.chunks),
    utilization=compressed.utilization
)
```

---

## Extension Points

### Custom Gatherers

```python
class CustomGatherer(ContextGatherer):
    async def gather_api_docs(self, openapi_path: str) -> ContextChunk:
        """Gather OpenAPI specification as context."""
        spec = await self._read_file(openapi_path)
        return ContextChunk(
            content=self._summarize_openapi(spec),
            source=openapi_path,
            chunk_type="api_spec",
            priority=ContextPriority.HIGH,
            tokens=self.counter.count(spec)
        )
```

### Custom Prioritizers

```python
class DomainPrioritizer(ContextPrioritizer):
    def score_chunk(self, chunk: ContextChunk, envelope: TaskEnvelope) -> float:
        score = super().score_chunk(chunk, envelope)
        
        # Boost domain-specific files
        if "domain/models" in chunk.source:
            score += 200
        
        return score
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024 | Initial specification |
