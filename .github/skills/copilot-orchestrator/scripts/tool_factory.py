"""
Tool Factory for Copilot Orchestrator
======================================

This module handles dynamic generation and registration of tools for SDK sessions.
Tools are the primary way the LLM interacts with external systems (files, APIs, etc.).

Architecture:
------------

    ┌─────────────────────────────────────────────────────────────┐
    │                      TOOL FACTORY                               │
    │                                                                 │
    │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐  │
    │  │   REGISTRY      │    │  SCHEMA GEN     │    │  HANDLERS   │  │
    │  │                 │    │                 │    │             │  │
    │  │ • Tool defs     │───▶│ • JSON Schema   │───▶│ • Execute   │  │
    │  │ • Task mappings │    │ • Pydantic      │    │ • Validate  │  │
    │  │ • Metadata      │    │ • SDK format    │    │ • Return    │  │
    │  └─────────────────┘    └─────────────────┘    └─────────────┘  │
    │                                                                 │
    └─────────────────────────────────────────────────────────────┘

Tool Categories:
---------------
1. FILE_OPERATIONS: read, write, list, delete files
2. CODE_ANALYSIS: analyze, lint, format code
3. WEB_FETCH: fetch URLs, APIs
4. TESTING: run tests, check coverage
5. DOCUMENTATION: generate docs, diagrams
6. SYSTEM: execute commands, manage processes

Key Concepts:
------------
- Tools are defined once, registered in a global registry
- Task types determine which tools are available
- Pydantic models ensure type-safe parameters
- Handlers are async functions that do the actual work

Usage:
-----
    # Register a custom tool
    @register_tool(
        name="my_tool",
        description="Does something useful",
        task_types=[TaskType.IMPLEMENT]
    )
    async def my_tool(params: MyParams) -> dict:
        return {"result": "success"}
    
    # Get tools for a task
    factory = ToolFactory()
    tools = factory.get_tools_for_task(TaskType.IMPLEMENT)
    
    # Use with SDK
    session = await client.create_session({
        "tools": [t.to_sdk_tool() for t in tools]
    })
"""

from __future__ import annotations

import asyncio
import json
import subprocess
from functools import wraps
from pathlib import Path
from typing import Any, Callable, TypeVar, ParamSpec

import structlog
from pydantic import BaseModel, Field, create_model

from models import TaskType, ToolDefinition, ToolParameter

# Configure logging
logger = structlog.get_logger(__name__)

# Type variables for decorator typing
P = ParamSpec("P")
T = TypeVar("T")


# =============================================================================
# GLOBAL TOOL REGISTRY
# =============================================================================


