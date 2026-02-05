"""
Copilot Orchestrator - Universal Skill for GitHub Copilot SDK
=============================================================

This package provides a meta-skill that can adapt to any development task
by orchestrating GitHub Copilot SDK calls with sophisticated context management.

Modules:
--------
- models: Data structures for type-safe context transfer
- context_manager: Semantic compression and token budgeting
- tool_factory: Dynamic tool generation and registration
- orchestrator: Main SDK bridge and execution engine

Quick Start:
-----------
    from orchestrator import Orchestrator, OrchestratorConfig
    
    config = OrchestratorConfig(
        workspace=Path("/my/project"),
        max_tokens=16000
    )
    
    orch = Orchestrator(config)
    result = await orch.execute("implement user authentication")

CLI Usage:
---------
    python -m orchestrator "implement user authentication"
    python -m orchestrator --task-type debug "fix the login error"

For detailed documentation, see the reference files in ../references/
"""

from pathlib import Path

__version__ = "1.0.0"
__author__ = "Copilot Orchestrator"

# Expose main classes at package level
from .models import (
    TaskType,
    ContextPriority,
    SessionState,
    TokenBudget,
    ContextChunk,
    CompressedContext,
    TaskEnvelope,
    Artifact,
    SessionInfo,
    ToolParameter,
    ToolDefinition,
)

from .context_manager import (
    TokenCounter,
    ContextGatherer,
    ContextPrioritizer,
    ContextCompressor,
    ContextManager,
    ContextCheckpoint,
)

from .tool_factory import (
    ToolRegistry,
    ToolEntry,
    ToolFactory,
    DynamicToolBuilder,
    register_tool,
)

from .orchestrator import (
    TaskClassifier,
    CopilotClient,
    ResponseRenderer,
    Orchestrator,
    OrchestratorConfig,
)

__all__ = [
    # Version
    "__version__",
    
    # Models
    "TaskType",
    "ContextPriority",
    "SessionState",
    "TokenBudget",
    "ContextChunk",
    "CompressedContext",
    "TaskEnvelope",
    "Artifact",
    "SessionInfo",
    "ToolParameter",
    "ToolDefinition",
    
    # Context Manager
    "TokenCounter",
    "ContextGatherer",
    "ContextPrioritizer",
    "ContextCompressor",
    "ContextManager",
    "ContextCheckpoint",
    
    # Tool Factory
    "ToolRegistry",
    "ToolEntry",
    "ToolFactory",
    "DynamicToolBuilder",
    "register_tool",
    
    # Orchestrator
    "TaskClassifier",
    "CopilotClient",
    "ResponseRenderer",
    "Orchestrator",
    "OrchestratorConfig",
]
