#!/usr/bin/env python3
"""
Copilot Orchestrator - Universal Skill Handler
==============================================

This orchestrator is invoked by GitHub Copilot when the SKILL.md definition
matches a user's request. It acts as a "skill factory" that can:

1. Execute tasks directly via Copilot SDK
2. Spawn ephemeral specialized skills for specific operations
3. Delegate to existing skills in the repository

Invocation Flow:
---------------

    User asks Copilot          Copilot matches            Orchestrator
    "list files here"  ──────▶ SKILL.md triggers ──────▶ handles request
                                                               │
                               ┌───────────────────────────────┼───────────┐
                               │                               ▼           │
                               │  ┌─────────────────────────────────────┐  │
                               │  │         ORCHESTRATOR DECIDES        │  │
                               │  └──────────┬──────────────┬───────────┘  │
                               │             │              │              │
                               │      ┌──────┴─────┐ ┌──────┴──────┐      │
                               │      ▼            │ │             ▼      │
                               │  ┌────────┐       │ │    ┌────────────┐  │
                               │  │SDK Call│       │ │    │Spawn Skill │  │
                               │  │Direct  │       │ │    │(ephemeral) │  │
                               │  └────────┘       │ │    └────────────┘  │
                               │                   │ │                    │
                               │                   ▼ ▼                    │
                               │             ┌──────────┐                 │
                               │             │  Result  │                 │
                               │             └──────────┘                 │
                               └──────────────────────────────────────────┘

The orchestrator may spawn specialized skills like:
- Shell executor (bash/powershell commands)
- File operations (read/write/search)
- Code analyzer (AST parsing, dependency analysis)
- Test runner (execute and report tests)

Usage Modes:
-----------
    # Mode 1: Invoked by Copilot (skill handler mode)
    # Copilot calls this when SKILL.md matches
    python orchestrator.py --skill-handler --request "list files in src/"
    
    # Mode 2: CLI for testing/debugging
    python orchestrator.py "implement a REST API for user management"
    
    # Mode 3: As a Python module
    from orchestrator import Orchestrator
    
    orch = Orchestrator(workspace=Path.cwd())
    result = await orch.execute("list files in current directory")
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncIterator, Callable

import structlog
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax

# Local imports
from models import (
    TaskType,
    TaskEnvelope,
    SessionState,
    SessionInfo,
    Artifact,
    CompressedContext
)
from context_manager import ContextManager, ContextCheckpoint
from tool_factory import ToolFactory, ToolEntry

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

# Rich console for output
console = Console()


# =============================================================================
# TASK CLASSIFIER
# =============================================================================


class TaskClassifier:
    """
    Classify user intent into task types.
    
    Uses keyword matching with confidence scoring to determine
    the most likely task type from user input.
    
    The classifier looks for:
    - Action keywords (implement, test, debug, etc.)
    - Domain keywords (API, database, authentication, etc.)
    - Context clues from the workspace
    """
    
    # Keyword mappings for each task type
    TASK_KEYWORDS: dict[TaskType, list[str]] = {
        TaskType.IMPLEMENT: [
            "implement", "create", "add", "build", "make", "write",
            "develop", "code", "feature", "new", "endpoint", "function"
        ],
        TaskType.ANALYZE: [
            "analyze", "review", "inspect", "check", "examine", "audit",
            "understand", "explain", "what does", "how does", "find"
        ],
        TaskType.REFACTOR: [
            "refactor", "improve", "optimize", "clean", "restructure",
            "simplify", "reorganize", "extract", "rename", "move"
        ],
        TaskType.DEBUG: [
            "debug", "fix", "error", "bug", "issue", "problem",
            "broken", "failing", "crash", "exception", "not working"
        ],
        TaskType.TEST: [
            "test", "tests", "testing", "spec", "coverage", "unit",
            "integration", "e2e", "assert", "verify", "validate"
        ],
        TaskType.GENERATE: [
            "generate", "scaffold", "template", "boilerplate", "starter",
            "init", "setup", "bootstrap", "create project"
        ],
        TaskType.DEPLOY: [
            "deploy", "release", "publish", "ship", "production",
            "staging", "ci/cd", "pipeline", "docker", "kubernetes"
        ],
        TaskType.AUTOMATE: [
            "automate", "script", "workflow", "action", "schedule",
            "cron", "batch", "pipeline", "process"
        ],
        TaskType.SCAFFOLD: [
            "scaffold", "structure", "layout", "architecture", "setup",
            "directory", "project structure", "folder"
        ],
        TaskType.MIGRATE: [
            "migrate", "upgrade", "convert", "port", "transition",
            "switch", "move to", "update from", "replace"
        ],
        TaskType.OPTIMIZE: [
            "optimize", "performance", "speed", "fast", "slow",
            "memory", "cpu", "efficient", "bottleneck", "profile"
        ]
    }
    
    def classify(self, input_text: str) -> tuple[TaskType, float]:
        """
        Classify input text into a task type.
        
        Args:
            input_text: User's request
            
        Returns:
            Tuple of (TaskType, confidence 0.0-1.0)
        """
        input_lower = input_text.lower()
        scores: dict[TaskType, float] = {}
        
        for task_type, keywords in self.TASK_KEYWORDS.items():
            score = 0.0
            for keyword in keywords:
                if keyword in input_lower:
                    # Give more weight to longer keywords (more specific)
                    weight = len(keyword) / 10.0
                    score += weight
            scores[task_type] = score
        
        # Get the highest scoring type
        if not scores or max(scores.values()) == 0:
            # Default to IMPLEMENT if no keywords match
            return TaskType.IMPLEMENT, 0.5
        
        best_type = max(scores, key=lambda t: scores[t])
        max_score = scores[best_type]
        
        # Normalize confidence (cap at 1.0)
        confidence = min(1.0, max_score / 3.0)
        
        logger.info(
            "task_classified",
            task_type=best_type.value,
            confidence=confidence,
            top_scores={t.value: round(s, 2) for t, s in sorted(
                scores.items(), key=lambda x: x[1], reverse=True
            )[:3]}
        )
        
        return best_type, confidence


# =============================================================================
# SDK CLIENT WRAPPER
# =============================================================================


# Auto-detect Copilot CLI path if not set
def _find_copilot_cli() -> str | None:
    """Find the GitHub Copilot CLI executable."""
    # Check official SDK env var first
    cli_path = os.environ.get("COPILOT_CLI_PATH")
    if cli_path and Path(cli_path).exists():
        return cli_path
    
    # Common locations to check
    locations = []
    
    # Windows: npm global install
    if sys.platform == "win32":
        npm_dir = os.environ.get("APPDATA", "")
        if npm_dir:
            locations.extend([
                Path(npm_dir) / "npm" / "copilot.cmd",
                Path(npm_dir) / "npm" / "copilot.ps1",
            ])
    else:
        # Unix: npm global install
        locations.extend([
            Path.home() / ".npm-global" / "bin" / "copilot",
            Path("/usr/local/bin/copilot"),
            Path.home() / ".local" / "bin" / "copilot",
        ])
    
    for loc in locations:
        if loc.exists():
            return str(loc)
    
    return None

# Set CLI path if found (using official SDK env var name)
_cli_path = _find_copilot_cli()
if _cli_path and not os.environ.get("COPILOT_CLI_PATH"):
    os.environ["COPILOT_CLI_PATH"] = _cli_path
    logger.debug("copilot_cli_found", path=_cli_path)

# Check if the official GitHub Copilot SDK is available
# See: https://github.com/github/copilot-sdk
try:
    from copilot import CopilotClient as SDKCopilotClient, define_tool, Tool
    _SDK_AVAILABLE = True
except ImportError:
    _SDK_AVAILABLE = False
    SDKCopilotClient = None
    define_tool = None
    Tool = None
    logger.debug("github_copilot_sdk_not_available", message="Running in mock mode")


class CopilotClient:
    """
    Wrapper around the official GitHub Copilot SDK.
    
    Uses the SDK from https://github.com/github/copilot-sdk which provides:
    - JSON-RPC communication with Copilot CLI
    - Session management with streaming support
    - Tool definition and execution
    
    Handles:
    - SDK client lifecycle (start/stop)
    - Session creation and management
    - Tool registration via @define_tool or Tool class
    - Event-based streaming with async iteration
    - Error recovery with fallback to mock mode
    
    Environment Variables:
        COPILOT_MOCK_MODE: Set to "true" to force mock mode
        GITHUB_COPILOT_MODEL: Model to use (default: gpt-4o)
        COPILOT_CLI_PATH: Path to Copilot CLI executable
    """
    
    def __init__(self, mock_mode: bool | None = None) -> None:
        """
        Initialize the Copilot client.
        
        Args:
            mock_mode: Force mock mode if True. If None, auto-detect.
        """
        self._session_id: str | None = None
        self._tools: list[dict[str, Any]] = []
        self._tool_handlers: dict[str, Callable[..., Any]] = {}
        self._history: list[dict[str, Any]] = []
        self._system_prompt: str | None = None
        
        # Official SDK objects
        self._sdk_client: Any = None  # SDKCopilotClient instance
        self._sdk_session: Any = None  # Session from create_session()
        
        # Determine mode
        if mock_mode is not None:
            self._mock_mode = mock_mode
        else:
            env_mock = os.environ.get("COPILOT_MOCK_MODE", "").lower()
            self._mock_mode = env_mock == "true" or not _SDK_AVAILABLE
        
        logger.info(
            "copilot_client_initialized",
            mock_mode=self._mock_mode,
            sdk_available=_SDK_AVAILABLE
        )
    
    def set_tool_handlers(self, handlers: dict[str, Callable[..., Any]]) -> None:
        """
        Set tool execution handlers for SDK mode.
        
        Args:
            handlers: Dict mapping tool names to async handler functions
        """
        self._tool_handlers = handlers
        
    async def create_session(
        self,
        tools: list[dict[str, Any]],
        system_prompt: str | None = None
    ) -> str:
        """
        Create a new Copilot SDK session.
        
        Args:
            tools: Tool definitions in SDK format
            system_prompt: Optional system prompt
            
        Returns:
            Session ID
        """
        import uuid
        self._session_id = str(uuid.uuid4())
        self._tools = tools
        self._history = []
        self._system_prompt = system_prompt
        
        if system_prompt:
            self._history.append({
                "role": "system",
                "content": system_prompt
            })
        
        if not self._mock_mode and _SDK_AVAILABLE and SDKCopilotClient is not None:
            try:
                # Create SDK tools from tool definitions
                sdk_tools = self._create_sdk_tools()
                
                model_name = os.environ.get("GITHUB_COPILOT_MODEL", "gpt-4o")
                
                # Initialize the SDK client with CLI path
                sdk_config: dict[str, Any] = {
                    "log_level": "warning" if not os.environ.get("COPILOT_DEBUG") else "debug",
                }
                
                # Pass CLI path explicitly if found
                if _cli_path:
                    sdk_config["cli_path"] = _cli_path
                
                self._sdk_client = SDKCopilotClient(sdk_config)
                await self._sdk_client.start()
                
                # Create session with configuration
                session_config: dict[str, Any] = {
                    "model": model_name,
                    "streaming": True,
                }
                
                # Add system message if provided
                if system_prompt:
                    session_config["system_message"] = {
                        "content": system_prompt
                    }
                
                # Add tools if any registered
                if sdk_tools:
                    session_config["tools"] = sdk_tools
                
                self._sdk_session = await self._sdk_client.create_session(session_config)
                
                logger.info(
                    "sdk_session_created",
                    session_id=self._session_id,
                    tool_count=len(sdk_tools),
                    model=model_name
                )
                
            except Exception as e:
                logger.error("sdk_session_creation_failed", error=str(e))
                # Fall back to mock mode
                self._mock_mode = True
                self._sdk_client = None
                self._sdk_session = None
                logger.info(
                    "fallback_to_mock_session",
                    session_id=self._session_id,
                    tool_count=len(tools)
                )
        else:
            logger.info(
                "mock_session_created",
                session_id=self._session_id,
                tool_count=len(tools)
            )
        
        return self._session_id
    
    def _create_sdk_tools(self) -> list[Any]:
        """
        Create SDK-compatible Tool objects from registered tools.
        
        The official SDK supports two ways to define tools:
        1. @define_tool decorator with Pydantic models
        2. Tool class with manual schema definition
        
        We use the Tool class for flexibility.
        """
        if Tool is None:
            return []
            
        sdk_tools: list[Any] = []
        
        for tool_def in self._tools:
            name = tool_def["name"]
            description = tool_def["description"]
            parameters = tool_def.get("parameters", {})
            
            if name in self._tool_handlers:
                handler = self._tool_handlers[name]
                
                # Create handler wrapper for SDK
                async def tool_handler(
                    invocation: dict[str, Any],
                    _handler: Callable = handler,
                    _name: str = name
                ) -> dict[str, Any]:
                    """Execute tool via registered handler."""
                    try:
                        args = invocation.get("arguments", {})
                        result = await _handler(args)
                        return {
                            "textResultForLlm": json.dumps(result) if isinstance(result, dict) else str(result),
                            "resultType": "success",
                            "sessionLog": f"Executed {_name}",
                        }
                    except Exception as e:
                        logger.error("tool_execution_error", tool=_name, error=str(e))
                        return {
                            "textResultForLlm": f"Error: {str(e)}",
                            "resultType": "error",
                        }
                
                # Create SDK Tool object
                sdk_tool = Tool(
                    name=name,
                    description=description,
                    parameters=parameters if parameters else {
                        "type": "object",
                        "properties": {},
                    },
                    handler=tool_handler,
                )
                sdk_tools.append(sdk_tool)
        
        return sdk_tools
    
    async def send_message(
        self,
        content: str,
        context: CompressedContext | None = None
    ) -> AsyncIterator[dict[str, Any]]:
        """
        Send a message and stream the response.
        
        Uses the SDK's event-based streaming when available,
        falling back to mock responses in development.
        
        Args:
            content: User message
            context: Optional compressed context
            
        Yields:
            Response chunks (text, tool_call, or done)
        """
        # Build the full message with context
        full_content = content
        if context:
            full_content = f"{context.to_prompt_text()}\n\n---\n\n{content}"
        
        self._history.append({
            "role": "user",
            "content": full_content
        })
        
        logger.info("message_sent", content_length=len(full_content))
        
        if not self._mock_mode and self._sdk_session is not None:
            # Use official SDK streaming
            async for chunk in self._stream_real_sdk(full_content):
                yield chunk
        else:
            # Mock response for development
            mock_response = self._generate_mock_response(content)
            
            for chunk in mock_response:
                yield chunk
                await asyncio.sleep(0.02)  # Simulate network delay
            
            yield {"type": "done"}
    
    async def _stream_real_sdk(self, content: str) -> AsyncIterator[dict[str, Any]]:
        """
        Stream response from the official GitHub Copilot SDK.
        
        Uses event-based streaming with session.on() callbacks.
        Events are collected into an async queue for iteration.
        
        Falls back to mock mode if SDK fails (e.g., CLI not installed).
        """
        if self._sdk_session is None:
            yield {"type": "done"}
            return
        
        import asyncio
        
        # Create an async queue to collect events
        event_queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        done_event = asyncio.Event()
        
        def on_event(event: Any) -> None:
            """Handle SDK events and put them in the queue."""
            try:
                event_type = event.type.value if hasattr(event.type, 'value') else str(event.type)
                
                if event_type == "assistant.message_delta":
                    # Streaming text chunk
                    delta = getattr(event.data, 'delta_content', None) or ""
                    if delta:
                        asyncio.get_event_loop().call_soon_threadsafe(
                            event_queue.put_nowait,
                            {"type": "text", "content": delta}
                        )
                        
                elif event_type == "assistant.message":
                    # Final complete message (we already got deltas, so just log)
                    final_content = getattr(event.data, 'content', None) or ""
                    logger.debug("sdk_message_complete", length=len(final_content))
                    
                elif event_type == "assistant.reasoning_delta":
                    # Reasoning chunk (for models that support it)
                    delta = getattr(event.data, 'delta_content', None) or ""
                    if delta:
                        asyncio.get_event_loop().call_soon_threadsafe(
                            event_queue.put_nowait,
                            {"type": "reasoning", "content": delta}
                        )
                        
                elif event_type == "tool.call":
                    # Tool is being called
                    tool_name = getattr(event.data, 'name', 'unknown')
                    tool_args = getattr(event.data, 'arguments', {})
                    asyncio.get_event_loop().call_soon_threadsafe(
                        event_queue.put_nowait,
                        {
                            "type": "tool_call",
                            "tool": tool_name,
                            "parameters": tool_args,
                            "auto_executed": True  # SDK handles execution
                        }
                    )
                    
                elif event_type == "tool.result":
                    # Tool result returned
                    tool_name = getattr(event.data, 'name', 'unknown')
                    tool_result = getattr(event.data, 'result', None)
                    asyncio.get_event_loop().call_soon_threadsafe(
                        event_queue.put_nowait,
                        {
                            "type": "tool_result",
                            "tool": tool_name,
                            "result": tool_result
                        }
                    )
                    
                elif event_type == "session.idle":
                    # Session finished processing
                    done_event.set()
                    
                elif event_type == "error":
                    error_msg = getattr(event.data, 'message', str(event.data))
                    asyncio.get_event_loop().call_soon_threadsafe(
                        event_queue.put_nowait,
                        {"type": "error", "content": error_msg}
                    )
                    done_event.set()
                    
            except Exception as e:
                logger.error("event_handler_error", error=str(e), event_type=str(event.type))
        
        try:
            # Register event handler
            self._sdk_session.on(on_event)
            
            # Send the message
            await self._sdk_session.send({"prompt": content})
            
            # Yield events as they arrive
            while not done_event.is_set():
                try:
                    # Wait for events with timeout to check done_event
                    event = await asyncio.wait_for(event_queue.get(), timeout=0.1)
                    yield event
                except asyncio.TimeoutError:
                    continue
            
            # Drain any remaining events in the queue
            while not event_queue.empty():
                try:
                    event = event_queue.get_nowait()
                    yield event
                except asyncio.QueueEmpty:
                    break
            
            yield {"type": "done"}
            
        except Exception as e:
            error_msg = str(e)
            logger.error("sdk_stream_error", error=error_msg)
            
            # Check if it's a CLI-not-found error - fall back to mock mode
            if "Failed to start" in error_msg or "cannot find" in error_msg.lower() or "WinError 2" in error_msg:
                logger.warning(
                    "sdk_fallback_to_mock",
                    reason="GitHub Copilot CLI not found. Install via: gh extension install github/gh-copilot"
                )
                # Fall back to mock response
                for chunk in self._generate_mock_response(content):
                    yield chunk
                    await asyncio.sleep(0.02)
                yield {"type": "done"}
            else:
                yield {"type": "error", "content": error_msg}
                yield {"type": "done"}
    
    async def close(self) -> None:
        """Clean up SDK resources."""
        try:
            if self._sdk_session is not None:
                await self._sdk_session.destroy()
                self._sdk_session = None
                
            if self._sdk_client is not None:
                await self._sdk_client.stop()
                self._sdk_client = None
                
            logger.debug("sdk_client_closed")
        except Exception as e:
            logger.error("sdk_close_error", error=str(e))
    
    def _generate_mock_response(self, content: str) -> list[dict[str, Any]]:
        """Generate mock response chunks for development."""
        # Simple mock - in production this comes from the SDK
        lower_content = content.lower()
        
        if "create" in lower_content or "implement" in lower_content:
            response_text = """I'll help you with that implementation.