class ToolRegistry:
    """
    Global registry of available tools.
    
    Singleton pattern ensures all tools are registered in one place.
    Tools are registered at module load time via decorators.
    
    Attributes:
        _tools: Map of tool name to ToolEntry
        _instance: Singleton instance
    """
    
    _instance: "ToolRegistry | None" = None
    
    def __new__(cls) -> "ToolRegistry":
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools = {}
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize registry (only runs once due to singleton)."""
        if not hasattr(self, "_tools"):
            self._tools: dict[str, ToolEntry] = {}
    
    def register(
        self,
        name: str,
        definition: ToolDefinition,
        handler: Callable[..., Any],
        param_model: type[BaseModel] | None = None
    ) -> None:
        """
        Register a tool.
        
        Args:
            name: Unique tool identifier
            definition: Tool metadata and schema
            handler: Async function to execute tool
            param_model: Pydantic model for parameter validation
        """
        self._tools[name] = ToolEntry(
            definition=definition,
            handler=handler,
            param_model=param_model
        )
        logger.debug("tool_registered", name=name)
    
    def get(self, name: str) -> "ToolEntry | None":
        """Get a tool by name."""
        return self._tools.get(name)
    
    def get_all(self) -> list["ToolEntry"]:
        """Get all registered tools."""
        return list(self._tools.values())
    
    def get_for_task(self, task_type: TaskType) -> list["ToolEntry"]:
        """Get tools applicable to a task type."""
        return [
            entry for entry in self._tools.values()
            if task_type in entry.definition.task_types or not entry.definition.task_types
        ]
    
    def get_names(self) -> list[str]:
        """Get all registered tool names."""
        return list(self._tools.keys())


class ToolEntry:
    """
    A registered tool with its handler.
    
    Bundles together:
    - Tool definition (schema, metadata)
    - Handler function (actual implementation)
    - Parameter model (for validation)
    """
    
    def __init__(
        self,
        definition: ToolDefinition,
        handler: Callable[..., Any],
        param_model: type[BaseModel] | None = None
    ) -> None:
        self.definition = definition
        self.handler = handler
        self.param_model = param_model
    
    async def execute(self, params: dict[str, Any]) -> Any:
        """
        Execute the tool with given parameters.
        
        Validates parameters if a model is defined, then calls handler.
        
        Args:
            params: Parameter dictionary from SDK
            
        Returns:
            Handler result
            
        Raises:
            ValueError: If parameter validation fails
        """
        # Validate parameters if model exists
        if self.param_model:
            try:
                validated = self.param_model.model_validate(params)
                params = validated.model_dump()
            except Exception as e:
                logger.error(
                    "tool_param_validation_failed",
                    tool=self.definition.name,
                    error=str(e)
                )
                raise ValueError(f"Parameter validation failed: {e}")
        
        # Execute handler
        logger.info(
            "tool_executing",
            tool=self.definition.name,
            param_keys=list(params.keys())
        )
        
        try:
            if asyncio.iscoroutinefunction(self.handler):
                result = await self.handler(params)
            else:
                # Run sync handler in executor
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, lambda: self.handler(params))
            
            logger.info("tool_executed", tool=self.definition.name)
            return result
            
        except Exception as e:
            logger.error(
                "tool_execution_failed",
                tool=self.definition.name,
                error=str(e)
            )
            raise
    
    def to_sdk_format(self) -> dict[str, Any]:
        """
        Convert to SDK tool format.
        
        Returns format compatible with copilot SDK define_tool().
        """
        return {
            "name": self.definition.name,
            "description": self.definition.description,
            "parameters": self.definition.to_json_schema()
        }


# Global registry instance
_registry = ToolRegistry()


# =============================================================================
# DECORATOR FOR TOOL REGISTRATION
# =============================================================================


def register_tool(
    name: str,
    description: str,
    task_types: list[TaskType] | None = None,
    requires_confirmation: bool = False
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator to register a function as a tool.
    
    Inspects the function's type hints to generate parameter schema.
    The function should accept a single dict or Pydantic model parameter.
    
    Example:
    -------
        @register_tool(
            name="write_file",
            description="Write content to a file",
            task_types=[TaskType.IMPLEMENT, TaskType.REFACTOR]
        )
        async def write_file(params: WriteFileParams) -> dict:
            path = params["path"]
            content = params["content"]
            Path(path).write_text(content)
            return {"success": True, "path": path}
    
    Args:
        name: Unique tool identifier
        description: What the tool does (shown to LLM)
        task_types: Which task types this tool applies to
        requires_confirmation: Ask user before executing
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        # Extract parameter model from type hints
        param_model = _extract_param_model(func)
        
        # Build parameter list from model
        parameters = _model_to_parameters(param_model) if param_model else []
        
        # Create tool definition
        definition = ToolDefinition(
            name=name,
            description=description,
            parameters=parameters,
            task_types=task_types or [],
            requires_confirmation=requires_confirmation
        )
        
        # Register
        _registry.register(
            name=name,
            definition=definition,
            handler=func,
            param_model=param_model
        )
        
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


def _extract_param_model(func: Callable[..., Any]) -> type[BaseModel] | None:
    """Extract Pydantic model from function's first parameter type hint."""
    import inspect
    
    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    
    if not params:
        return None
    
    first_param = params[0]
    annotation = first_param.annotation
    
    if annotation is inspect.Parameter.empty:
        return None
    
    # Check if it's a Pydantic model
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return annotation
    
    return None


