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
    cli_path = os.environ.get("GITHUB_COPILOT_CLI_PATH")
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

# Set CLI path if found
_cli_path = _find_copilot_cli()
if _cli_path and not os.environ.get("GITHUB_COPILOT_CLI_PATH"):
    os.environ["GITHUB_COPILOT_CLI_PATH"] = _cli_path
    logger.debug("copilot_cli_found", path=_cli_path)

# Check if the real SDK is available
try:
    from agent_framework.github import GitHubCopilotAgent, GitHubCopilotOptions
    _SDK_AVAILABLE = True
except ImportError:
    _SDK_AVAILABLE = False
    logger.debug("agent_framework_not_available", message="Running in mock mode")


class CopilotClient:
    """
    Wrapper around GitHub Copilot SDK.
    
    Handles:
    - Session creation and management
    - Tool registration
    - Message streaming
    - Error recovery with retries
    
    Supports both real SDK mode (via agent-framework-github-copilot)
    and mock mode for development/testing.
    
    Environment Variables:
        COPILOT_MOCK_MODE: Set to "true" to force mock mode
        GITHUB_COPILOT_MODEL: Model to use (default: gpt-4o)
        GITHUB_COPILOT_TIMEOUT: Request timeout in seconds
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
        self._agent: Any = None  # GitHubCopilotAgent when using real SDK
        
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
        Set tool execution handlers for real SDK mode.
        
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
        Create a new Copilot session.
        
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
        
        if not self._mock_mode and _SDK_AVAILABLE:
            # Create real SDK agent with tools as functions
            sdk_tools = self._create_sdk_tool_functions()
            
            model_name = os.environ.get("GITHUB_COPILOT_MODEL", "gpt-4o")
            options = GitHubCopilotOptions(
                instructions=system_prompt or "You are a helpful coding assistant.",
                model=model_name,
            )
            
            self._agent = GitHubCopilotAgent(
                default_options=options,
                tools=sdk_tools if sdk_tools else None,
            )
            
            logger.info(
                "sdk_session_created",
                session_id=self._session_id,
                tool_count=len(sdk_tools),
                model=model_name
            )
        else:
            logger.info(
                "mock_session_created",
                session_id=self._session_id,
                tool_count=len(tools)
            )
        
        return self._session_id
    
    def _create_sdk_tool_functions(self) -> list[Callable[..., Any]]:
        """
        Create SDK-compatible tool functions from registered tools.
        
        The SDK expects tool functions with type hints that it introspects
        to generate schemas. We create wrapper functions for each tool.
        """
        sdk_tools: list[Callable[..., Any]] = []
        
        for tool_def in self._tools:
            name = tool_def["name"]
            description = tool_def["description"]
            
            if name in self._tool_handlers:
                handler = self._tool_handlers[name]
                
                # Create a wrapper that matches SDK expectations
                async def tool_wrapper(
                    _handler: Callable = handler,
                    _name: str = name,
                    **kwargs: Any
                ) -> dict[str, Any]:
                    """Wrapper to execute tool via handler."""
                    try:
                        result = await _handler(kwargs)
                        return result
                    except Exception as e:
                        logger.error("tool_execution_error", tool=_name, error=str(e))
                        return {"error": str(e), "success": False}
                
                # Set function metadata for SDK introspection
                tool_wrapper.__name__ = name
                tool_wrapper.__doc__ = description
                
                sdk_tools.append(tool_wrapper)
        
        return sdk_tools
    
    async def send_message(
        self,
        content: str,
        context: CompressedContext | None = None
    ) -> AsyncIterator[dict[str, Any]]:
        """
        Send a message and stream the response.
        
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
        
        if not self._mock_mode and self._agent is not None:
            # Use real SDK streaming
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
        Stream response from real SDK.
        
        The GitHubCopilotAgent handles tool calls internally, so we
        yield text chunks as they arrive. Tool calls are handled
        automatically by the wrapped tool functions.
        
        Falls back to mock mode if SDK fails (e.g., CLI not installed).
        """
        if self._agent is None:
            yield {"type": "done"}
            return
            
        try:
            async with self._agent:
                async for chunk in self._agent.run_stream(content):
                    if hasattr(chunk, 'text') and chunk.text:
                        yield {"type": "text", "content": chunk.text}
                    elif hasattr(chunk, 'tool_call') and chunk.tool_call:
                        # Emit tool call for UI rendering (tool is auto-executed by SDK)
                        yield {
                            "type": "tool_call",
                            "tool": chunk.tool_call.name,
                            "parameters": chunk.tool_call.arguments,
                            "auto_executed": True  # SDK handles execution
                        }
                    elif hasattr(chunk, 'tool_result') and chunk.tool_result:
                        # Tool result from SDK-executed tool
                        yield {
                            "type": "tool_result",
                            "tool": chunk.tool_result.name,
                            "result": chunk.tool_result.output
                        }
            
            yield {"type": "done"}
            
        except Exception as e:
            error_msg = str(e)
            logger.error("sdk_stream_error", error=error_msg)
            
            # Check if it's a CLI-not-found error - fall back to mock mode
            if "Failed to start GitHub Copilot client" in error_msg or "cannot find the file" in error_msg.lower():
                logger.warning(
                    "sdk_fallback_to_mock",
                    reason="GitHub Copilot CLI not found. See: https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line"
                )
                # Fall back to mock response
                for chunk in self._generate_mock_response(content):
                    yield chunk
                    await asyncio.sleep(0.02)
                yield {"type": "done"}
            else:
                yield {"type": "error", "content": error_msg}
                yield {"type": "done"}
    
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
  
Examples:
  # Skill handler mode (used by Copilot)
  %(prog)s --skill-handler --request "list files in src/"
  
  # CLI mode for testing
  %(prog)s "implement user authentication"
  %(prog)s "list files in current directory"
  %(prog)s --task-type debug "fix the login error"
  %(prog)s --workspace /path/to/project "add unit tests"
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
    
    return parser.parse_args()


async def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    # Get request from either positional arg or --request flag
    request = args.request or args.request_flag
    
    # Validate arguments
    if not args.resume and not request:
        console.print("[red]Error: Either request or --resume is required[/red]")
        return 1
    
    # Configure
    config = OrchestratorConfig(
        workspace=args.workspace.resolve(),
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
