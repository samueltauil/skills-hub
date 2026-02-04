"""
Pydantic Models for Copilot Orchestrator
=========================================

This module defines all data structures used throughout the orchestrator.
Using Pydantic v2 for:
- Runtime type validation
- JSON serialization/deserialization
- Schema generation for SDK tools
- Clear documentation through type hints

Architecture Note:
-----------------
These models form the "contract" between components:

    ┌─────────────┐     ┌─────────────────┐     ┌─────────────┐
    │  SKILL.md   │────▶│ TaskEnvelope    │────▶│ SDK Session │
    │  (trigger)  │     │ (context xfer)  │     │ (execution) │
    └─────────────┘     └─────────────────┘     └─────────────┘

All context transfer happens through TaskEnvelope, ensuring
consistent serialization and type safety.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator
from uuid_extensions import uuid7


# =============================================================================
# ENUMS - Task and capability classifications
# =============================================================================


class TaskType(str, Enum):
    """
    Classification of development tasks.
    
    Each type maps to specific:
    - SDK model selection (gpt-4.1 vs claude-sonnet-4.5)
    - Tool configurations
    - System prompts
    - Token budget allocations
    
    See CAPABILITY_REGISTRY.md for full mappings.
    """
    
    IMPLEMENT = "implement"      # Build new features, create code
    ANALYZE = "analyze"          # Review, audit, inspect code
    GENERATE = "generate"        # Create docs, specs, configs
    REFACTOR = "refactor"        # Restructure, reorganize, clean
    DEBUG = "debug"              # Fix errors, diagnose issues
    TEST = "test"                # Write tests, improve coverage
    DEPLOY = "deploy"            # CI/CD, containerization, infra
    AUTOMATE = "automate"        # Scripts, workflows, actions
    SCAFFOLD = "scaffold"        # Bootstrap projects, initialize
    MIGRATE = "migrate"          # Convert, upgrade, transform
    OPTIMIZE = "optimize"        # Performance, size, efficiency
    UNKNOWN = "unknown"          # Fallback for unclassified tasks


class ContextPriority(str, Enum):
    """
    Priority levels for context chunks during compression.
    
    Higher priority = more likely to be retained when token budget is tight.
    
    Priority Hierarchy:
    -------------------
    CRITICAL > HIGH > MEDIUM > LOW > MINIMAL
    
    Examples:
    - CRITICAL: Current file being edited, error messages
    - HIGH: Related files, recent changes
    - MEDIUM: Project structure, dependencies
    - LOW: Documentation, historical context
    - MINIMAL: Style guides, general info
    """
    
    CRITICAL = "critical"   # Must include - directly relevant to task
    HIGH = "high"           # Should include - strongly related
    MEDIUM = "medium"       # Include if budget allows
    LOW = "low"             # Include only with excess budget
    MINIMAL = "minimal"     # Only for large context windows


class SessionState(str, Enum):
    """
    State machine for SDK session lifecycle.
    
    State Transitions:
    -----------------
    INITIALIZING ──▶ ACTIVE ──▶ STREAMING ──▶ IDLE ──▶ COMPLETED
                       │                        │
                       └────────▶ ERROR ◀───────┘
                                    │
                                    ▼
                               TERMINATED
    """
    
    INITIALIZING = "initializing"  # Session being created
    ACTIVE = "active"              # Ready to receive messages
    STREAMING = "streaming"        # Currently streaming response
    IDLE = "idle"                  # Waiting for next message
    COMPLETED = "completed"        # Task finished successfully
    ERROR = "error"                # Recoverable error state
    TERMINATED = "terminated"      # Session ended (cleanup done)


# =============================================================================
# TOKEN MANAGEMENT - Budget tracking and allocation
# =============================================================================


class TokenBudget(BaseModel):
    """
    Token budget configuration for SDK sessions.
    
    Tracks input and output token limits to prevent context overflow.
    The orchestrator uses this to decide how aggressively to compress context.
    
    Budget Strategy:
    ---------------
    - Reserve 20% of model's context window for system prompts
    - Allocate remaining 80% split: 60% input, 40% output
    - For gpt-4.1 (128k): input=61,440, output=40,960
    - For typical tasks: input=8,000, output=4,000 (conservative)
    
    Attributes:
        input_max: Maximum tokens for input context
        output_max: Maximum tokens for generated output
        input_used: Tokens consumed by current context
        output_used: Tokens generated so far
        reserved: Tokens reserved for system overhead
    """
    
    input_max: int = Field(default=8000, ge=1000, le=128000)
    output_max: int = Field(default=4000, ge=500, le=32000)
    input_used: int = Field(default=0, ge=0)
    output_used: int = Field(default=0, ge=0)
    reserved: int = Field(default=500, ge=0)  # For system prompts
    
    @property
    def input_available(self) -> int:
        """Remaining input token capacity."""
        return max(0, self.input_max - self.input_used - self.reserved)
    
    @property
    def output_available(self) -> int:
        """Remaining output token capacity."""
        return max(0, self.output_max - self.output_used)
    
    @property
    def utilization(self) -> float:
        """Total budget utilization as percentage (0.0 to 1.0)."""
        total_max = self.input_max + self.output_max
        total_used = self.input_used + self.output_used
        return total_used / total_max if total_max > 0 else 0.0
    
    def can_fit(self, tokens: int) -> bool:
        """Check if the given token count fits in remaining input budget."""
        return tokens <= self.input_available
    
    def consume_input(self, tokens: int) -> None:
        """Record tokens consumed from input budget."""
        self.input_used += tokens
    
    def consume_output(self, tokens: int) -> None:
        """Record tokens generated to output."""
        self.output_used += tokens


# =============================================================================
# CONTEXT CHUNKS - Units of context being transferred
# =============================================================================


class ContextChunk(BaseModel):
    """
    A discrete unit of context for SDK transfer.
    
    Context is broken into chunks for:
    - Priority-based inclusion decisions
    - Accurate token counting per chunk
    - Selective compression
    - Traceability (source tracking)
    
    Chunk Types:
    -----------
    - file: Source code file (full or partial)
    - snippet: Code extract with line numbers
    - error: Error message or stack trace
    - structure: Project structure (dirs, files)
    - dependency: Package/import information
    - history: Previous conversation turns
    - metadata: Project config, settings
    
    Attributes:
        chunk_id: Unique identifier for this chunk
        content: The actual text content
        source: Where this content came from (file path, "user input", etc.)
        chunk_type: Classification of content type
        priority: Importance for inclusion decisions
        token_count: Pre-computed token count
        metadata: Additional context (line numbers, language, etc.)
    """
    
    chunk_id: str = Field(default_factory=lambda: str(uuid7()))
    content: str = Field(min_length=1)
    source: str = Field(description="Origin of this content")
    chunk_type: Literal["file", "snippet", "error", "structure", "dependency", "history", "metadata"]
    priority: ContextPriority = Field(default=ContextPriority.MEDIUM)
    token_count: int = Field(default=0, ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)
    
    @field_validator("content")
    @classmethod
    def strip_excessive_whitespace(cls, v: str) -> str:
        """Normalize whitespace to reduce token waste."""
        # Collapse multiple blank lines into two max
        import re
        return re.sub(r'\n{4,}', '\n\n\n', v)


class CompressedContext(BaseModel):
    """
    Result of context compression.
    
    Contains the compressed context ready for SDK transfer,
    along with metadata about what was included/excluded.
    
    This enables:
    - Transparency: Know exactly what context the SDK sees
    - Debugging: Understand why certain code wasn't included
    - Optimization: Track compression effectiveness
    
    Attributes:
        chunks: List of included context chunks
        total_tokens: Sum of all chunk token counts
        compression_ratio: Original tokens / compressed tokens
        excluded_sources: Sources that didn't fit in budget
        summary: Optional human-readable summary of context
    """
    
    chunks: list[ContextChunk] = Field(default_factory=list)
    total_tokens: int = Field(default=0, ge=0)
    compression_ratio: float = Field(default=1.0, ge=0.0)
    excluded_sources: list[str] = Field(default_factory=list)
    summary: str | None = Field(default=None)
    
    def to_prompt_text(self) -> str:
        """
        Serialize all chunks into a single prompt string.
        
        Format:
        -------
        === [source] ===
        [content]
        
        === [source2] ===
        [content2]
        ...
        """
        parts = []
        for chunk in self.chunks:
            header = f"=== {chunk.source} ({chunk.chunk_type}) ==="
            parts.append(f"{header}\n{chunk.content}")
        return "\n\n".join(parts)


# =============================================================================
# TASK ENVELOPE - The complete context transfer unit
# =============================================================================


class TaskEnvelope(BaseModel):
    """
    Complete context package for SDK session.
    
    The TaskEnvelope is THE central data structure for context transfer.
    Everything needed to execute a task is serialized into this envelope,
    enabling:
    
    1. Session Persistence: Save/restore mid-task
    2. Debugging: Full traceability of what context was used
    3. Audit Trail: Record of all orchestrator decisions
    4. Error Recovery: Restore from last known good state
    
    Lifecycle:
    ---------
    1. Created when task is received
    2. Populated with compressed context
    3. Attached tools and configuration
    4. Sent to SDK session
    5. Updated with results
    6. Archived for debugging
    
    Example JSON:
    ------------
    {
        "task_id": "01919e17-7c9f-7f0c-8d9a-3b4c5d6e7f8a",
        "task_type": "implement",
        "original_request": "add user authentication",
        "compressed_context": { ... },
        "token_budget": {"input_max": 8000, "output_max": 4000},
        "selected_tools": ["file_write", "code_analysis"],
        "model": "gpt-4.1",
        "created_at": "2026-02-04T10:30:00Z"
    }
    
    Attributes:
        task_id: Unique identifier (UUID7 for time-ordering)
        task_type: Classified task type
        original_request: User's raw input
        compressed_context: Processed context ready for SDK
        token_budget: Token limits for this task
        selected_tools: Tool names to register with SDK
        model: LLM model to use
        system_prompt: Custom system message (optional)
        artifacts: Output file paths (populated after execution)
        restoration_point: For resuming interrupted tasks
        created_at: Timestamp for ordering
        metadata: Extension point for custom data
    """
    
    task_id: str = Field(default_factory=lambda: str(uuid7()))
    task_type: TaskType = Field(default=TaskType.UNKNOWN)
    original_request: str = Field(min_length=1)
    compressed_context: CompressedContext = Field(default_factory=CompressedContext)
    token_budget: TokenBudget = Field(default_factory=TokenBudget)
    selected_tools: list[str] = Field(default_factory=list)
    model: str = Field(default="gpt-4.1")
    system_prompt: str | None = Field(default=None)
    artifacts: list[str] = Field(default_factory=list)
    restoration_point: dict[str, Any] | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)
    
    def to_sdk_config(self) -> dict[str, Any]:
        """
        Convert envelope to SDK session configuration.
        
        Returns:
            Dictionary compatible with CopilotClient.create_session()
        """
        config: dict[str, Any] = {
            "model": self.model,
            "streaming": True,
        }
        
        if self.system_prompt:
            config["system_message"] = {"content": self.system_prompt}
        
        return config
    
    def build_prompt(self) -> str:
        """
        Construct the final prompt string for SDK.
        
        Combines compressed context with original request in a
        format optimized for LLM understanding.
        
        Returns:
            Complete prompt ready for session.send()
        """
        parts = []
        
        # Add context section if available
        if self.compressed_context.chunks:
            parts.append("## Context\n")
            parts.append(self.compressed_context.to_prompt_text())
            parts.append("\n")
        
        # Add the actual request
        parts.append("## Request\n")
        parts.append(self.original_request)
        
        return "\n".join(parts)


# =============================================================================
# ARTIFACTS - Output tracking
# =============================================================================


class ArtifactType(str, Enum):
    """Types of artifacts generated by the orchestrator."""
    
    CODE = "code"              # Source code files
    TEST = "test"              # Test files
    DOCUMENTATION = "documentation"  # Markdown, docs
    CONFIGURATION = "configuration"  # Config files (yaml, json, toml)
    SCRIPT = "script"          # Executable scripts
    DIAGRAM = "diagram"        # Visual diagrams (mermaid, etc.)
    OTHER = "other"            # Uncategorized


class Artifact(BaseModel):
    """
    A generated output from SDK execution.
    
    Artifacts are tracked for:
    - User presentation (show what was created)
    - Testing (verify generated code)
    - Rollback (undo changes if needed)
    
    Attributes:
        artifact_id: Unique identifier
        artifact_type: Classification
        path: File system path (relative to workspace)
        content: The generated content
        language: Programming language (if applicable)
        created_at: Generation timestamp
    """
    
    artifact_id: str = Field(default_factory=lambda: str(uuid7()))
    artifact_type: ArtifactType = Field(default=ArtifactType.OTHER)
    path: Path
    content: str
    language: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    @property
    def extension(self) -> str:
        """File extension without the dot."""
        return self.path.suffix.lstrip(".")


# =============================================================================
# SESSION TRACKING - SDK session state
# =============================================================================


class SessionInfo(BaseModel):
    """
    Metadata about an SDK session.
    
    Used for:
    - Session persistence and resume
    - Debugging session issues
    - Monitoring session health
    
    Attributes:
        session_id: SDK session identifier
        state: Current lifecycle state
        task: Associated task envelope
        task_id: Associated task envelope ID
        model: LLM model in use
        turn_count: Number of message exchanges
        total_input_tokens: Cumulative input tokens
        total_output_tokens: Cumulative output tokens
        started_at: Session creation time
        ended_at: Session end time
        last_activity: Last message timestamp
        artifacts: Output artifacts from the session
        error_message: Last error (if state is ERROR)
    """
    
    session_id: str
    state: SessionState = Field(default=SessionState.INITIALIZING)
    task: "TaskEnvelope | None" = Field(default=None)
    task_id: str | None = Field(default=None)
    model: str = Field(default="gpt-4.1")
    turn_count: int = Field(default=0, ge=0)
    total_input_tokens: int = Field(default=0, ge=0)
    total_output_tokens: int = Field(default=0, ge=0)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: datetime | None = Field(default=None)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    artifacts: list["Artifact"] | None = Field(default=None)
    error_message: str | None = Field(default=None)
    
    def update_activity(self) -> None:
        """Mark session as recently active."""
        self.last_activity = datetime.utcnow()
    
    def record_turn(self, input_tokens: int, output_tokens: int) -> None:
        """Record a completed message exchange."""
        self.turn_count += 1
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.update_activity()


# =============================================================================
# TOOL DEFINITIONS - For dynamic tool registration
# =============================================================================


class ToolParameter(BaseModel):
    """
    A parameter in a tool's JSON schema.
    
    Attributes:
        name: Parameter name
        param_type: JSON schema type (string, number, boolean, etc.)
        description: Help text for the LLM
        required: Whether this parameter must be provided
        default: Default value if not provided
        enum: Allowed values (for constrained choices)
    """
    
    name: str = Field(min_length=1)
    param_type: str = Field(default="string")
    description: str = Field(default="")
    required: bool = Field(default=False)
    default: Any = Field(default=None)
    enum: list[str] | None = Field(default=None)
    
    def to_json_schema(self) -> dict[str, Any]:
        """Convert to JSON Schema property definition."""
        schema: dict[str, Any] = {
            "type": self.param_type,
            "description": self.description,
        }
        if self.default is not None:
            schema["default"] = self.default
        if self.enum:
            schema["enum"] = self.enum
        return schema


class ToolDefinition(BaseModel):
    """
    Complete tool definition for SDK registration.
    
    This generates the JSON schema that tells the LLM:
    - What the tool does
    - What parameters it accepts
    - How to call it
    
    Example:
    -------
    ToolDefinition(
        name="write_file",
        description="Write content to a file",
        parameters=[
            ToolParameter(name="path", param_type="string", required=True),
            ToolParameter(name="content", param_type="string", required=True),
        ]
    )
    
    Attributes:
        name: Unique tool identifier
        description: What the tool does (shown to LLM)
        parameters: List of accepted parameters
        task_types: Which task types this tool supports
        requires_confirmation: Ask user before executing
    """
    
    name: str = Field(min_length=1, pattern=r"^[a-z_][a-z0-9_]*$")
    description: str = Field(min_length=10)
    parameters: list[ToolParameter] = Field(default_factory=list)
    task_types: list[TaskType] = Field(default_factory=list)
    requires_confirmation: bool = Field(default=False)
    
    def to_json_schema(self) -> dict[str, Any]:
        """
        Generate JSON schema for SDK tool registration.
        
        Returns:
            Schema compatible with defineTool() / define_tool()
        """
        properties = {p.name: p.to_json_schema() for p in self.parameters}
        required = [p.name for p in self.parameters if p.required]
        
        return {
            "type": "object",
            "properties": properties,
            "required": required,
        }