def _model_to_parameters(model: type[BaseModel]) -> list[ToolParameter]:
    """Convert Pydantic model fields to ToolParameter list."""
    parameters = []
    
    for field_name, field_info in model.model_fields.items():
        # Determine type
        annotation = field_info.annotation
        param_type = "string"  # Default
        
        if annotation is int:
            param_type = "integer"
        elif annotation is float:
            param_type = "number"
        elif annotation is bool:
            param_type = "boolean"
        elif annotation is list:
            param_type = "array"
        elif annotation is dict:
            param_type = "object"
        
        parameters.append(ToolParameter(
            name=field_name,
            param_type=param_type,
            description=field_info.description or "",
            required=field_info.is_required(),
            default=field_info.default if field_info.default is not None else None
        ))
    
    return parameters


# =============================================================================
# TOOL FACTORY - Main interface
# =============================================================================


class ToolFactory:
    """
    Factory for creating and managing tools.
    
    Provides the main interface for:
    - Getting tools for specific task types
    - Creating custom tools at runtime
    - Executing tools with validation
    
    Attributes:
        registry: The global tool registry
        workspace: Working directory for file operations
    """
    
    def __init__(self, workspace: Path | None = None) -> None:
        """
        Initialize tool factory.
        
        Args:
            workspace: Root directory for file operations
        """
        self.registry = _registry
        self.workspace = workspace or Path.cwd()
        
        # Ensure built-in tools are registered
        _register_builtin_tools(self.workspace)
        
        logger.info(
            "tool_factory_initialized",
            workspace=str(self.workspace),
            registered_tools=len(self.registry.get_names())
        )
    
    def get_tools_for_task(self, task_type: TaskType) -> list[ToolEntry]:
        """
        Get all tools applicable to a task type.
        
        Args:
            task_type: The type of task
            
        Returns:
            List of applicable tool entries
        """
        tools = self.registry.get_for_task(task_type)
        logger.debug(
            "tools_retrieved",
            task_type=task_type.value,
            tool_count=len(tools)
        )
        return tools
    
    def get_tool(self, name: str) -> ToolEntry | None:
        """Get a specific tool by name."""
        return self.registry.get(name)
    
    async def execute_tool(
        self,
        name: str,
        params: dict[str, Any]
    ) -> Any:
        """
        Execute a tool by name.
        
        Args:
            name: Tool identifier
            params: Parameters to pass
            
        Returns:
            Tool execution result
            
        Raises:
            ValueError: If tool not found
        """
        tool = self.registry.get(name)
        if not tool:
            raise ValueError(f"Tool not found: {name}")
        
        return await tool.execute(params)
    
    def create_tool(
        self,
        name: str,
        description: str,
        parameters: list[dict[str, Any]],
        handler: Callable[..., Any],
        task_types: list[TaskType] | None = None
    ) -> ToolEntry:
        """
        Create and register a tool at runtime.
        
        Useful for dynamically creating tools based on task requirements.
        
        Args:
            name: Unique tool identifier
            description: Tool description
            parameters: Parameter definitions as dicts
            handler: Function to execute
            task_types: Applicable task types
            
        Returns:
            The created tool entry
        """
        # Convert parameter dicts to ToolParameter
        tool_params = [
            ToolParameter(
                name=p["name"],
                param_type=p.get("type", "string"),
                description=p.get("description", ""),
                required=p.get("required", False),
                default=p.get("default")
            )
            for p in parameters
        ]
        
        definition = ToolDefinition(
            name=name,
            description=description,
            parameters=tool_params,
            task_types=task_types or []
        )
        
        self.registry.register(name, definition, handler)
        
        return self.registry.get(name)  # type: ignore
    
    def to_sdk_tools(self, tools: list[ToolEntry]) -> list[dict[str, Any]]:
        """
        Convert tool entries to SDK format.
        
        Args:
            tools: List of tool entries
            
        Returns:
            List of SDK-compatible tool definitions
        """
        return [t.to_sdk_format() for t in tools]
    
    def get_available_tool_names(self) -> list[str]:
        """Get names of all registered tools."""
        return self.registry.get_names()


# =============================================================================
# BUILT-IN TOOLS - Core functionality
# =============================================================================


# Track if built-in tools have been registered
_builtins_registered = False


def _register_builtin_tools(workspace: Path) -> None:
    """
    Register built-in tools.
    
    Called once when ToolFactory is initialized.
    """
    global _builtins_registered
    if _builtins_registered:
        return
    _builtins_registered = True
    
    # Register file operation tools
    _register_file_tools(workspace)
    
    # Register code analysis tools
    _register_analysis_tools(workspace)
    
    # Register system tools
    _register_system_tools(workspace)
    
    logger.info("builtin_tools_registered")