First, let me analyze the requirements and create a plan:

1. **Understand the current structure** - Examine existing code
2. **Design the solution** - Plan the implementation approach
3. **Implement** - Write the code with proper error handling
4. **Test** - Verify the implementation works

Let me start by examining the workspace..."""
            
            # Simulate a tool call
            chunks = [
                {"type": "text", "content": response_text[:100]},
                {"type": "text", "content": response_text[100:200]},
                {"type": "text", "content": response_text[200:]},
                {
                    "type": "tool_call",
                    "tool": "list_directory",
                    "parameters": {"path": ".", "recursive": False}
                }
            ]
        else:
            response_text = f"I understand you want to: {content}\n\nI'll analyze this request and help you accomplish it."
            chunks = [
                {"type": "text", "content": response_text}
            ]
        
        return chunks
    
    async def submit_tool_result(
        self,
        tool_name: str,
        result: Any
    ) -> AsyncIterator[dict[str, Any]]:
        """
        Submit tool execution result and continue the conversation.
        
        Note: In real SDK mode, tools are auto-executed, so this is
        primarily used in mock mode. The orchestrator may still call
        this for manual tool execution scenarios.
        
        Args:
            tool_name: Name of the executed tool
            result: Tool execution result
            
        Yields:
            Continuation response chunks
        """
        self._history.append({
            "role": "tool",
            "name": tool_name,
            "content": json.dumps(result)
        })
        
        logger.info("tool_result_submitted", tool=tool_name)
        
        if not self._mock_mode and self._agent is not None:
            # Real SDK handles tool results internally
            # This path is for manual tool submission if needed
            yield {"type": "done"}
        else:
            # Mock continuation
            yield {
                "type": "text",
                "content": f"\n\nI received the results from `{tool_name}`. Let me analyze them..."
            }
            await asyncio.sleep(0.1)
            yield {"type": "done"}
    
    async def close(self) -> None:
        """Close the session."""
        if self._session_id:
            logger.info("session_closed", session_id=self._session_id)
            self._session_id = None
            self._agent = None


# =============================================================================
# EPHEMERAL SKILL SPAWNER
# =============================================================================


class EphemeralSkillSpawner:
    """
    Dynamically create and execute specialized skills.
    
    When the orchestrator determines a task needs a specialized skill
    (like shell execution), it spawns an ephemeral skill that:
    1. Is created on-the-fly from templates
    2. Executes the specific operation
    3. Returns results to the orchestrator
    4. Can be persisted for reuse if useful
    
    Built-in ephemeral skill types:
    - shell: Execute bash/powershell commands
    - file_ops: Read, write, search files
    - code_runner: Execute code snippets
    - test_runner: Run tests and collect results
    """
    
    SKILL_TEMPLATES: dict[str, dict[str, Any]] = {
        "shell": {
            "name": "shell-executor",
            "description": "Execute shell commands (bash/powershell)",
            "executor": "_execute_shell",
            "capabilities": ["list_files", "run_command", "check_status"]
        },
        "file_ops": {
            "name": "file-operations",
            "description": "Read, write, and search files",
            "executor": "_execute_file_ops",
            "capabilities": ["read", "write", "search", "list", "delete"]
        },
        "code_runner": {
            "name": "code-runner",
            "description": "Execute code snippets in various languages",
            "executor": "_execute_code",
            "capabilities": ["python", "javascript", "bash", "powershell"]
        },
        "test_runner": {
            "name": "test-runner",
            "description": "Execute tests and collect results",
            "executor": "_execute_tests",
            "capabilities": ["pytest", "jest", "unittest", "coverage"]
        }
    }
    
    def __init__(self, workspace: Path) -> None:
        """Initialize the ephemeral skill spawner."""
        self.workspace = workspace
        self._spawned_skills: dict[str, dict[str, Any]] = {}
        self._is_windows = sys.platform == "win32"
        
    def select_skill_type(self, request: str) -> str | None:
        """
        Determine which ephemeral skill type fits the request.
        
        Args:
            request: User's request
            
        Returns:
            Skill type name or None if no ephemeral skill needed
        """
        request_lower = request.lower()
        
        # Shell operations
        shell_keywords = [
            "list files", "list directory", "run command", "execute",
            "ls ", "dir ", "pwd", "cd ", "mkdir", "rm ", "cat ", "echo",
            "pip ", "npm ", "git ", "docker ", "kubectl "
        ]
        if any(kw in request_lower for kw in shell_keywords):
            return "shell"
        
        # File operations
        file_keywords = [
            "read file", "write file", "create file", "delete file",
            "search in", "find in files", "grep", "contents of"
        ]
        if any(kw in request_lower for kw in file_keywords):
            return "file_ops"
        
        # Code execution
        code_keywords = [
            "run this code", "execute script", "eval", "run python",
            "run javascript", "test this snippet"
        ]
        if any(kw in request_lower for kw in code_keywords):
            return "code_runner"
        
        # Test execution
        test_keywords = [
            "run tests", "execute tests", "pytest", "jest", "unittest",
            "test coverage", "run the test"
        ]
        if any(kw in request_lower for kw in test_keywords):
            return "test_runner"
        
        return None
    
    async def spawn_and_execute(
        self,
        skill_type: str,
        request: str,
        params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Spawn an ephemeral skill and execute the request.
        
        Args:
            skill_type: Type of skill to spawn
            request: User's request
            params: Additional parameters
            
        Returns:
            Execution result from the ephemeral skill
        """
        if skill_type not in self.SKILL_TEMPLATES:
            return {"success": False, "error": f"Unknown skill type: {skill_type}"}
        
        template = self.SKILL_TEMPLATES[skill_type]
        logger.info(
            "spawning_ephemeral_skill",
            skill_type=skill_type,
            skill_name=template["name"]
        )
        
        # Track spawned skill
        self._spawned_skills[skill_type] = {
            "template": template,
            "spawned_at": datetime.now().isoformat(),
            "request": request
        }
        
        # Execute via the appropriate method
        executor_method = getattr(self, template["executor"], None)
        if executor_method:
            return await executor_method(request, params or {})
        
        return {"success": False, "error": "Executor not found"}
    
    async def _execute_shell(
        self,
        request: str,
        params: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Execute shell commands.
        
        Handles both explicit commands and natural language requests
        like "list files in current directory".
        """
        import subprocess
        
        # Parse natural language to command
        command = self._parse_shell_request(request, params)
        
        if not command:
            return {
                "success": False,
                "error": "Could not parse shell command from request"
            }
        
        logger.info("executing_shell_command", command=command)
        
        try:
            # Choose shell based on OS
            if self._is_windows:
                result = subprocess.run(
                    ["powershell", "-Command", command],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(self.workspace)
                )
            else:
                result = subprocess.run(
                    ["bash", "-c", command],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(self.workspace)
                )
            
            return {
                "success": result.returncode == 0,
                "command": command,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out", "command": command}
        except Exception as e:
            return {"success": False, "error": str(e), "command": command}
    
    def _parse_shell_request(
        self,
        request: str,
        params: dict[str, Any]
    ) -> str | None:
        """
        Parse natural language request into shell command.
        
        Examples:
            "list files in current directory" -> "ls -la" or "Get-ChildItem"
            "show directory contents" -> "ls" or "dir"
            "find python files" -> "find . -name '*.py'" or "Get-ChildItem -Recurse -Filter *.py"
        """
        # If explicit command provided in params
        if "command" in params:
            return params["command"]
        
        request_lower = request.lower()
        
        # Map common requests to commands
        command_map = {
            # List/directory
            ("list files", "list directory", "show files", "what files", "ls", "dir"):
                "Get-ChildItem" if self._is_windows else "ls -la",
            ("list all files", "recursive list", "all files"):
                "Get-ChildItem -Recurse" if self._is_windows else "ls -laR",
            
            # Current directory
            ("current directory", "where am i", "pwd", "current path"):
                "Get-Location" if self._is_windows else "pwd",
            
            # Find files
            ("find python", "python files", "*.py"):
                "Get-ChildItem -Recurse -Filter *.py" if self._is_windows else "find . -name '*.py'",
            ("find javascript", "js files", "*.js"):
                "Get-ChildItem -Recurse -Filter *.js" if self._is_windows else "find . -name '*.js'",
            ("find typescript", "ts files", "*.ts"):
                "Get-ChildItem -Recurse -Filter *.ts" if self._is_windows else "find . -name '*.ts'",
            
            # Git
            ("git status", "repo status"):
                "git status",
            ("git log", "commit history"):
                "git log --oneline -10",
            ("git branch", "branches"):
                "git branch -a",
        }
        
        for keywords, command in command_map.items():
            if any(kw in request_lower for kw in keywords):
                return command
        
        # If request looks like a direct command, use it
        if request.strip().startswith(("ls", "dir", "cat", "echo", "git", "cd", "pwd")):
            return request.strip()
        
        if self._is_windows and request.strip().startswith(("Get-", "Set-", "New-", "Remove-")):
            return request.strip()
        
        return None
    
    async def _execute_file_ops(
        self,
        request: str,
        params: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute file operations."""
        request_lower = request.lower()
        
        # Read file
        if "read" in request_lower or "contents" in request_lower:
            file_path = params.get("path") or self._extract_path(request)
            if file_path:
                try:
                    full_path = self.workspace / file_path
                    content = full_path.read_text()
                    return {
                        "success": True,
                        "operation": "read",
                        "path": str(file_path),
                        "content": content,
                        "size": len(content)
                    }
                except Exception as e:
                    return {"success": False, "error": str(e)}
        
        # List directory
        if "list" in request_lower:
            dir_path = params.get("path", ".")
            try:
                full_path = self.workspace / dir_path
                items = list(full_path.iterdir())
                return {
                    "success": True,
                    "operation": "list",
                    "path": str(dir_path),
                    "items": [
                        {"name": p.name, "is_dir": p.is_dir(), "size": p.stat().st_size if p.is_file() else None}
                        for p in items
                    ]
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "Unknown file operation"}
    
    def _extract_path(self, request: str) -> str | None:
        """Extract file path from request."""
        import re
        # Look for quoted paths or common patterns
        patterns = [
            r'"([^"]+)"',  # Quoted
            r"'([^']+)'",  # Single quoted
            r"file\s+(\S+)",  # "file X"
            r"(\S+\.\w+)",  # Something.ext
        ]
        
        for pattern in patterns:
            match = re.search(pattern, request)
            if match:
                return match.group(1)
        return None
    
    async def _execute_code(
        self,
        request: str,
        params: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute code snippets."""
        import subprocess
        
        code = params.get("code", "")
        language = params.get("language", "python")
        
        if language == "python":
            try:
                result = subprocess.run(
                    [sys.executable, "-c", code],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(self.workspace)
                )
                return {
                    "success": result.returncode == 0,
                    "language": language,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        return {"success": False, "error": f"Language {language} not supported"}
    
    async def _execute_tests(
        self,
        request: str,
        params: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute tests."""
        import subprocess
        
        # Detect test framework
        if (self.workspace / "pytest.ini").exists() or (self.workspace / "pyproject.toml").exists():
            cmd = ["pytest", "-v", "--tb=short"]
        elif (self.workspace / "package.json").exists():
            cmd = ["npm", "test"]
        else:
            cmd = ["pytest", "-v"]  # Default to pytest
        
        # Add specific test path if provided
        if "path" in params:
            cmd.append(params["path"])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(self.workspace)
            )
            return {
                "success": result.returncode == 0,
                "framework": cmd[0],
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def persist_skill(self, skill_type: str, skill_name: str) -> Path | None:
        """
        Persist an ephemeral skill as a permanent skill file.
        
        Creates a SKILL.md in .github/skills/{skill_name}/
        """
        if skill_type not in self._spawned_skills:
            return None
        
        template = self.SKILL_TEMPLATES[skill_type]
        skills_dir = self.workspace / ".github" / "skills" / skill_name
        skills_dir.mkdir(parents=True, exist_ok=True)
        
        skill_md = skills_dir / "SKILL.md"
        skill_md.write_text(f"""---
name: {skill_name}
description: {template['description']}
license: MIT
compatibility: Requires Python 3.11+
---

# {skill_name}

Auto-generated specialized skill from copilot-orchestrator.

## Capabilities

{chr(10).join(f"- {cap}" for cap in template['capabilities'])}

## Usage

This skill was spawned from an ephemeral skill of type `{skill_type}`.
""")
        
        logger.info("skill_persisted", skill_name=skill_name, path=str(skill_md))
        return skill_md


# =============================================================================
# SKILL CATALOG - Mother of All Skills Management
# =============================================================================


# Pre-built skill templates for common development patterns
# Inspired by awesome-copilot skills: https://github.com/github/awesome-copilot/tree/main/skills
SKILL_TEMPLATES: dict[str, dict[str, Any]] = {
    # ==========================================================================
    # GIT & VERSION CONTROL
    # ==========================================================================
    "git-commit": {
        "description": "Execute git commits with conventional commit message analysis, intelligent staging, and message generation. Use when committing changes, creating standardized commits, or '/commit'. Supports auto-detecting type/scope from changes.",
        "triggers": ["commit", "git commit", "conventional commit", "feat", "fix", "chore", "stage", "/commit", "commit message"],
        "tools": ["run_in_terminal", "read_file", "grep_search"],
        "instructions": [
            "Analyze git diff (staged or unstaged) to understand changes",
            "Determine conventional commit type (feat/fix/docs/style/refactor/perf/test/build/ci/chore/revert)",
            "Identify scope from changed files (module, component, area)",
            "Generate concise description (<72 chars, imperative mood)",
            "Stage files if needed (never commit secrets)",
            "Execute: git commit -m '<type>[scope]: <description>'",
            "SAFETY: Never run --force, --no-verify, or force push to main/master"
        ]
    },
    "gh-cli": {
        "description": "Comprehensive GitHub CLI operations: repos, issues, PRs, actions, releases, gists, codespaces. Use when interacting with GitHub via command line.",
        "triggers": ["gh", "github cli", "gh pr", "gh issue", "gh repo", "gh release", "gh workflow", "gh run", "gh auth", "pull request", "issue create"],
        "tools": ["run_in_terminal", "read_file", "grep_search"],
        "instructions": [
            "Verify gh authentication: gh auth status",
            "For repos: gh repo create/clone/view/list/fork/sync",
            "For issues: gh issue create/list/view/edit/close --labels --assignee",
            "For PRs: gh pr create/list/checkout/merge/review --draft --reviewer",
            "For actions: gh run list/view/watch, gh workflow run/list",
            "For releases: gh release create/list/download",
            "Use --json and --jq for scripting; --web to open in browser"
        ]
    },
    "github-issues": {
        "description": "Create, manage, and track GitHub issues with labels, milestones, and assignees. Use when organizing work, bug reports, or feature requests.",
        "triggers": ["issue", "github issue", "bug report", "feature request", "issue tracker", "label", "milestone", "assignee"],
        "tools": ["run_in_terminal", "read_file", "create_file"],
        "instructions": [
            "Check existing issues: gh issue list --search 'keyword'",
            "Create issue: gh issue create --title 'Title' --body 'Description' --labels bug,enhancement",
            "Add templates: Create .github/ISSUE_TEMPLATE/ folder",
            "Link issues to PRs: Add 'Closes #123' or 'Fixes #456' in PR body",
            "Manage with milestones: gh issue edit 123 --milestone 'v1.0'",
            "Use projects: gh project item-add for project board integration"
        ]
    },
    
    # ==========================================================================
    # CODE QUALITY & REFACTORING
    # ==========================================================================
    "refactor": {
        "description": "Surgical code refactoring to improve maintainability without changing behavior. Covers extracting functions, renaming, breaking down god functions, improving type safety, eliminating code smells.",
        "triggers": ["refactor", "clean up", "improve code", "code smell", "extract method", "rename", "god function", "technical debt", "maintainability"],
        "tools": ["read_file", "replace_string_in_file", "grep_search", "runTests", "get_errors"],
        "instructions": [
            "GOLDEN RULES: Behavior preserved, small steps, commit before/after, tests essential",
            "Identify code smells: long method, duplication, large class, long params, feature envy",
            "Extract methods for 50+ line functions into focused units",
            "Replace magic numbers with named constants",
            "Use guard clauses to flatten nested conditionals (early returns)",
            "Remove dead code (git has history if needed)",
            "Run tests after each small change",
            "Document the refactoring rationale"
        ]
    },
    "code-review": {
        "description": "Perform thorough code reviews checking for bugs, style, performance, and security. Use when reviewing PRs or providing feedback on code.",
        "triggers": ["code review", "review", "pr review", "feedback", "approve", "request changes", "lgtm"],
        "tools": ["read_file", "grep_search", "semantic_search", "get_errors"],
        "instructions": [
            "Check for correctness: Does the code do what it claims?",
            "Verify test coverage: Are edge cases handled?",
            "Review style: Consistent with codebase conventions?",
            "Check performance: Any N+1 queries, unnecessary loops?",
            "Security scan: Input validation, auth checks, secrets exposure?",
            "Provide constructive feedback with specific suggestions",
            "Use gh pr review for GitHub integration"
        ]
    },
    
    # ==========================================================================
    # DOCUMENTATION & REQUIREMENTS
    # ==========================================================================
    "prd": {
        "description": "Generate high-quality Product Requirements Documents for software systems and AI features. Includes executive summary, user stories, technical specs, and risk analysis.",
        "triggers": ["prd", "product requirements", "requirements document", "feature spec", "specification", "user stories", "acceptance criteria"],
        "tools": ["read_file", "create_file", "semantic_search", "ask_questions"],
        "instructions": [
            "PHASE 1 - Discovery: Ask about core problem, success metrics, constraints",
            "PHASE 2 - Analysis: Map user flow, define non-goals, identify dependencies",
            "PHASE 3 - Draft using schema: Executive Summary, User Experience, Technical Specs, Risks",
            "Include measurable criteria (not 'fast' but '200ms response time')",
            "Define acceptance criteria for each user story",
            "List technical risks with mitigation strategies",
            "Create phased rollout plan: MVP → v1.1 → v2.0"
        ]
    },
    "meeting-minutes": {
        "description": "Generate concise, actionable meeting minutes for internal meetings. Includes metadata, attendees, agenda, decisions, action items (owner + due date), and follow-up steps.",
        "triggers": ["meeting minutes", "meeting notes", "minutes", "action items", "standup", "sync", "retro"],
        "tools": ["read_file", "create_file", "ask_questions"],
        "instructions": [
            "Gather metadata: title, date, organizer, attendees",
            "Structure: Metadata → Attendance → Summary → Decisions → Action Items → Notes",
            "Every action item MUST have: Owner, Due Date, Acceptance Criteria",
            "Decisions include: statement, who decided, rationale (1-2 sentences)",
            "Parking lot for unresolved items with suggested owner/next steps",
            "Keep concise: <1 page for 30min, <2 pages for 60min meetings",
            "Use ISO 8601 dates (YYYY-MM-DD)"
        ]
    },
    "documentation": {
        "description": "Write technical documentation, README files, and API docs. Use when creating guides, updating README, or documenting code.",
        "triggers": ["docs", "readme", "documentation", "guide", "explain", "jsdoc", "markdown", "api docs", "tutorial"],
        "tools": ["read_file", "create_file", "replace_string_in_file", "semantic_search", "file_search"],
        "instructions": [
            "Analyze the code/feature to be documented",
            "Determine documentation scope and audience",
            "Create or update the appropriate doc file",
            "Include clear examples and code samples",
            "Add installation/setup instructions where relevant",
            "Include troubleshooting section for common issues",
            "Cross-reference related documentation"
        ]
    },
    "markdown-to-html": {
        "description": "Convert Markdown documents to styled HTML with syntax highlighting, tables, and responsive design. Use for documentation sites, reports, or publishing.",
        "triggers": ["markdown to html", "md to html", "convert markdown", "static html", "markdown render"],
        "tools": ["read_file", "create_file", "run_in_terminal"],
        "instructions": [
            "Parse markdown content including frontmatter",
            "Convert to HTML with proper semantic tags",
            "Add syntax highlighting for code blocks (Prism.js/highlight.js)",
            "Style tables with responsive CSS",
            "Include table of contents for long docs",
            "Output standalone HTML with embedded CSS or external stylesheet"
        ]
    },
    
    # ==========================================================================
    # DIAGRAMS & VISUALIZATION
    # ==========================================================================
    "excalidraw-diagram": {
        "description": "Generate Excalidraw diagrams from natural language descriptions. Use when asked to create diagrams, flowcharts, mind maps, architecture diagrams, or visualize processes.",
        "triggers": ["diagram", "flowchart", "architecture diagram", "mind map", "excalidraw", "visualize", "draw", "chart", "system design"],
        "tools": ["create_file", "read_file"],
        "instructions": [
            "Determine diagram type: flowchart, relationship, mind map, architecture, DFD, sequence, ER",
            "Extract key elements: entities, steps, relationships",
            "Layout guidelines: 200-300px horizontal gap, 100-150px vertical gap",
            "Use consistent colors: primary (#a5d8ff), secondary (#b2f2bb), important (#ffd43b)",
            "Element types: rectangle (entities), diamond (decisions), arrow (flow)",
            "Font: Always use fontFamily: 5 (Excalifont)",
            "Save as .excalidraw JSON file",
            "Limit: 20 elements max per diagram for clarity"
        ]
    },
    "plantuml": {
        "description": "Generate PlantUML diagrams for sequence diagrams, class diagrams, and system architecture. Use for technical documentation and design.",
        "triggers": ["plantuml", "sequence diagram", "class diagram", "uml", "component diagram", "state diagram"],
        "tools": ["create_file", "read_file", "run_in_terminal"],
        "instructions": [
            "Choose diagram type: @startuml/@startmindmap/@startgantt",
            "Sequence: actor -> participant : message",
            "Class: class Name { +method() -field }",
            "Use proper arrow types: --> (dependency), --|> (inheritance), ..> (realization)",
            "Add notes: note right of X : description",
            "Group related elements: package/namespace",
            "Export to PNG/SVG using plantuml.jar or server"
        ]
    },
    
    # ==========================================================================
    # TESTING
    # ==========================================================================
    "test-suite": {
        "description": "Write comprehensive test suites with proper mocking and assertions. Use when adding unit tests, integration tests, or improving coverage.",
        "triggers": ["test", "spec", "coverage", "jest", "pytest", "vitest", "mock", "assert", "describe", "it", "unit test"],
        "tools": ["read_file", "create_file", "replace_string_in_file", "runTests", "get_errors"],
        "instructions": [
            "Analyze the code to be tested and identify test cases",
            "Review existing test patterns and frameworks used",
            "Create test file with proper describe/it blocks",
            "Write tests for happy path scenarios first",
            "Add edge cases and error handling tests",
            "Set up necessary mocks and fixtures",
            "Run tests and verify coverage improvement"
        ]
    },
    "webapp-testing": {
        "description": "Test web applications using Playwright automation. Use for verifying UI behavior, capturing screenshots, debugging web apps, and validating user flows.",
        "triggers": ["playwright", "e2e test", "browser test", "ui test", "web test", "screenshot", "automation test", "selenium"],
        "tools": ["run_in_terminal", "create_file", "read_file"],
        "instructions": [
            "Verify app is running before tests",
            "Navigation: await page.goto('url')",
            "Interactions: page.click(), page.fill(), page.selectOption()",
            "Assertions: expect(page.locator('#el')).toBeVisible()",
            "Wait properly: page.waitForSelector(), page.waitForURL()",
            "Capture screenshots on failure: page.screenshot({ path: 'error.png' })",
            "Clean up: always close browser when done",
            "Use data-testid selectors over CSS classes"
        ]
    },
    "agentic-eval": {
        "description": "Evaluate AI agent outputs for quality, accuracy, and safety. Use when testing LLM responses, validating agent behavior, or building evaluation pipelines.",
        "triggers": ["eval", "evaluation", "llm eval", "agent eval", "benchmark", "quality check", "accuracy test"],
        "tools": ["run_in_terminal", "read_file", "create_file", "runTests"],
        "instructions": [
            "Define evaluation criteria: accuracy, relevance, safety, format",
            "Create test cases with expected outputs",
            "Use structured grading rubrics (1-5 scale)",
            "Implement automated checkers where possible",
            "Track metrics: precision, recall, F1 for classification",
            "Include edge cases and adversarial inputs",
            "Log and analyze failure patterns"
        ]
    },
    
    # ==========================================================================
    # API & BACKEND
    # ==========================================================================
    "api-endpoint": {
        "description": "Create REST API endpoints with validation, error handling, and proper HTTP methods. Use when building backend APIs, creating CRUD operations, or adding new routes.",
        "triggers": ["api", "endpoint", "route", "rest", "crud", "http", "get", "post", "put", "delete", "controller"],
        "tools": ["read_file", "create_file", "replace_string_in_file", "grep_search", "runTests"],
        "instructions": [
            "Analyze existing API patterns and conventions in the codebase",
            "Determine the appropriate HTTP method(s) and URL structure",
            "Create the endpoint handler with request validation",
            "Add proper error handling and response formatting",
            "Update route registration if needed",
            "Add or update API documentation",
            "Create integration tests for the endpoint"
        ]
    },
    "database-migration": {
        "description": "Create database migrations and schema changes safely. Use when modifying tables, adding columns, creating indexes, or seeding data.",
        "triggers": ["migration", "database", "schema", "table", "column", "index", "sql", "prisma", "knex", "typeorm", "alembic"],
        "tools": ["read_file", "create_file", "run_in_terminal", "grep_search"],
        "instructions": [
            "Review existing schema and migrations for patterns",
            "Plan the migration with rollback strategy",
            "Create the migration file following project conventions",
            "Write both up and down migration logic",
            "Test migration on local database first",
            "Update any affected model/entity files",
            "Document breaking changes if applicable"
        ]
    },
    
    # ==========================================================================
    # FRONTEND & UI
    # ==========================================================================
    "react-component": {
        "description": "Build React components with TypeScript, hooks, and proper state management. Use when creating UI components, forms, or interactive elements.",
        "triggers": ["react", "component", "tsx", "jsx", "hook", "useState", "useEffect", "props", "ui", "form", "button"],
        "tools": ["read_file", "create_file", "replace_string_in_file", "file_search", "runTests"],
        "instructions": [
            "Analyze existing component patterns and styling conventions",
            "Create the component file with TypeScript types/interfaces",
            "Implement component logic with appropriate React hooks",
            "Add proper prop types and default values",
            "Include necessary styling (CSS modules, Tailwind, etc.)",
            "Create unit tests for the component",
            "Export the component and update barrel files if needed"
        ]
    },
    "web-design-review": {
        "description": "Review web designs for UX, accessibility, and implementation feasibility. Use when evaluating mockups, providing design feedback, or auditing UI.",
        "triggers": ["design review", "ux review", "accessibility", "a11y", "wcag", "ui audit", "design feedback", "usability"],
        "tools": ["read_file", "semantic_search", "grep_search"],
        "instructions": [
            "Check accessibility: color contrast, focus states, alt text, keyboard nav",
            "Review information hierarchy and visual flow",
            "Verify responsive breakpoints and mobile experience",
            "Check loading states and error handling UI",
            "Validate against WCAG 2.1 AA standards",
            "Document implementation concerns for engineering",
            "Provide specific, actionable improvement suggestions"
        ]
    },
    
    # ==========================================================================
    # DEVOPS & CI/CD
    # ==========================================================================
    "ci-pipeline": {
        "description": "Create CI/CD pipelines with GitHub Actions, testing, and deployment. Use when setting up automation, build processes, or release workflows.",
        "triggers": ["ci", "cd", "pipeline", "github actions", "workflow", "deploy", "build", "release", "automation"],
        "tools": ["read_file", "create_file", "replace_string_in_file", "run_in_terminal", "file_search"],
        "instructions": [
            "Analyze project structure and deployment requirements",
            "Review existing workflows for patterns and secrets",
            "Create .github/workflows YAML file",
            "Define triggers (push, PR, schedule)",
            "Add build and test jobs",
            "Configure deployment steps and environments",
            "Add caching for dependencies where beneficial",
            "Test workflow with a dry run if possible"
        ]
    },
    "azure-deployment": {
        "description": "Deploy applications to Azure: App Service, Functions, Static Web Apps, Container Apps. Use when deploying to Azure cloud infrastructure.",
        "triggers": ["azure", "deploy to azure", "app service", "azure functions", "container apps", "aks", "azure static web app"],
        "tools": ["run_in_terminal", "read_file", "create_file", "file_search"],
        "instructions": [
            "Verify Azure CLI: az account show",
            "Choose deployment target: App Service, Functions, Static Web Apps, Container Apps",
            "Configure app settings and environment variables",
            "Set up deployment slots for staging",
            "Configure CI/CD with GitHub Actions or Azure DevOps",
            "Enable Application Insights for monitoring",
            "Configure scaling and alerts",
            "Document deployment process"
        ]
    },
    "azure-devops": {
        "description": "Work with Azure DevOps: pipelines, repos, boards, artifacts. Use when managing work items, builds, or deployments in Azure DevOps.",
        "triggers": ["azure devops", "ado", "azure pipeline", "azure boards", "work item", "azure repos", "artifacts"],
        "tools": ["run_in_terminal", "read_file", "create_file"],
        "instructions": [
            "Authenticate: az devops login",
            "Configure organization and project: az devops configure --defaults",
            "Create pipelines: az pipelines create",
            "Manage work items: az boards work-item create/update",
            "Use azure-pipelines.yml for YAML pipelines",
            "Configure service connections for deployments",
            "Set up artifact feeds for packages"
        ]
    },
    "terraform": {
        "description": "Infrastructure as Code with Terraform: create, plan, apply infrastructure. Use when managing cloud infrastructure declaratively.",
        "triggers": ["terraform", "iac", "infrastructure as code", "tf", "hcl", "terraform plan", "terraform apply"],
        "tools": ["run_in_terminal", "read_file", "create_file", "grep_search"],
        "instructions": [
            "Initialize: terraform init",
            "Structure: main.tf, variables.tf, outputs.tf, terraform.tfvars",
            "Use modules for reusable components",
            "Plan before apply: terraform plan -out=tfplan",
            "Apply with approval: terraform apply tfplan",
            "State management: Use remote backend (S3, Azure Blob)",
            "Use terraform fmt and terraform validate",
            "Never commit .tfvars with secrets"
        ]
    },
    
    # ==========================================================================
    # SECURITY & AUDIT
    # ==========================================================================
    "security-audit": {
        "description": "Perform security audits checking for vulnerabilities and best practices. Use when reviewing code security, checking dependencies, or hardening apps.",
        "triggers": ["security", "audit", "vulnerability", "xss", "csrf", "injection", "auth", "secrets", "owasp"],
        "tools": ["read_file", "grep_search", "semantic_search", "run_in_terminal", "get_errors"],
        "instructions": [
            "Scan for hardcoded secrets and credentials",
            "Check for common vulnerability patterns (injection, XSS)",
            "Review authentication and authorization logic",
            "Audit dependencies for known vulnerabilities",
            "Check for proper input validation",
            "Review error handling (no sensitive info leaks)",
            "Compile findings with severity ratings and remediation steps"
        ]
    },
    
    # ==========================================================================
    # PERFORMANCE
    # ==========================================================================
    "performance-optimizer": {
        "description": "Optimize code for performance: reduce latency, memory usage, and bundle size. Use when improving load times, query performance, or resource usage.",
        "triggers": ["optimize", "performance", "speed", "slow", "latency", "memory", "bundle", "cache", "lazy load"],
        "tools": ["read_file", "replace_string_in_file", "grep_search", "run_in_terminal", "runTests"],
        "instructions": [
            "Profile and identify performance bottlenecks",
            "Analyze algorithms for time/space complexity",
            "Check for unnecessary re-renders or computations",
            "Implement caching where beneficial",
            "Optimize database queries and indexes",
            "Consider lazy loading and code splitting",
            "Benchmark before and after changes",
            "Document performance improvements achieved"
        ]
    },
    
    # ==========================================================================
    # TOOLS & DEBUGGING
    # ==========================================================================
    "chrome-devtools": {
        "description": "Debug web applications using Chrome DevTools: inspect elements, network, performance, console. Use when debugging frontend issues.",
        "triggers": ["devtools", "chrome devtools", "debug", "inspect", "network tab", "console", "performance profile", "memory leak"],
        "tools": ["run_in_terminal", "read_file"],
        "instructions": [
            "Elements: Inspect and modify DOM/CSS in real-time",
            "Console: Execute JS, log statements, filter errors",
            "Network: Analyze requests, response times, payload sizes",
            "Performance: Record and analyze runtime performance",
            "Memory: Find leaks with heap snapshots",
            "Application: Inspect storage, service workers, cache",
            "Use Lighthouse for automated audits"
        ]
    },
    "vscode-extension": {
        "description": "Create and configure VS Code extensions: commands, settings, keybindings, language support. Use when building or customizing VS Code.",
        "triggers": ["vscode extension", "vscode", "extension", "keybinding", "command palette", "extension api"],
        "tools": ["run_in_terminal", "read_file", "create_file", "grep_search"],
        "instructions": [
            "Generate extension: yo code",
            "Define in package.json: contributes.commands, keybindings, configuration",
            "Implement in extension.ts: activate(), deactivate()",
            "Register commands: vscode.commands.registerCommand()",
            "Access workspace: vscode.workspace.fs, vscode.window.activeTextEditor",
            "Debug: F5 launches Extension Development Host",
            "Package: vsce package, publish: vsce publish"
        ]
    },
    "mcp-server": {
        "description": "Create Model Context Protocol (MCP) servers for extending AI assistants with custom tools. Use when building integrations for Copilot or Claude.",
        "triggers": ["mcp", "model context protocol", "mcp server", "mcp tool", "copilot extension", "ai tool"],
        "tools": ["run_in_terminal", "read_file", "create_file"],
        "instructions": [
            "Structure: Use @modelcontextprotocol/sdk",
            "Define tools with JSON Schema for parameters",
            "Implement tool handlers with proper error handling",
            "Use stdio or HTTP transport",
            "Configure in mcp.json for VS Code",
            "Test with MCP inspector",
            "Handle timeouts and rate limits"
        ]
    },
    
    # ==========================================================================
    # DATA & ANALYTICS
    # ==========================================================================
    "powerbi": {
        "description": "Create Power BI data models, DAX measures, and reports. Use when building business intelligence solutions.",
        "triggers": ["powerbi", "power bi", "dax", "data model", "measure", "calculated column", "report", "dashboard"],
        "tools": ["read_file", "create_file"],
        "instructions": [
            "Design star schema: fact tables, dimension tables",
            "Create relationships with proper cardinality",
            "Write DAX measures: SUM, CALCULATE, FILTER, RELATED",
            "Time intelligence: DATEADD, SAMEPERIODLASTYEAR",
            "Optimize model: Remove unused columns, use integer keys",
            "Build visualizations: charts, tables, cards, slicers",
            "Configure row-level security if needed"
        ]
    },
    "data-pipeline": {
        "description": "Build data pipelines for ETL, streaming, and analytics. Use when moving, transforming, or processing data at scale.",
        "triggers": ["etl", "data pipeline", "airflow", "spark", "data engineering", "batch processing", "streaming"],
        "tools": ["run_in_terminal", "read_file", "create_file"],
        "instructions": [
            "Design pipeline: Source → Transform → Destination",
            "Choose tool: Airflow (orchestration), Spark (processing), dbt (transform)",
            "Implement idempotent operations",
            "Add data quality checks and validation",
            "Handle failures with retries and dead-letter queues",
            "Monitor with logging and alerting",
            "Document data lineage and schema"
        ]
    },
    
    # ==========================================================================
    # PACKAGE MANAGEMENT
    # ==========================================================================
    "nuget": {
        "description": "Manage NuGet packages: install, update, create, publish. Use when working with .NET dependencies.",
        "triggers": ["nuget", "dotnet package", "package reference", "nuspec", "pack", "push"],
        "tools": ["run_in_terminal", "read_file", "create_file"],
        "instructions": [
            "Search: dotnet search <package>",
            "Install: dotnet add package <name> --version <ver>",
            "Update: dotnet list package --outdated, then update",
            "Create: dotnet pack with proper .csproj metadata",
            "Publish: dotnet nuget push to nuget.org or private feed",
            "Restore: dotnet restore",
            "Use Directory.Packages.props for central package management"
        ]
    },
    
    # ==========================================================================
    # IMAGE & MEDIA
    # ==========================================================================
    "image-manipulation": {
        "description": "Process images with ImageMagick: resize, convert, optimize, composite. Use when batch processing images or generating thumbnails.",
        "triggers": ["imagemagick", "image resize", "convert image", "image processing", "thumbnail", "optimize image"],
        "tools": ["run_in_terminal", "read_file"],
        "instructions": [
            "Install: apt/brew install imagemagick",
            "Resize: magick input.jpg -resize 800x600 output.jpg",
            "Convert: magick input.png output.webp",
            "Optimize: magick input.jpg -quality 85 -strip output.jpg",
            "Batch: magick mogrify -resize 50% *.jpg",
            "Composite: magick background.jpg overlay.png -composite result.jpg",
            "Info: magick identify -verbose image.jpg"
        ]
    },
    
    # ==========================================================================
    # SKILL CREATION (META)
    # ==========================================================================
    "skill-template": {
        "description": "Create new GitHub Copilot skills with proper SKILL.md structure. Use when building reusable AI assistant capabilities.",
        "triggers": ["create skill", "skill template", "new skill", "copilot skill", "skill.md"],
        "tools": ["create_file", "read_file", "file_search"],
        "instructions": [
            "Create folder: .github/skills/<skill-name>/",
            "Create SKILL.md with YAML frontmatter: name, description",
            "Define triggers: when should this skill activate",
            "List allowed-tools: what tools can the skill use",
            "Write clear instructions: step-by-step guidance",
            "Include examples for common use cases",
            "Add references to documentation or templates"
        ]
    },
    "copilot-sdk": {
        "description": "Use GitHub Copilot SDK for AI-powered code generation and chat. Use when building AI features with Copilot integration.",
        "triggers": ["copilot sdk", "copilot api", "copilot chat", "ai completions", "lm api"],
        "tools": ["run_in_terminal", "read_file", "create_file"],
        "instructions": [
            "Install: pip install copilot-sdk or npm install @anthropic-ai/sdk",
            "Initialize: client = CopilotClient()",
            "Chat: response = await client.chat(messages=[...])",
            "Completions: client.complete(prompt=..., max_tokens=...)",
            "Stream responses for long outputs",
            "Handle rate limits with exponential backoff",
            "Use system prompts for role/behavior definition"
        ]
    }
}


@dataclass
class SkillMatch:
    """Result of skill matching/discovery."""
    name: str
    path: Path
    description: str
    match_score: float  # 0.0 to 1.0
    matched_keywords: list[str]


class SkillCatalog:
    """
    Catalog and discovery system for generated skills.
    
    The Mother of All Skills - manages skill lifecycle:
    - Discovery: Find existing skills that match a request
    - Generation: Create new skills when none exist
    - Evolution: Improve skills based on usage patterns
    - Templates: Quick-start from common patterns
    
    Usage:
        catalog = SkillCatalog(workspace)
        
        # Find matching skills
        matches = await catalog.find_matching_skills("create a REST API endpoint")
        
        # Auto-generate if no good match
        if not matches or matches[0].match_score < 0.5:
            skill = await catalog.generate_specialized_skill(
                request="create REST API endpoint with validation",
                use_sdk=True
            )
    """
    
    def __init__(self, workspace: Path) -> None:
        """Initialize the skill catalog."""
        self.workspace = workspace.resolve()
        self.skills_dir = self.workspace / ".github" / "skills"
        self.generator = SkillGenerator(workspace)
        self._cache: dict[str, dict] = {}  # skill name -> parsed content
        logger.debug("skill_catalog_init", workspace=str(self.workspace))
    
    def _parse_skill_content(self, skill_path: Path) -> dict[str, Any]:
        """Parse a SKILL.md file into structured data."""
        if not skill_path.exists():
            return {}
        
        content = skill_path.read_text(encoding="utf-8")
        result: dict[str, Any] = {
            "name": skill_path.parent.name,
            "path": str(skill_path),
            "raw_content": content,
            "description": "",
            "triggers": [],
            "instructions": [],
            "tools": []
        }
        
        # Parse YAML frontmatter
        import re
        fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if fm_match:
            for line in fm_match.group(1).split('\n'):
                if line.startswith('description:'):
                    result["description"] = line.replace('description:', '').strip().strip("'\"")
                elif line.startswith('name:'):
                    result["name"] = line.replace('name:', '').strip()
        
        # Extract keywords from content
        keywords = []
        # Look for trigger sections
        trigger_match = re.search(r'(?:Triggers?|Keywords?|Activation).*?(?=##|\Z)', content, re.IGNORECASE | re.DOTALL)
        if trigger_match:
            for match in re.finditer(r'`([^`]+)`', trigger_match.group(0)):
                keywords.append(match.group(1).lower())
        
        # Also extract from description
        desc_words = re.findall(r'\b\w+\b', result["description"].lower())
        keywords.extend(desc_words)
        result["triggers"] = list(set(keywords))[:50]
        
        # Extract tools
        tools_match = re.search(r'allowed-tools:\s*(.*?)(?:\n```|\Z)', content, re.DOTALL)
        if tools_match:
            for line in tools_match.group(1).split('\n'):
                tool = line.strip().lstrip('-').strip()
                if tool:
                    result["tools"].append(tool)
        
        return result
    
    def refresh_cache(self) -> None:
        """Refresh the skill cache from disk."""
        self._cache.clear()
        
        if not self.skills_dir.exists():
            return
        
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    try:
                        self._cache[skill_dir.name] = self._parse_skill_content(skill_md)
                    except Exception as e:
                        logger.warning("skill_parse_error", skill=skill_dir.name, error=str(e))
    
    def get_all_skills(self) -> list[dict[str, Any]]:
        """Get all available skills."""
        if not self._cache:
            self.refresh_cache()
        return list(self._cache.values())
    
    async def find_matching_skills(
        self,
        request: str,
        min_score: float = 0.1
    ) -> list[SkillMatch]:
        """
        Find skills that match a user request.
        
        Uses keyword matching and semantic similarity to rank skills.
        
        Args:
            request: User's natural language request
            min_score: Minimum score to include in results (0.0-1.0)
            
        Returns:
            List of SkillMatch objects sorted by match_score descending
        """
        import re
        
        if not self._cache:
            self.refresh_cache()
        
        request_lower = request.lower()
        request_words = set(re.findall(r'\b\w{3,}\b', request_lower))
        
        matches: list[SkillMatch] = []
        
        for skill_name, skill_data in self._cache.items():
            skill_keywords = set(skill_data.get("triggers", []))
            skill_desc_words = set(re.findall(r'\b\w{3,}\b', skill_data.get("description", "").lower()))
            all_skill_words = skill_keywords | skill_desc_words
            
            # Calculate match score
            matched = request_words & all_skill_words
            if not all_skill_words:
                score = 0.0
            else:
                # Jaccard-like similarity with boost for keyword matches
                keyword_matches = request_words & skill_keywords
                total_possible = len(request_words | all_skill_words)
                score = (len(matched) + len(keyword_matches) * 0.5) / max(total_possible, 1)
            
            if score >= min_score:
                matches.append(SkillMatch(
                    name=skill_name,
                    path=Path(skill_data.get("path", "")),
                    description=skill_data.get("description", ""),
                    match_score=min(score, 1.0),
                    matched_keywords=list(matched)
                ))
        
        # Sort by score descending
        matches.sort(key=lambda m: m.match_score, reverse=True)
        return matches
    
    def suggest_template(self, request: str) -> str | None:
        """
        Suggest a skill template based on the request.
        
        Returns template key or None if no good match.
        """
        request_lower = request.lower()
        
        best_template = None
        best_score = 0.0
        
        for template_key, template_data in SKILL_TEMPLATES.items():
            triggers = template_data.get("triggers", [])
            matches = sum(1 for t in triggers if t in request_lower)
            score = matches / len(triggers) if triggers else 0
            
            if score > best_score:
                best_score = score
                best_template = template_key
        
        return best_template if best_score >= 0.2 else None
    
    async def generate_specialized_skill(
        self,
        request: str,
        name: str | None = None,
        use_sdk: bool = True,
        from_template: str | None = None
    ) -> GeneratedSkill:
        """
        Generate a specialized skill based on request.
        
        This is the core "skill factory" method. It:
        1. Optionally starts from a template
        2. Uses SDK to generate comprehensive, tailored content
        3. Creates a production-ready SKILL.md
        
        Args:
            request: Natural language description of what the skill should do
            name: Optional skill name (auto-generated if not provided)
            use_sdk: Whether to use Copilot SDK for intelligent generation
            from_template: Optional template key to start from
            
        Returns:
            GeneratedSkill with the created skill details
        """
        import re
        
        # Auto-generate name from request if not provided
        if not name:
            # Extract key nouns/verbs for name
            words = re.findall(r'\b[a-z]{3,}\b', request.lower())
            common = {"the", "and", "for", "with", "that", "this", "create", "make", "build", "write", "need", "want", "should", "would", "could"}
            meaningful = [w for w in words if w not in common][:3]
            name = "-".join(meaningful) if meaningful else f"skill-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Get template boost if available
        template_data: dict[str, Any] = {}
        if from_template and from_template in SKILL_TEMPLATES:
            template_data = SKILL_TEMPLATES[from_template]
        elif not from_template:
            # Auto-detect template
            suggested = self.suggest_template(request)
            if suggested:
                template_data = SKILL_TEMPLATES[suggested]
                logger.info("template_auto_selected", template=suggested)
        
        # Generate using SDK or standard method
        if use_sdk:
            return await self.generator.generate_with_sdk(
                name=name,
                task_description=request,
                template_boost=template_data
            )
        else:
            return await self.generator.generate(
                name=name,
                description=request,
                task_description=request,
                triggers=template_data.get("triggers"),
                instructions=template_data.get("instructions"),
                tools=template_data.get("tools")
            )
    
    async def should_create_skill(
        self,
        request: str,
        threshold: float = 0.4
    ) -> tuple[bool, str]:
        """
        Determine if a new skill should be created for this request.
        
        Returns (should_create, reason).
        
        Criteria for creating a new skill:
        - No existing skill matches well (score < threshold)
        - Request describes a repeatable task pattern
        - Request is specific enough to be useful
        """
        import re
        
        matches = await self.find_matching_skills(request)
        
        if matches and matches[0].match_score >= threshold:
            return False, f"Existing skill '{matches[0].name}' matches well (score: {matches[0].match_score:.2f})"
        
        # Check if request is specific enough
        words = re.findall(r'\b\w+\b', request.lower())
        if len(words) < 5:
            return False, "Request too vague - provide more details for skill generation"
        
        # Check for repeatable patterns
        repeatable_indicators = [
            "whenever", "always", "every time", "frequently", "often", 
            "standardize", "pattern", "consistently", "template"
        ]
        has_repeatable = any(ind in request.lower() for ind in repeatable_indicators)
        
        if has_repeatable:
            return True, "Request indicates a repeatable pattern"
        
        # Check for specific task type
        if self.suggest_template(request):
            return True, "Request matches a common development pattern"
        
        return True, "No matching skill found - creating specialized skill"


# =============================================================================
# SKILL GENERATOR - Creates reusable SKILL.md files
# =============================================================================


@dataclass
class GeneratedSkill:
    """Result of skill generation."""
    
    name: str
    path: Path
    description: str
    task_type: str
    triggers: list[str]
    instructions: list[str]
    context_files: list[str]
    created_at: datetime = field(default_factory=datetime.now)


class SkillGenerator:
    """
    Generate reusable SKILL.md files from task descriptions.
    
    The core value of skills is **minimizing context consumption**:
    - Instead of loading the full orchestrator (~8K tokens) every time,
    - Generate a focused skill (~500-1500 tokens) for specific tasks.
    
    Follows the Agent Skills specification from awesome-copilot:
    - name: 1-64 chars, lowercase letters/numbers/hyphens, matches folder
    - description: 1-1024 chars, WHAT it does + WHEN to use + keywords
    
    Usage:
        generator = SkillGenerator(workspace)
        skill = await generator.generate(
            name="api-endpoint-creator",
            description="Create REST API endpoints with validation",
            task_description="I frequently need to create REST endpoints..."
        )
        # Creates .github/skills/api-endpoint-creator/SKILL.md
    """
    
    # Template follows awesome-copilot/make-skill-template spec
    SKILL_TEMPLATE = '''---
name: {name}
description: '{description}'
license: MIT
---

# {title}

{summary}

## When to Use This Skill

{use_cases}

## Prerequisites

{prerequisites}

## Step-by-Step Workflow

{instructions_section}

## Allowed Tools

```yaml
allowed-tools: {tools_inline}
```

## Validation

{validation_section}

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Skill not matching | Ensure your prompt contains relevant keywords |
| Tool not available | Check that the tool is enabled in your Copilot settings |

## References

- [copilot-orchestrator skill](.github/skills/copilot-orchestrator/SKILL.md)
- [Agent Skills specification](https://agentskills.io/specification)
'''
    
    def __init__(self, workspace: Path) -> None:
        """
        Initialize the skill generator.
        
        Args:
            workspace: Project root directory (must contain .github folder or it will be created)
        """
        # Ensure workspace is resolved to absolute path
        self.workspace = workspace.resolve()
        self.skills_dir = self.workspace / ".github" / "skills"
        
        logger.debug("skill_generator_init", workspace=str(self.workspace), skills_dir=str(self.skills_dir))
        
    def _slugify(self, name: str) -> str:
        """Convert name to valid skill directory name."""
        import re
        slug = name.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug
    
    def _analyze_task(self, task_description: str) -> dict[str, Any]:
        """
        Analyze task description to determine skill parameters.
        
        Returns task type, keywords, tools needed, etc.
        """
        desc_lower = task_description.lower()
        
        # Determine task type - order matters! More specific checks first
        task_type = "general"
        
        # Test should be checked early - test descriptions often mention "error handling"
        if any(w in desc_lower for w in ["test", "coverage", "spec", "assert", "unit test", "unittest"]):
            task_type = "test"
        elif any(w in desc_lower for w in ["implement", "create", "build", "add", "make", "develop"]):
            task_type = "implement"
        elif any(w in desc_lower for w in ["fix", "debug", "bug", "issue", "problem", "broken", "not working"]):
            # Removed "error" since it's too general (appears in "error handling")
            task_type = "debug"
        elif any(w in desc_lower for w in ["refactor", "restructure", "improve", "clean", "optimize"]):
            task_type = "refactor"
        elif any(w in desc_lower for w in ["deploy", "pipeline", "ci", "cd", "release", "ci/cd"]):
            task_type = "deploy"
        elif any(w in desc_lower for w in ["document", "readme", "doc", "explain", "documentation"]):
            task_type = "document"
        elif any(w in desc_lower for w in ["analyze", "review", "audit", "check", "scan"]):
            task_type = "analyze"
        
        # Extract keywords for triggers
        import re
        words = re.findall(r'\b[a-z]{3,}\b', desc_lower)
        common_words = {"the", "and", "for", "with", "that", "this", "from", "have", "are", "was", "will", "can", "should", "would", "could", "need", "want"}
        keywords = [w for w in words if w not in common_words][:10]
        
        # Determine tools needed based on task type
        tools_map = {
            "implement": ["create_file", "replace_string_in_file", "read_file", "run_in_terminal"],
            "debug": ["read_file", "grep_search", "get_errors", "run_in_terminal"],
            "test": ["runTests", "read_file", "create_file", "get_errors"],
            "refactor": ["read_file", "replace_string_in_file", "file_search", "list_code_usages"],
            "deploy": ["run_in_terminal", "create_file", "read_file", "file_search"],
            "document": ["read_file", "create_file", "replace_string_in_file", "semantic_search"],
            "analyze": ["read_file", "grep_search", "file_search", "semantic_search", "get_errors"],
            "general": ["read_file", "create_file", "replace_string_in_file", "run_in_terminal", "file_search"]
        }
        
        return {
            "task_type": task_type,
            "keywords": keywords,
            "tools": tools_map.get(task_type, tools_map["general"])
        }
    
    def _generate_triggers_section(self, keywords: list[str], task_type: str) -> str:
        """Generate the triggers/keywords section."""
        lines = []
        for kw in keywords:
            lines.append(f"- `{kw}`")
        
        # Add task-type specific triggers
        type_triggers = {
            "implement": ["create", "build", "add", "implement", "make"],
            "debug": ["fix", "debug", "error", "bug", "problem", "issue"],
            "test": ["test", "coverage", "spec", "assert", "verify"],
            "refactor": ["refactor", "restructure", "improve", "clean", "optimize"],
            "deploy": ["deploy", "pipeline", "release", "ci/cd"],
            "document": ["document", "readme", "explain", "describe"],
            "analyze": ["analyze", "review", "audit", "check"]
        }
        for t in type_triggers.get(task_type, []):
            if t not in keywords:
                lines.append(f"- `{t}`")
        
        return "\n".join(lines[:15])  # Limit to 15 triggers
    
    def _generate_instructions_section(
        self, 
        task_description: str,
        task_type: str,
        custom_instructions: list[str] | None
    ) -> str:
        """Generate step-by-step instructions."""
        if custom_instructions:
            lines = [f"{i+1}. {inst}" for i, inst in enumerate(custom_instructions)]
            return "\n".join(lines)
        
        # Generate default instructions based on task type
        default_instructions = {
            "implement": [
                "Understand the requirements from the user's request",
                "Search for existing related code patterns in the codebase",
                "Create or modify files as needed to implement the feature",
                "Add appropriate error handling and validation",
                "Run tests to verify the implementation works",
                "Provide a summary of changes made"
            ],
            "debug": [
                "Analyze the error message or symptoms described",
                "Search for the relevant code causing the issue",
                "Identify the root cause of the problem",
                "Implement the fix with minimal changes",
                "Test to verify the fix resolves the issue",
                "Explain what caused the bug and how it was fixed"
            ],
            "test": [
                "Identify the code that needs test coverage",
                "Analyze existing test patterns in the project",
                "Create test file(s) with appropriate structure",
                "Write test cases covering happy path and edge cases",
                "Run tests to verify they pass",
                "Check coverage if possible"
            ],
            "refactor": [
                "Understand the current code structure",
                "Identify code smells and improvement opportunities",
                "Plan the refactoring approach",
                "Make incremental changes preserving behavior",
                "Run tests after each change to ensure no regressions",
                "Document any significant architectural changes"
            ],
            "deploy": [
                "Review deployment target requirements",
                "Create or update deployment configuration",
                "Set up CI/CD pipeline if needed",
                "Configure environment variables and secrets",
                "Test the deployment process",
                "Document the deployment procedure"
            ],
            "document": [
                "Analyze the code/feature to be documented",
                "Identify the target audience for the documentation",
                "Create clear, concise documentation with examples",
                "Include installation/setup instructions if applicable",
                "Add code samples and usage examples",
                "Review for clarity and completeness"
            ],
            "analyze": [
                "Scan the codebase for relevant patterns",
                "Identify areas of concern or improvement",
                "Check for common issues (security, performance)",
                "Review code against best practices",
                "Compile findings into a clear report",
                "Prioritize recommendations by impact"
            ],
            "general": [
                "Parse and understand the user's request",
                "Gather necessary context from the codebase",
                "Execute the required operations",
                "Verify the results meet expectations",
                "Provide clear feedback on what was done"
            ]
        }
        
        instructions = default_instructions.get(task_type, default_instructions["general"])
        return "\n".join(f"{i+1}. {inst}" for i, inst in enumerate(instructions))
    
    def _generate_context_section(self, context_files: list[str] | None) -> str:
        """Generate the context requirements section."""
        if context_files:
            lines = [f"- `{f}`" for f in context_files]
            return "\n".join(lines)
        
        return """- Relevant source files in the workspace
- Configuration files (if applicable)
- Related test files (if available)"""
    
    def _generate_tools_yaml(self, tools: list[str]) -> str:
        """Generate YAML list of allowed tools."""
        return "\n".join(f"  - {tool}" for tool in tools)
    
    def _generate_execution_section(self, task_type: str) -> str:
        """Generate execution guidance."""
        return f"""When this skill is triggered, it will:

1. **Analyze** the request to understand specific requirements
2. **Gather** relevant context from the workspace
3. **Execute** using the appropriate tools for {task_type} tasks
4. **Validate** results and provide feedback"""

    def _generate_validation_section(self, task_type: str) -> str:
        """Generate validation criteria."""
        validations = {
            "implement": "- [ ] Code compiles/runs without errors\n- [ ] Feature works as expected\n- [ ] Tests pass (if applicable)",
            "debug": "- [ ] Error no longer occurs\n- [ ] No regressions introduced\n- [ ] Root cause was addressed",
            "test": "- [ ] Tests pass\n- [ ] Tests cover the target code\n- [ ] Edge cases are covered",
            "refactor": "- [ ] All tests still pass\n- [ ] Code quality improved\n- [ ] No behavior changes",
            "deploy": "- [ ] Deployment succeeds\n- [ ] Application runs correctly\n- [ ] Configuration is correct",
            "document": "- [ ] Documentation is clear and complete\n- [ ] Examples work correctly\n- [ ] Covers all key features",
            "analyze": "- [ ] Analysis is thorough\n- [ ] Findings are actionable\n- [ ] Recommendations are prioritized",
            "general": "- [ ] Task completed successfully\n- [ ] Results match expectations"
        }
        return validations.get(task_type, validations["general"])
    
    async def generate(
        self,
        name: str,
        description: str,
        task_description: str | None = None,
        instructions: list[str] | None = None,
        context_files: list[str] | None = None,
        triggers: list[str] | None = None,
        tools: list[str] | None = None
    ) -> GeneratedSkill:
        """
        Generate a new SKILL.md file following Agent Skills specification.
        
        Args:
            name: Skill name (will be slugified - lowercase, hyphens)
            description: One-line description (1-1024 chars, includes WHAT + WHEN + keywords)
            task_description: Detailed description of what this skill does
            instructions: Custom step-by-step instructions (auto-generated if not provided)
            context_files: Files this skill typically needs
            triggers: Keywords/phrases that activate this skill
            tools: Tools this skill uses (auto-detected if not provided)
            
        Returns:
            GeneratedSkill with path to created SKILL.md
        """
        slug = self._slugify(name)
        skill_dir = self.skills_dir / slug
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # Analyze task if description provided
        analysis = self._analyze_task(task_description or description)
        task_type = analysis["task_type"]
        
        # Use provided values or defaults from analysis
        final_triggers = triggers or analysis["keywords"]
        final_tools = tools or analysis["tools"]
        
        # Build rich description with triggers (per awesome-copilot spec)
        # Format: "<WHAT it does>. Use when <triggers/scenarios>. Triggers on <keywords>."
        trigger_words = ", ".join(final_triggers[:7])
        rich_description = description
        if not any(phrase in description.lower() for phrase in ["use when", "trigger"]):
            rich_description = f"{description}. Triggers on {trigger_words}."
        
        # Generate use cases as bullet list
        use_cases_list = []
        for desc in (task_description or description).split("."):
            desc = desc.strip()
            if desc and len(desc) > 10:
                use_cases_list.append(f"- {desc}")
        use_cases = "\n".join(use_cases_list[:5]) if use_cases_list else f"- {description}"
        
        # Generate prerequisites based on task type
        prerequisites_map = {
            "implement": "- Code editor with workspace access\n- Understanding of the target codebase structure",
            "debug": "- Access to error logs or stack traces\n- Reproducible test case (if possible)",
            "test": "- Testing framework configured (pytest, jest, etc.)\n- Code to be tested is accessible",
            "refactor": "- Existing test suite (recommended)\n- Understanding of current code behavior",
            "deploy": "- Deployment target credentials configured\n- Required CLI tools installed",
            "document": "- Access to code/feature being documented\n- Knowledge of target audience",
            "analyze": "- Full codebase access\n- Understanding of what to analyze",
            "general": "- Workspace with relevant files\n- Clear task description"
        }
        prerequisites = prerequisites_map.get(task_type, prerequisites_map["general"])
        
        # Summary paragraph for body
        summary = (task_description or description).split(".")[0].strip() + "."
        
        # Tools as space-delimited inline list
        tools_inline = " ".join(final_tools)
        
        # Generate skill content using updated template
        content = self.SKILL_TEMPLATE.format(
            name=slug,
            title=name.title().replace("-", " ").replace("_", " "),
            description=rich_description,
            summary=summary,
            use_cases=use_cases,
            prerequisites=prerequisites,
            instructions_section=self._generate_instructions_section(
                task_description or description, task_type, instructions
            ),
            tools_inline=tools_inline,
            validation_section=self._generate_validation_section(task_type)
        )
        
        # Write SKILL.md
        skill_path = skill_dir / "SKILL.md"
        skill_path.write_text(content)
        
        logger.info(
            "skill_generated",
            name=slug,
            path=str(skill_path),
            task_type=task_type,
            triggers_count=len(final_triggers),
            tools_count=len(final_tools)
        )
        
        return GeneratedSkill(
            name=slug,
            path=skill_path,
            description=rich_description,
            task_type=task_type,
            triggers=final_triggers,
            instructions=instructions or [],
            context_files=context_files or []
        )
    
    def list_generated_skills(self) -> list[dict[str, Any]]:
        """List all generated skills in the workspace."""
        skills = []
        if not self.skills_dir.exists():
            return skills
        
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    content = skill_md.read_text()
                    # Parse basic info from SKILL.md
                    name = skill_dir.name
                    desc = ""
                    for line in content.split("\n"):
                        if line.startswith("description:"):
                            desc = line.replace("description:", "").strip()
                            break
                    skills.append({
                        "name": name,
                        "path": str(skill_md),
                        "description": desc
                    })
        
        return skills
    
    def delete_skill(self, name: str) -> bool:
        """Delete a generated skill."""
        import shutil
        slug = self._slugify(name)
        skill_dir = self.skills_dir / slug
        
        if skill_dir.exists():
            shutil.rmtree(skill_dir)
            logger.info("skill_deleted", name=slug)
            return True
        return False
    
    async def generate_with_sdk(
        self,
        name: str,
        task_description: str,
        client: "CopilotClient | None" = None,
        template_boost: dict[str, Any] | None = None
    ) -> GeneratedSkill:
        """
        Generate a comprehensive skill using Copilot SDK for intelligent content creation.
        
        This is the core "skill factory" method - the SDK acts as an expert skill designer
        that creates production-ready, highly detailed SKILL.md files.
        
        The SDK analyzes:
        1. The task description to understand intent and scope
        2. Common patterns and best practices for this task type
        3. Optimal tool selection and sequencing
        4. Edge cases and error handling strategies
        
        Args:
            name: Skill name (will be slugified)
            task_description: Detailed description of what the skill should do
            client: Optional CopilotClient instance (creates one if not provided)
            template_boost: Optional template data to guide generation
            
        Returns:
            GeneratedSkill with path to created SKILL.md
        """
        own_client = client is None
        
        if own_client:
            client = CopilotClient()
        
        try:
            # Build template context if available
            template_context = ""
            if template_boost:
                template_context = f"""
I have a starting template that provides some context:
- Suggested triggers: {', '.join(template_boost.get('triggers', []))}
- Recommended tools: {', '.join(template_boost.get('tools', []))}
- Base instructions: {template_boost.get('instructions', [])}

Use this as inspiration but feel free to enhance and adapt based on the specific task description.
"""

            # Build comprehensive prompt for expert skill generation
            prompt = f"""You are an expert Agent Skill designer for GitHub Copilot. Your job is to create comprehensive, production-ready skills that minimize context consumption while maximizing utility.

## Task: Create a skill named "{name}"

## User's Task Description:
{task_description}
{template_context}

## Your Mission:
Create a COMPLETE skill specification that will enable Copilot to handle this task type autonomously and expertly. Think like a senior developer who has done this task hundreds of times - what are ALL the steps, edge cases, and best practices?

## Required Output (JSON format):

{{
    "description": "A rich description (150-250 chars) that explains WHAT the skill does, WHEN to use it, and includes key TRIGGER WORDS. Format: '<What it does>. Use when <trigger conditions>. Keywords: <key terms>.'",
    
    "summary": "A 2-3 sentence overview for the skill documentation explaining the skill's purpose and value.",
    
    "use_cases": [
        "Specific use case 1 with example",
        "Specific use case 2 with example", 
        "Specific use case 3 with example"
    ],
    
    "triggers": [
        "keyword1",
        "keyword2",
        "action phrase",
        "problem indicator",
        "domain term"
    ],
    
    "prerequisites": [
        "Required tool, dependency, or setup 1",
        "Required tool, dependency, or setup 2"
    ],
    
    "instructions": [
        "Step 1: [Specific action with details]",
        "Step 2: [Specific action with details]",
        "Step 3: Continue with comprehensive steps...",
        "...Include 8-12 detailed steps covering the ENTIRE workflow"
    ],
    
    "tools": [
        "tool_name_1",
        "tool_name_2"
    ],
    
    "validation": [
        "Specific success criterion 1",
        "Specific success criterion 2",
        "How to verify the task completed correctly"
    ],
    
    "troubleshooting": [
        {{"issue": "Common problem 1", "solution": "How to fix it"}},
        {{"issue": "Common problem 2", "solution": "How to fix it"}}
    ],
    
    "edge_cases": [
        "Edge case 1 and how to handle it",
        "Edge case 2 and how to handle it"
    ]
}}

## Available Tools (choose the most appropriate):
- read_file: Read file contents
- create_file: Create new files  
- replace_string_in_file: Edit existing files
- run_in_terminal: Execute shell commands
- grep_search: Search for text patterns
- file_search: Find files by path/glob
- semantic_search: Semantic code search
- get_errors: Get compile/lint errors
- runTests: Run test suites
- list_code_usages: Find symbol references
- fetch_webpage: Fetch web documentation

## Quality Guidelines:
1. Instructions should be SPECIFIC and ACTIONABLE, not generic
2. Include error handling and validation steps
3. Consider the user's workflow and minimize friction
4. Triggers should include verbs, nouns, and problem phrases
5. Use_cases should be concrete scenarios developers actually face
6. Validation criteria should be measurable

Respond with ONLY the JSON object, no additional text."""

            response_text = ""
            
            async for chunk in client.send_message(content=prompt):
                if chunk.get("type") == "text":
                    response_text += chunk.get("content", "")
                elif chunk.get("type") == "done":
                    break
            
            # Parse SDK response
            sdk_content = self._parse_sdk_skill_response(response_text)
            
            # Build enhanced content from SDK response
            enhanced_description = sdk_content.get("description", task_description[:200])
            summary = sdk_content.get("summary", "")
            use_cases = sdk_content.get("use_cases", [])
            triggers = sdk_content.get("triggers", [])
            prerequisites = sdk_content.get("prerequisites", [])
            instructions = sdk_content.get("instructions", [])
            tools = sdk_content.get("tools", [])
            validation = sdk_content.get("validation", [])
            troubleshooting = sdk_content.get("troubleshooting", [])
            edge_cases = sdk_content.get("edge_cases", [])
            
            # Generate skill using enhanced content
            skill = await self.generate(
                name=name,
                description=enhanced_description,
                task_description=task_description,
                triggers=triggers if triggers else None,
                instructions=instructions if instructions else None,
                tools=tools if tools else None
            )
            
            # If we got rich content from SDK, enhance the generated SKILL.md
            if summary or use_cases or troubleshooting:
                await self._enhance_skill_md(
                    skill.path,
                    summary=summary,
                    use_cases=use_cases,
                    prerequisites=prerequisites,
                    validation=validation,
                    troubleshooting=troubleshooting,
                    edge_cases=edge_cases
                )
            
            return skill
            
        finally:
            if own_client and client:
                await client.close()
    
    async def _enhance_skill_md(
        self,
        skill_path: Path,
        summary: str = "",
        use_cases: list[str] | None = None,
        prerequisites: list[str] | None = None, 
        validation: list[str] | None = None,
        troubleshooting: list[dict] | None = None,
        edge_cases: list[str] | None = None
    ) -> None:
        """
        Enhance a generated SKILL.md with additional SDK-generated content.
        """
        if not skill_path.exists():
            return
        
        content = skill_path.read_text(encoding="utf-8")
        
        # Build enhanced sections
        enhancements = []
        
        if use_cases:
            use_case_section = "## Use Cases\n\n"
            for uc in use_cases:
                use_case_section += f"- {uc}\n"
            enhancements.append(("## When to Use", use_case_section + "\n## When to Use"))
        
        if prerequisites and "## Prerequisites" in content:
            prereq_section = "## Prerequisites\n\n"
            for pr in prerequisites:
                prereq_section += f"- {pr}\n"
            content = content.replace("## Prerequisites", prereq_section)
        
        if validation:
            validation_section = "\n## Validation Criteria\n\n"
            for v in validation:
                validation_section += f"- [ ] {v}\n"
            # Insert before Troubleshooting
            if "## Troubleshooting" in content:
                content = content.replace("## Troubleshooting", validation_section + "\n## Troubleshooting")
        
        if troubleshooting:
            # Find and replace troubleshooting section
            import re
            trouble_section = "## Troubleshooting\n\n| Issue | Solution |\n|-------|----------|\n"
            for t in troubleshooting:
                issue = t.get("issue", "")
                solution = t.get("solution", "")
                trouble_section += f"| {issue} | {solution} |\n"
            
            # Replace existing troubleshooting
            content = re.sub(
                r'## Troubleshooting.*?(?=## |\Z)',
                trouble_section + "\n",
                content,
                flags=re.DOTALL
            )
        
        if edge_cases:
            edge_section = "\n## Edge Cases\n\n"
            for ec in edge_cases:
                edge_section += f"- {ec}\n"
            # Insert before References
            if "## References" in content:
                content = content.replace("## References", edge_section + "\n## References")
        
        # Write enhanced content
        skill_path.write_text(content, encoding="utf-8")
        logger.info("skill_enhanced", path=str(skill_path))
    
    def _parse_sdk_skill_response(self, response: str) -> dict[str, Any]:
        """Parse SDK response to extract skill content."""
        import json
        import re
        
        # Try to extract JSON from response
        # Handle markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Try direct JSON parse
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # Fallback: return empty dict (will use defaults)
        logger.warning("sdk_response_parse_failed", response_preview=response[:200])
        return {}


# =============================================================================
# RESPONSE RENDERER
# =============================================================================


class ResponseRenderer:
    """
    Render streaming responses with rich formatting.
    
    Handles:
    - Markdown rendering
    - Code syntax highlighting
    - Progress indicators
    - Tool call visualization
    """
    
    def __init__(self) -> None:
        """Initialize renderer."""
        self.console = console
        self._accumulated_text = ""
    
    def render_text(self, text: str, is_streaming: bool = True) -> None:
        """
        Render text content.
        
        Args:
            text: Text to render
            is_streaming: Whether this is part of a stream
        """
        self._accumulated_text += text
        
        if is_streaming:
            # Print raw during streaming for responsiveness
            self.console.print(text, end="")
        else:
            # Render as markdown when complete
            self.console.print(Markdown(text))
    
    def render_code(self, code: str, language: str = "python") -> None:
        """Render code with syntax highlighting."""
        syntax = Syntax(
            code,
            language,
            theme="monokai",
            line_numbers=True,
            word_wrap=True
        )
        self.console.print(Panel(syntax, title=f"[bold]{language}[/bold]"))
    
    def render_tool_call(self, tool_name: str, params: dict[str, Any]) -> None:
        """Render a tool call notification."""
        self.console.print()
        self.console.print(
            Panel(
                f"[bold cyan]Tool:[/bold cyan] {tool_name}\n"
                f"[bold cyan]Parameters:[/bold cyan]\n{json.dumps(params, indent=2)}",
                title="[yellow]🔧 Tool Call[/yellow]",
                border_style="yellow"
            )
        )
    
    def render_tool_result(self, tool_name: str, result: Any) -> None:
        """Render a tool result."""
        result_str = json.dumps(result, indent=2) if isinstance(result, (dict, list)) else str(result)
        
        # Truncate long results
        if len(result_str) > 1000:
            result_str = result_str[:1000] + "\n... (truncated)"
        
        self.console.print(
            Panel(
                result_str,
                title=f"[green]✓ {tool_name} Result[/green]",
                border_style="green"
            )
        )
    
    def render_error(self, error: str) -> None:
        """Render an error message."""
        self.console.print(
            Panel(
                f"[bold red]{error}[/bold red]",
                title="[red]❌ Error[/red]",
                border_style="red"
            )
        )
    
    def render_status(self, message: str) -> None:
        """Render a status message."""
        self.console.print(f"[dim]ℹ {message}[/dim]")
    
    def finish_stream(self) -> str:
        """Complete a streaming response and return accumulated text."""
        self.console.print()  # New line after stream
        text = self._accumulated_text
        self._accumulated_text = ""
        return text
    
    def show_progress(self, message: str) -> Progress:
        """Create a progress indicator."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        )


# =============================================================================
# MAIN ORCHESTRATOR
# =============================================================================


@dataclass
class OrchestratorConfig:
    """
    Configuration for the orchestrator.
    
    Attributes:
        workspace: Root directory for operations
        max_tokens: Maximum context tokens
        max_retries: Maximum retry attempts
        timeout: Request timeout in seconds
        verbose: Enable verbose logging
    """
    workspace: Path = field(default_factory=Path.cwd)
    max_tokens: int = 8000
    max_retries: int = 3
    timeout: int = 60
    verbose: bool = False


class Orchestrator:
    """
    Main orchestrator class - the "skill factory".
    
    When invoked by Copilot (via SKILL.md matching), the orchestrator:
    1. Classifies the user's intent
    2. Decides execution strategy:
       - Direct SDK call for complex tasks
       - Ephemeral skill for specialized operations
    3. Executes and returns results
    
    This creates a "meta-skill" that can handle ANY request by
    dynamically adapting its execution strategy.
    
    Example - User asks Copilot: "list files in this directory"
    --------------------------------------------------------
    1. Copilot matches SKILL.md (broad intent keywords)
    2. Orchestrator receives request
    3. Orchestrator spawns "shell" ephemeral skill
    4. Shell skill executes `ls` or `Get-ChildItem`
    5. Results returned to user via Copilot
    
    Example - User asks: "implement OAuth2 authentication"
    -----------------------------------------------------
    1. Copilot matches SKILL.md
    2. Orchestrator classifies as IMPLEMENT task
    3. Orchestrator uses SDK session with code tools
    4. SDK generates implementation with tests
    5. Artifacts returned to user
    """
    
    def __init__(self, config: OrchestratorConfig | None = None) -> None:
        """
        Initialize orchestrator.
        
        Args:
            config: Configuration options
        """
        self.config = config or OrchestratorConfig()
        
        # Initialize components
        self.classifier = TaskClassifier()
        self.context_manager = ContextManager(
            workspace=self.config.workspace
        )
        self.tool_factory = ToolFactory(workspace=self.config.workspace)
        self.client = CopilotClient()
        self.renderer = ResponseRenderer()
        
        # Ephemeral skill spawner - key for "skill factory" behavior
        self.skill_spawner = EphemeralSkillSpawner(workspace=self.config.workspace)
        
        # Session state
        self.session_info: SessionInfo | None = None
        self._artifacts: list[Artifact] = []
        
        logger.info(
            "orchestrator_initialized",
            workspace=str(self.config.workspace),
            max_tokens=self.config.max_tokens
        )
    
    async def execute(
        self,
        request: str,
        task_type: TaskType | None = None,
        session_id: str | None = None,
        skill_handler_mode: bool = False
    ) -> SessionInfo | dict[str, Any]:
        """
        Execute a user request.
        
        This is the main entry point. It decides between:
        - Spawning an ephemeral skill for simple operations
        - Using full SDK session for complex tasks
        
        Args:
            request: User's request in natural language
            task_type: Override automatic task classification
            session_id: Resume existing session
            skill_handler_mode: If True, return structured data for Copilot
            
        Returns:
            SessionInfo or dict with results
        """
        # First, check if an ephemeral skill can handle this directly
        ephemeral_type = self.skill_spawner.select_skill_type(request)
        
        if ephemeral_type:
            # Fast path: spawn ephemeral skill for specialized operation
            self.renderer.render_status(
                f"Spawning ephemeral skill: {ephemeral_type}"
            )
            
            result = await self.skill_spawner.spawn_and_execute(
                skill_type=ephemeral_type,
                request=request
            )
            
            if skill_handler_mode:
                return result
            
            # Render result for CLI mode
            if result.get("success"):
                if "stdout" in result:
                    self.renderer.render_code(result["stdout"], "text")
                elif "items" in result:
                    for item in result["items"]:
                        icon = "📁" if item["is_dir"] else "📄"
                        self.renderer.render_status(f"{icon} {item['name']}")
                elif "content" in result:
                    self.renderer.render_code(result["content"], "text")
            else:
                self.renderer.render_error(result.get("error", "Unknown error"))
            
            # Return as SessionInfo for consistency
            return SessionInfo(
                session_id=self._generate_session_id(),
                state=SessionState.COMPLETED,
                task=TaskEnvelope(
                    task_type=TaskType.AUTOMATE,
                    original_request=request
                ),
                started_at=datetime.now(),
                ended_at=datetime.now(),
                artifacts=[]
            )
        
        # Full SDK path for complex tasks
        # Classify task if not provided
        if task_type is None:
            task_type, confidence = self.classifier.classify(request)
            self.renderer.render_status(
                f"Classified as: {task_type.value} (confidence: {confidence:.0%})"
            )
        
        # Create task envelope
        envelope = TaskEnvelope(
            task_type=task_type,
            original_request=request
        )
        
        # Initialize session
        self.session_info = SessionInfo(
            session_id=session_id or self._generate_session_id(),
            state=SessionState.INITIALIZING,
            task=envelope,
            started_at=datetime.now()
        )
        
        try:
            # Gather context
            self.renderer.render_status("Gathering context...")
            context = await self._gather_context(envelope)
            envelope.compressed_context = context
            
            # Get tools for task
            tools = self.tool_factory.get_tools_for_task(task_type)
            tool_defs = self.tool_factory.to_sdk_tools(tools)
            
            # Build tool handlers map for real SDK mode
            tool_handlers = {
                tool.definition.name: tool.execute
                for tool in tools
            }
            self.client.set_tool_handlers(tool_handlers)
            
            self.renderer.render_status(
                f"Registered {len(tools)} tools for {task_type.value}"
            )
            
            # Create SDK session
            system_prompt = self._build_system_prompt(envelope)
            await self.client.create_session(tool_defs, system_prompt)
            
            self.session_info.state = SessionState.ACTIVE
            
            # Execute conversation loop
            await self._conversation_loop(envelope)
            
            # Finalize
            self.session_info.state = SessionState.COMPLETED
            self.session_info.ended_at = datetime.now()
            self.session_info.artifacts = self._artifacts
            
            return self.session_info
            
        except Exception as e:
            logger.error("orchestrator_error", error=str(e))
            self.renderer.render_error(str(e))
            
            if self.session_info:
                self.session_info.state = SessionState.ERROR
                self.session_info.ended_at = datetime.now()
            
            raise
        
        finally:
            await self.client.close()
    
    async def _gather_context(self, envelope: TaskEnvelope) -> CompressedContext:
        """
        Gather and compress context for the task.
        
        Uses progressive disclosure:
        1. Start with workspace structure
        2. Add relevant files based on task
        3. Compress to fit token budget
        """
        return await self.context_manager.prepare_context(
            task_type=envelope.task_type,
            request=envelope.original_request,
            budget=envelope.token_budget
        )
    
    def _build_system_prompt(self, envelope: TaskEnvelope) -> str:
        """
        Build system prompt for the SDK session.
        
        The prompt:
        - Establishes the assistant role
        - Describes available tools
        - Sets task-specific guidelines
        """
        return f"""You are an expert software development assistant operating in a {envelope.task_type.value} context.

Your capabilities:
- Read and analyze code files
- Write and modify files
- Execute commands and tests
- Search for patterns and dependencies

Guidelines for {envelope.task_type.value}:
{self._get_task_guidelines(envelope.task_type)}

Important:
- Always verify your understanding before making changes
- Use tools to gather information before acting
- Explain your reasoning
- Handle errors gracefully"""
    
    def _get_task_guidelines(self, task_type: TaskType) -> str:
        """Get specific guidelines for a task type."""
        guidelines = {
            TaskType.IMPLEMENT: """
- Understand requirements thoroughly before coding
- Follow existing code patterns and conventions
- Write clear, documented code
- Include error handling
- Suggest tests for new functionality""",
            
            TaskType.DEBUG: """
- Reproduce the issue first
- Examine error messages and stack traces
- Check recent changes
- Isolate the problem systematically
- Verify the fix doesn't introduce new issues""",
            
            TaskType.REFACTOR: """
- Ensure tests exist before refactoring
- Make small, incremental changes
- Preserve existing behavior
- Improve readability and maintainability
- Update documentation as needed""",
            
            TaskType.TEST: """
- Cover both positive and negative cases
- Test edge cases and boundaries
- Use descriptive test names
- Keep tests independent
- Mock external dependencies""",
            
            TaskType.ANALYZE: """
- Examine code structure and patterns
- Identify dependencies and relationships
- Note potential issues or improvements
- Provide clear, actionable insights
- Use concrete examples"""
        }
        
        return guidelines.get(task_type, "- Follow best practices\n- Be thorough and careful")
    
    async def _conversation_loop(self, envelope: TaskEnvelope) -> None:
        """
        Main conversation loop with the SDK.
        
        Processes:
        1. Send initial request with context
        2. Stream response chunks
        3. Execute any tool calls
        4. Continue until done or max iterations
        """
        max_iterations = 20
        iteration = 0
        
        # Initial message
        prompt = envelope.build_prompt()
        
        while iteration < max_iterations:
            iteration += 1
            
            # Stream response
            async for chunk in self.client.send_message(
                content=prompt if iteration == 1 else "",
                context=envelope.compressed_context if iteration == 1 else None
            ):
                if chunk["type"] == "text":
                    self.renderer.render_text(chunk["content"])
                
                elif chunk["type"] == "tool_call":
                    self.renderer.finish_stream()
                    
                    # Execute tool
                    tool_name = chunk["tool"]
                    params = chunk["parameters"]
                    
                    self.renderer.render_tool_call(tool_name, params)
                    
                    result = await self._execute_tool(tool_name, params)
                    
                    self.renderer.render_tool_result(tool_name, result)
                    
                    # Submit result and continue
                    async for cont_chunk in self.client.submit_tool_result(tool_name, result):
                        if cont_chunk["type"] == "text":
                            self.renderer.render_text(cont_chunk["content"])
                        elif cont_chunk["type"] == "done":
                            break
                
                elif chunk["type"] == "done":
                    self.renderer.finish_stream()
                    return
            
            # Check if should continue
            # In production, check for explicit continuation signals
            break
    
    async def _execute_tool(
        self,
        tool_name: str,
        params: dict[str, Any]
    ) -> Any:
        """
        Execute a tool and track artifacts.
        
        Args:
            tool_name: Name of tool to execute
            params: Tool parameters
            
        Returns:
            Tool execution result
        """
        result = await self.tool_factory.execute_tool(tool_name, params)
        
        # Track file artifacts
        if tool_name == "write_file" and result.get("success"):
            from models import ArtifactType
            self._artifacts.append(Artifact(
                artifact_type=ArtifactType.CODE,
                path=Path(result.get("path", "")),
                content=params.get("content", ""),
                created_at=datetime.now()
            ))
        
        return result
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        from uuid import uuid4
        return f"session_{uuid4().hex[:12]}"
    
    async def resume(self, session_id: str) -> SessionInfo:
        """
        Resume a previous session.
        
        Loads checkpoint and continues from last state.
        
        Args:
            session_id: ID of session to resume
            
        Returns:
            Resumed session info
        """
        checkpoint = ContextCheckpoint(storage_dir=self.config.workspace / ".copilot")
        
        state = checkpoint.restore(session_id)
        if not state:
            raise ValueError(f"No checkpoint found for session: {session_id}")
        
        self.renderer.render_status(f"Resuming session {session_id}")
        
        # Re-create envelope from checkpoint
        envelope = TaskEnvelope(
            task_type=TaskType(state["task_type"]),
            original_request=state["original_request"]
        )
        
        return await self.execute(
            request=envelope.original_request,
            task_type=envelope.task_type,
            session_id=session_id
        )


# =============================================================================
# CLI INTERFACE
# =============================================================================


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Universal Copilot Orchestrator - Skill Factory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Invocation Modes:
  Skill Handler:  Invoked by Copilot when SKILL.md matches
  CLI:            Direct command-line usage for testing
  Skill Factory:  Generate reusable SKILL.md files
  
Examples:
  # Skill handler mode (used by Copilot)
  %(prog)s --skill-handler --request "list files in src/"
  
  # CLI mode for testing
  %(prog)s "implement user authentication"
  %(prog)s "list files in current directory"
  %(prog)s --task-type debug "fix the login error"
  %(prog)s --workspace /path/to/project "add unit tests"
  
  # Skill factory mode - generate reusable skills
  %(prog)s --generate-skill --skill-name "api-creator" "Create REST API endpoints with validation and error handling"
  %(prog)s --generate-skill --skill-name "test-writer" --skill-description "Write comprehensive unit tests"
  %(prog)s --list-skills
  %(prog)s --delete-skill api-creator

The value of generating skills is MINIMIZING CONTEXT CONSUMPTION:
- Full orchestrator: ~8K tokens loaded every time
- Generated skill: ~500-1500 tokens, focused on specific task
- Copilot can match lightweight skills for common operations
        """
    )
    
    parser.add_argument(
        "request",
        nargs="?",
        help="The request to process (natural language)"
    )
    
    parser.add_argument(
        "--skill-handler",
        action="store_true",
        help="Run in skill handler mode (invoked by Copilot)"
    )
    
    parser.add_argument(
        "--request", "-r",
        dest="request_flag",
        help="Request when using --skill-handler mode"
    )
    
    parser.add_argument(
        "--task-type", "-t",
        choices=[t.value for t in TaskType],
        help="Override automatic task classification"
    )
    
    parser.add_argument(
        "--workspace", "-w",
        type=Path,
        default=Path.cwd(),
        help="Workspace directory (default: current)"
    )
    
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=8000,
        help="Maximum context tokens (default: 8000)"
    )
    
    parser.add_argument(
        "--resume",
        metavar="SESSION_ID",
        help="Resume a previous session"
    )
    
    parser.add_argument(
        "--output-json",
        action="store_true",
        help="Output results as JSON (for skill handler mode)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    # Skill generation arguments
    parser.add_argument(
        "--generate-skill",
        action="store_true",
        help="Generate a new SKILL.md file instead of executing a task"
    )
    
    parser.add_argument(
        "--skill-name",
        help="Name for the generated skill (required with --generate-skill)"
    )
    
    parser.add_argument(
        "--skill-description",
        help="One-line description for the generated skill"
    )
    
    parser.add_argument(
        "--list-skills",
        action="store_true",
        help="List all generated skills in the workspace"
    )
    
    parser.add_argument(
        "--delete-skill",
        metavar="SKILL_NAME",
        help="Delete a generated skill"
    )
    
    parser.add_argument(
        "--use-sdk",
        action="store_true",
        help="Use Copilot SDK to generate intelligent skill content (requires SDK setup)"
    )
    
    # Skill Catalog features (mother of all skills)
    parser.add_argument(
        "--find-skill",
        metavar="REQUEST",
        help="Find existing skills that match a request"
    )
    
    parser.add_argument(
        "--suggest-template",
        metavar="REQUEST",
        help="Suggest a skill template for a request"
    )
    
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="List all available skill templates"
    )
    
    parser.add_argument(
        "--from-template",
        metavar="TEMPLATE_NAME",
        help="Generate skill starting from a template (use with --generate-skill)"
    )
    
    parser.add_argument(
        "--auto-skill",
        metavar="REQUEST",
        help="Auto-generate a specialized skill if no matching skill exists"
    )
    
    return parser.parse_args()


async def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    workspace = args.workspace.resolve()
    
    # =========================================================================
    # SKILL MANAGEMENT MODES
    # =========================================================================
    
    # List skills mode
    if args.list_skills:
        generator = SkillGenerator(workspace)
        skills = generator.list_generated_skills()
        
        if not skills:
            console.print("[yellow]No skills found in workspace[/yellow]")
            return 0
        
        console.print(Panel(
            "\n".join(
                f"[bold cyan]{s['name']}[/bold cyan]\n  {s['description']}\n  [dim]{s['path']}[/dim]"
                for s in skills
            ),
            title="Generated Skills"
        ))
        return 0
    
    # Delete skill mode
    if args.delete_skill:
        generator = SkillGenerator(workspace)
        if generator.delete_skill(args.delete_skill):
            console.print(f"[green]✓ Deleted skill: {args.delete_skill}[/green]")
            return 0
        else:
            console.print(f"[red]Skill not found: {args.delete_skill}[/red]")
            return 1
    
    # =========================================================================
    # SKILL CATALOG MODES (Mother of All Skills)
    # =========================================================================
    
    # List templates mode
    if args.list_templates:
        console.print(Panel(
            "\n".join(
                f"[bold cyan]{key}[/bold cyan]\n"
                f"  {data['description'][:100]}{'...' if len(data['description']) > 100 else ''}\n"
                f"  [dim]Triggers: {', '.join(data['triggers'][:5])}{'...' if len(data['triggers']) > 5 else ''}[/dim]"
                for key, data in SKILL_TEMPLATES.items()
            ),
            title="Available Skill Templates"
        ))
        return 0
    
    # Find matching skills mode
    if args.find_skill:
        catalog = SkillCatalog(workspace)
        matches = await catalog.find_matching_skills(args.find_skill)
        
        if not matches:
            console.print(f"[yellow]No skills match: '{args.find_skill}'[/yellow]")
            
            # Suggest template
            template = catalog.suggest_template(args.find_skill)
            if template:
                console.print(f"\n[dim]Suggested template: [bold]{template}[/bold][/dim]")
                console.print(f"[dim]Generate with: --auto-skill \"{args.find_skill}\"[/dim]")
            return 0
        
        console.print(Panel(
            "\n".join(
                f"[bold cyan]{m.name}[/bold cyan] [dim]({m.match_score:.0%} match)[/dim]\n"
                f"  {m.description[:80]}{'...' if len(m.description) > 80 else ''}\n"
                f"  [dim]Matched: {', '.join(m.matched_keywords[:5])}[/dim]"
                for m in matches[:5]
            ),
            title=f"Matching Skills for '{args.find_skill[:40]}...'" if len(args.find_skill) > 40 else f"Matching Skills for '{args.find_skill}'"
        ))
        return 0
    
    # Suggest template mode
    if args.suggest_template:
        catalog = SkillCatalog(workspace)
        template = catalog.suggest_template(args.suggest_template)
        
        if template:
            data = SKILL_TEMPLATES[template]
            console.print(Panel(
                f"[bold]Template:[/bold] {template}\n\n"
                f"[bold]Description:[/bold]\n{data['description']}\n\n"
                f"[bold]Triggers:[/bold] {', '.join(data['triggers'])}\n\n"
                f"[bold]Tools:[/bold] {', '.join(data['tools'])}\n\n"
                f"[bold]To generate:[/bold]\n"
                f"  --generate-skill --skill-name my-skill --from-template {template} \"Your description\"",
                title=f"Suggested Template: {template}"
            ))
        else:
            console.print(f"[yellow]No template matches: '{args.suggest_template}'[/yellow]")
            console.print("[dim]Available templates: " + ", ".join(SKILL_TEMPLATES.keys()) + "[/dim]")
        return 0
    
    # Auto-skill mode (intelligent skill creation)
    if args.auto_skill:
        catalog = SkillCatalog(workspace)
        
        # Check if we should create a skill
        should_create, reason = await catalog.should_create_skill(args.auto_skill)
        
        if not should_create:
            console.print(f"[yellow]{reason}[/yellow]")
            matches = await catalog.find_matching_skills(args.auto_skill)
            if matches:
                console.print(f"\n[dim]Best match: {matches[0].name} ({matches[0].match_score:.0%})[/dim]")
            return 0
        
        console.print(f"[dim]{reason}[/dim]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            progress.add_task("Creating specialized skill with SDK...", total=None)
            
            skill = await catalog.generate_specialized_skill(
                request=args.auto_skill,
                use_sdk=True
            )
        
        console.print(Panel(
            f"[bold green]✓ Specialized Skill Created[/bold green]\n\n"
            f"[bold]Name:[/bold] {skill.name}\n"
            f"[bold]Path:[/bold] {skill.path}\n"
            f"[bold]Type:[/bold] {skill.task_type}\n"
            f"[bold]Triggers:[/bold] {', '.join(skill.triggers[:5])}{'...' if len(skill.triggers) > 5 else ''}\n\n"
            f"[dim]This skill was auto-generated from your request and will be matched automatically.[/dim]",
            title="Skill Factory"
        ))
        
        if args.output_json:
            print(json.dumps({
                "name": skill.name,
                "path": str(skill.path),
                "description": skill.description,
                "task_type": skill.task_type,
                "triggers": skill.triggers
            }, indent=2))
        
        return 0
    
    # Generate skill mode
    if args.generate_skill:
        if not args.skill_name:
            console.print("[red]Error: --skill-name is required with --generate-skill[/red]")
            return 1
        
        # Use request as task description
        request = args.request or args.request_flag or ""
        description = args.skill_description or request or f"Skill for {args.skill_name}"
        
        # Get template boost if specified
        template_boost = None
        if hasattr(args, 'from_template') and args.from_template:
            if args.from_template in SKILL_TEMPLATES:
                template_boost = SKILL_TEMPLATES[args.from_template]
                console.print(f"[dim]Using template: {args.from_template}[/dim]")
            else:
                console.print(f"[yellow]Template '{args.from_template}' not found. Available: {', '.join(SKILL_TEMPLATES.keys())}[/yellow]")
        
        generator = SkillGenerator(workspace)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            if args.use_sdk:
                progress.add_task("Generating skill with SDK...", total=None)
                skill = await generator.generate_with_sdk(
                    name=args.skill_name,
                    task_description=description,
                    template_boost=template_boost
                )
            else:
                progress.add_task("Generating skill...", total=None)
                skill = await generator.generate(
                    name=args.skill_name,
                    description=description,
                    task_description=request if request else None,
                    triggers=template_boost.get("triggers") if template_boost else None,
                    instructions=template_boost.get("instructions") if template_boost else None,
                    tools=template_boost.get("tools") if template_boost else None
                )
        
        console.print(Panel(
            f"[bold green]✓ Skill Generated[/bold green]\n\n"
            f"[bold]Name:[/bold] {skill.name}\n"
            f"[bold]Path:[/bold] {skill.path}\n"
            f"[bold]Type:[/bold] {skill.task_type}\n"
            f"[bold]Triggers:[/bold] {', '.join(skill.triggers[:5])}{'...' if len(skill.triggers) > 5 else ''}\n\n"
            f"[dim]The skill is ready to use. Copilot will automatically match it based on triggers.[/dim]",
            title="Skill Generator"
        ))
        
        if args.output_json:
            print(json.dumps({
                "name": skill.name,
                "path": str(skill.path),
                "description": skill.description,
                "task_type": skill.task_type,
                "triggers": skill.triggers
            }, indent=2))
        
        return 0
    
    # =========================================================================
    # TASK EXECUTION MODE
    # =========================================================================
    
    # Get request from either positional arg or --request flag
    request = args.request or args.request_flag
    
    # Validate arguments
    if not args.resume and not request:
        console.print("[red]Error: Either request or --resume is required[/red]")
        console.print("\n[dim]Usage examples:[/dim]")
        console.print("  orchestrator.py \"implement user authentication\"")
        console.print("  orchestrator.py --generate-skill --skill-name my-skill \"description of what it does\"")
        console.print("  orchestrator.py --list-skills")
        return 1
    
    # Configure
    config = OrchestratorConfig(
        workspace=workspace,
        max_tokens=args.max_tokens,
        verbose=args.verbose
    )
    
    # Create orchestrator
    orch = Orchestrator(config)
    
    try:
        if args.resume:
            # Resume existing session
            result = await orch.resume(args.resume)
        else:
            # New session
            task_type = TaskType(args.task_type) if args.task_type else None
            result = await orch.execute(
                request,
                task_type=task_type,
                skill_handler_mode=args.skill_handler
            )
        
        # Output mode
        if args.output_json or args.skill_handler:
            # JSON output for skill handler mode
            if isinstance(result, dict):
                print(json.dumps(result, indent=2, default=str))
            else:
                print(json.dumps({
                    "session_id": result.session_id,
                    "state": result.state.value,
                    "artifacts": [
                        {"type": a.artifact_type, "path": str(a.path)}
                        for a in (result.artifacts or [])
                    ]
                }, indent=2))
        else:
            # Rich console summary for CLI mode
            if isinstance(result, SessionInfo):
                console.print()
                console.print(Panel(
                    f"[bold green]Session Complete[/bold green]\n\n"
                    f"Session ID: {result.session_id}\n"
                    f"State: {result.state.value}\n"
                    f"Artifacts: {len(result.artifacts or [])}\n"
                    f"Duration: {(result.ended_at - result.started_at).total_seconds():.1f}s"
                    if result.ended_at else "In progress",
                    title="Summary"
                ))
        
        return 0
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        return 130
    except Exception as e:
        if config.verbose:
            console.print_exception()
        else:
            console.print(f"[red]Error: {e}[/red]")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