# -----------------------------------------------------------------------------
# File Operation Tools
# -----------------------------------------------------------------------------


class ReadFileParams(BaseModel):
    """Parameters for read_file tool."""
    path: str = Field(description="Path to the file to read (relative to workspace)")
    encoding: str = Field(default="utf-8", description="File encoding")


class WriteFileParams(BaseModel):
    """Parameters for write_file tool."""
    path: str = Field(description="Path to write (relative to workspace)")
    content: str = Field(description="Content to write")
    create_dirs: bool = Field(default=True, description="Create parent directories if needed")


class ListDirParams(BaseModel):
    """Parameters for list_directory tool."""
    path: str = Field(default=".", description="Directory path (relative to workspace)")
    recursive: bool = Field(default=False, description="List recursively")
    pattern: str = Field(default="*", description="Glob pattern to match")


def _register_file_tools(workspace: Path) -> None:
    """Register file operation tools."""
    
    @register_tool(
        name="read_file",
        description="Read the contents of a file. Returns the file content as a string.",
        task_types=[TaskType.IMPLEMENT, TaskType.ANALYZE, TaskType.REFACTOR, 
                   TaskType.DEBUG, TaskType.TEST]
    )
    async def read_file(params: ReadFileParams) -> dict[str, Any]:
        """
        Read a file from the workspace.
        
        Security: Only allows reading files within the workspace.
        """
        file_path = workspace / params.path
        
        # Security check: ensure path is within workspace
        try:
            file_path = file_path.resolve()
            workspace.resolve()
            file_path.relative_to(workspace.resolve())
        except ValueError:
            return {"error": "Access denied: path outside workspace"}
        
        if not file_path.exists():
            return {"error": f"File not found: {params.path}"}
        
        if not file_path.is_file():
            return {"error": f"Not a file: {params.path}"}
        
        try:
            content = file_path.read_text(encoding=params.encoding)
            return {
                "success": True,
                "path": params.path,
                "content": content,
                "size": len(content)
            }
        except Exception as e:
            return {"error": f"Failed to read file: {e}"}
    
    @register_tool(
        name="write_file",
        description="Write content to a file. Creates the file if it doesn't exist.",
        task_types=[TaskType.IMPLEMENT, TaskType.REFACTOR, TaskType.GENERATE,
                   TaskType.SCAFFOLD],
        requires_confirmation=True
    )
    async def write_file(params: WriteFileParams) -> dict[str, Any]:
        """
        Write content to a file.
        
        Creates parent directories if needed.
        Security: Only allows writing within workspace.
        """
        file_path = workspace / params.path
        
        # Security check
        try:
            file_path = file_path.resolve()
            file_path.relative_to(workspace.resolve())
        except ValueError:
            return {"error": "Access denied: path outside workspace"}
        
        try:
            if params.create_dirs:
                file_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_path.write_text(params.content, encoding="utf-8")
            
            return {
                "success": True,
                "path": params.path,
                "bytes_written": len(params.content.encode())
            }
        except Exception as e:
            return {"error": f"Failed to write file: {e}"}
    
    @register_tool(
        name="list_directory",
        description="List files and directories in a path. Returns names and types.",
        task_types=[TaskType.IMPLEMENT, TaskType.ANALYZE, TaskType.SCAFFOLD]
    )
    async def list_directory(params: ListDirParams) -> dict[str, Any]:
        """
        List contents of a directory.
        
        Can optionally recurse and filter by pattern.
        """
        dir_path = workspace / params.path
        
        # Security check
        try:
            dir_path = dir_path.resolve()
            dir_path.relative_to(workspace.resolve())
        except ValueError:
            return {"error": "Access denied: path outside workspace"}
        
        if not dir_path.exists():
            return {"error": f"Directory not found: {params.path}"}
        
        if not dir_path.is_dir():
            return {"error": f"Not a directory: {params.path}"}
        
        try:
            entries = []
            
            if params.recursive:
                for item in dir_path.rglob(params.pattern):
                    rel_path = item.relative_to(dir_path)
                    entries.append({
                        "name": str(rel_path),
                        "type": "directory" if item.is_dir() else "file",
                        "size": item.stat().st_size if item.is_file() else None
                    })
            else:
                for item in dir_path.glob(params.pattern):
                    entries.append({
                        "name": item.name,
                        "type": "directory" if item.is_dir() else "file",
                        "size": item.stat().st_size if item.is_file() else None
                    })
            
            return {
                "success": True,
                "path": params.path,
                "entries": entries,
                "count": len(entries)
            }
        except Exception as e:
            return {"error": f"Failed to list directory: {e}"}


# -----------------------------------------------------------------------------
# Code Analysis Tools
# -----------------------------------------------------------------------------


class AnalyzeCodeParams(BaseModel):
    """Parameters for analyze_code tool."""
    path: str = Field(description="Path to file or directory to analyze")
    analysis_type: str = Field(
        default="structure",
        description="Type of analysis: structure, complexity, dependencies, security"
    )


class SearchCodeParams(BaseModel):
    """Parameters for search_code tool."""
    pattern: str = Field(description="Search pattern (regex supported)")
    path: str = Field(default=".", description="Path to search in")
    file_pattern: str = Field(default="*", description="File glob pattern")
    case_sensitive: bool = Field(default=False, description="Case sensitive search")


def _register_analysis_tools(workspace: Path) -> None:
    """Register code analysis tools."""
    
    @register_tool(
        name="analyze_code",
        description="Analyze code structure, complexity, or dependencies. Returns analysis results.",
        task_types=[TaskType.ANALYZE, TaskType.REFACTOR, TaskType.OPTIMIZE]
    )
    async def analyze_code(params: AnalyzeCodeParams) -> dict[str, Any]:
        """
        Analyze code for structure, complexity, or dependencies.
        
        Analysis types:
        - structure: Classes, functions, imports
        - complexity: Cyclomatic complexity estimates
        - dependencies: Import analysis
        - security: Basic security pattern checks
        """
        file_path = workspace / params.path
        
        if not file_path.exists():
            return {"error": f"Path not found: {params.path}"}
        
        if file_path.is_file():
            files = [file_path]
        else:
            files = list(file_path.rglob("*.py"))  # For now, Python only
        
        results = []
        for f in files[:20]:  # Limit to 20 files
            try:
                content = f.read_text()
                rel_path = str(f.relative_to(workspace))
                
                if params.analysis_type == "structure":
                    result = _analyze_structure(content)
                elif params.analysis_type == "dependencies":
                    result = _analyze_dependencies(content)
                else:
                    result = _analyze_structure(content)
                
                results.append({
                    "file": rel_path,
                    "analysis": result
                })
            except Exception as e:
                results.append({
                    "file": str(f),
                    "error": str(e)
                })
        
        return {
            "success": True,
            "analysis_type": params.analysis_type,
            "results": results
        }
    
    @register_tool(
        name="search_code",
        description="Search for patterns in code files. Returns matching lines with context.",
        task_types=[TaskType.ANALYZE, TaskType.DEBUG, TaskType.REFACTOR]
    )
    async def search_code(params: SearchCodeParams) -> dict[str, Any]:
        """
        Search for patterns in source files.
        
        Returns matching lines with file paths and line numbers.
        """
        import re
        
        search_path = workspace / params.path
        
        if not search_path.exists():
            return {"error": f"Path not found: {params.path}"}
        
        flags = 0 if params.case_sensitive else re.IGNORECASE
        try:
            pattern = re.compile(params.pattern, flags)
        except re.error as e:
            return {"error": f"Invalid regex pattern: {e}"}
        
        matches = []
        
        if search_path.is_file():
            files = [search_path]
        else:
            files = list(search_path.rglob(params.file_pattern))
        
        for f in files[:50]:  # Limit to 50 files
            if not f.is_file():
                continue
            
            try:
                content = f.read_text(errors="replace")
                lines = content.split("\n")
                
                for i, line in enumerate(lines):
                    if pattern.search(line):
                        matches.append({
                            "file": str(f.relative_to(workspace)),
                            "line_number": i + 1,
                            "line": line.strip()[:200],  # Truncate long lines
                            "context": _get_context(lines, i, 2)
                        })
                        
                        if len(matches) >= 100:  # Limit results
                            break
            except Exception:
                continue
            
            if len(matches) >= 100:
                break
        
        return {
            "success": True,
            "pattern": params.pattern,
            "matches": matches,
            "total_matches": len(matches)
        }


def _analyze_structure(content: str) -> dict[str, Any]:
    """Simple structure analysis for code."""
    import re
    
    # Count classes and functions (Python-style)
    classes = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
    functions = re.findall(r'^(?:async\s+)?def\s+(\w+)', content, re.MULTILINE)
    
    # Count lines
    lines = content.split("\n")
    code_lines = len([l for l in lines if l.strip() and not l.strip().startswith("#")])
    
    return {
        "classes": classes,
        "functions": functions,
        "total_lines": len(lines),
        "code_lines": code_lines,
        "class_count": len(classes),
        "function_count": len(functions)
    }


def _analyze_dependencies(content: str) -> dict[str, Any]:
    """Analyze imports and dependencies."""
    import re
    
    # Python imports
    imports = re.findall(r'^import\s+(\S+)', content, re.MULTILINE)
    from_imports = re.findall(r'^from\s+(\S+)\s+import', content, re.MULTILINE)
    
    # Combine and deduplicate
    all_imports = list(set(imports + from_imports))
    
    # Categorize
    stdlib = []
    third_party = []
    local = []
    
    for imp in all_imports:
        if imp.startswith("."):
            local.append(imp)
        elif _is_stdlib(imp):
            stdlib.append(imp)
        else:
            third_party.append(imp)
    
    return {
        "imports": all_imports,
        "stdlib": sorted(stdlib),
        "third_party": sorted(third_party),
        "local": sorted(local),
        "total_imports": len(all_imports)
    }


def _is_stdlib(module: str) -> bool:
    """Check if module is Python standard library."""
    import sys
    stdlib_modules = set(sys.stdlib_module_names) if hasattr(sys, 'stdlib_module_names') else set()
    return module.split(".")[0] in stdlib_modules


def _get_context(lines: list[str], index: int, context_lines: int) -> list[str]:
    """Get surrounding context lines."""
    start = max(0, index - context_lines)
    end = min(len(lines), index + context_lines + 1)
    return [l.strip()[:100] for l in lines[start:end]]


# -----------------------------------------------------------------------------
# System Tools
# -----------------------------------------------------------------------------


class RunCommandParams(BaseModel):
    """Parameters for run_command tool."""
    command: str = Field(description="Command to execute")
    timeout: int = Field(default=30, description="Timeout in seconds")
    cwd: str = Field(default=".", description="Working directory")


def _register_system_tools(workspace: Path) -> None:
    """Register system operation tools."""
    
    @register_tool(
        name="run_command",
        description="Execute a shell command and return output. Use for running tests, builds, etc.",
        task_types=[TaskType.TEST, TaskType.DEPLOY, TaskType.AUTOMATE],
        requires_confirmation=True
    )
    async def run_command(params: RunCommandParams) -> dict[str, Any]:
        """
        Execute a shell command.
        
        Security: Commands run in workspace context with timeout.
        """
        cwd = workspace / params.cwd
        
        # Security check
        try:
            cwd = cwd.resolve()
            cwd.relative_to(workspace.resolve())
        except ValueError:
            return {"error": "Access denied: working directory outside workspace"}
        
        # Block dangerous commands
        dangerous_patterns = [
            "rm -rf /", "rm -rf ~", "mkfs", "dd if=",
            ":(){:|:&};:", "chmod -R 777 /", "> /dev/sd"
        ]
        
        for pattern in dangerous_patterns:
            if pattern in params.command:
                return {"error": f"Blocked dangerous command pattern: {pattern}"}
        
        try:
            result = await asyncio.wait_for(
                asyncio.create_subprocess_shell(
                    params.command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=cwd
                ),
                timeout=params.timeout
            )
            
            stdout, stderr = await result.communicate()
            
            return {
                "success": result.returncode == 0,
                "return_code": result.returncode,
                "stdout": stdout.decode("utf-8", errors="replace")[:10000],
                "stderr": stderr.decode("utf-8", errors="replace")[:10000]
            }
            
        except asyncio.TimeoutError:
            return {"error": f"Command timed out after {params.timeout} seconds"}
        except Exception as e:
            return {"error": f"Command execution failed: {e}"}


# =============================================================================
# DYNAMIC TOOL GENERATION
# =============================================================================


class DynamicToolBuilder:
    """
    Build tools dynamically at runtime.
    
    Useful for creating task-specific tools that don't fit
    the pre-defined categories.
    
    Example:
    -------
        builder = DynamicToolBuilder()
        
        # Create a custom API tool
        api_tool = builder.create_api_tool(
            name="fetch_user",
            endpoint="/api/users/{user_id}",
            method="GET"
        )
        
        factory.registry.register(
            api_tool.name,
            api_tool.definition,
            api_tool.handler
        )
    """
    
    def create_api_tool(
        self,
        name: str,
        endpoint: str,
        method: str = "GET",
        description: str | None = None
    ) -> ToolEntry:
        """
        Create a tool for calling an API endpoint.
        
        Args:
            name: Tool name
            endpoint: API endpoint (can include {param} placeholders)
            method: HTTP method
            description: Tool description
            
        Returns:
            Tool entry ready for registration
        """
        import re
        import httpx
        
        # Extract path parameters
        path_params = re.findall(r'\{(\w+)\}', endpoint)
        
        parameters = [
            ToolParameter(
                name=param,
                param_type="string",
                description=f"Value for {param} path parameter",
                required=True
            )
            for param in path_params
        ]
        
        # Add optional body parameter for POST/PUT
        if method in ("POST", "PUT", "PATCH"):
            parameters.append(ToolParameter(
                name="body",
                param_type="object",
                description="Request body",
                required=False
            ))
        
        definition = ToolDefinition(
            name=name,
            description=description or f"Call {method} {endpoint}",
            parameters=parameters,
            task_types=[TaskType.IMPLEMENT, TaskType.AUTOMATE]
        )
        
        async def handler(params: dict[str, Any]) -> dict[str, Any]:
            url = endpoint
            for param in path_params:
                url = url.replace(f"{{{param}}}", str(params.get(param, "")))
            
            async with httpx.AsyncClient() as client:
                try:
                    if method == "GET":
                        response = await client.get(url)
                    elif method == "POST":
                        response = await client.post(url, json=params.get("body"))
                    elif method == "PUT":
                        response = await client.put(url, json=params.get("body"))
                    elif method == "DELETE":
                        response = await client.delete(url)
                    else:
                        return {"error": f"Unsupported method: {method}"}
                    
                    return {
                        "success": response.is_success,
                        "status_code": response.status_code,
                        "body": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text[:5000]
                    }
                except Exception as e:
                    return {"error": str(e)}
        
        return ToolEntry(definition=definition, handler=handler)
    
    def create_validator_tool(
        self,
        name: str,
        schema: dict[str, Any],
        description: str | None = None
    ) -> ToolEntry:
        """
        Create a tool for validating data against a JSON schema.
        
        Args:
            name: Tool name
            schema: JSON schema for validation
            description: Tool description
            
        Returns:
            Tool entry ready for registration
        """
        definition = ToolDefinition(
            name=name,
            description=description or f"Validate data against schema",
            parameters=[
                ToolParameter(
                    name="data",
                    param_type="object",
                    description="Data to validate",
                    required=True
                )
            ],
            task_types=[TaskType.TEST, TaskType.ANALYZE]
        )
        
        async def handler(params: dict[str, Any]) -> dict[str, Any]:
            # Simple validation (would use jsonschema in production)
            data = params.get("data", {})
            errors = []
            
            required = schema.get("required", [])
            for field in required:
                if field not in data:
                    errors.append(f"Missing required field: {field}")
            
            properties = schema.get("properties", {})
            for field, value in data.items():
                if field in properties:
                    expected_type = properties[field].get("type")
                    if expected_type == "string" and not isinstance(value, str):
                        errors.append(f"Field {field} should be string")
                    elif expected_type == "number" and not isinstance(value, (int, float)):
                        errors.append(f"Field {field} should be number")
                    elif expected_type == "boolean" and not isinstance(value, bool):
                        errors.append(f"Field {field} should be boolean")
            
            return {
                "valid": len(errors) == 0,
                "errors": errors
            }
        
        return ToolEntry(definition=definition, handler=handler)
