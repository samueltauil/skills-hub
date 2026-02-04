# Tool Patterns Reference

> **Version:** 1.0.0  
> **Purpose:** Reusable patterns for defining and implementing tools

This document provides templates and patterns for creating tools that work with the Copilot Orchestrator.

---

## Table of Contents

1. [Tool Anatomy](#tool-anatomy)
2. [Common Patterns](#common-patterns)
3. [Parameter Design](#parameter-design)
4. [Error Handling](#error-handling)
5. [Security Considerations](#security-considerations)
6. [Testing Tools](#testing-tools)

---

## Tool Anatomy

Every tool consists of three parts:

```
┌─────────────────────────────────────────────────────────────────┐
│                         TOOL                                    │
├─────────────────────┬─────────────────┬─────────────────────────┤
│    DEFINITION       │    HANDLER      │      SCHEMA             │
│                     │                 │                         │
│ • name              │ • async func    │ • JSON Schema           │
│ • description       │ • validation    │ • Parameters            │
│ • task_types        │ • execution     │ • Return type           │
│ • requires_confirm  │ • result        │ • Examples              │
└─────────────────────┴─────────────────┴─────────────────────────┘
```

### Basic Structure

```python
from pydantic import BaseModel, Field
from models import TaskType, ToolParameter, ToolDefinition

# 1. Parameter Model (Schema)
class MyToolParams(BaseModel):
    """Parameters for my_tool."""
    required_param: str = Field(description="A required string parameter")
    optional_param: int = Field(default=10, description="Optional with default")

# 2. Handler Function
async def my_tool_handler(params: dict[str, Any]) -> dict[str, Any]:
    """
    Execute the tool logic.
    
    Args:
        params: Validated parameters from the LLM
        
    Returns:
        Result dictionary with at least 'success' key
    """
    # Implementation
    result = do_something(params["required_param"])
    return {"success": True, "result": result}

# 3. Registration
@register_tool(
    name="my_tool",
    description="Does something useful with the required parameter",
    task_types=[TaskType.IMPLEMENT, TaskType.AUTOMATE]
)
async def my_tool(params: MyToolParams) -> dict[str, Any]:
    return await my_tool_handler(params.model_dump())
```

---

## Common Patterns

### Pattern 1: File Operation Tool

For tools that read or write files:

```python
class FileOperationParams(BaseModel):
    """Standard file operation parameters."""
    path: str = Field(description="File path relative to workspace")
    encoding: str = Field(default="utf-8", description="File encoding")


async def file_operation_base(
    workspace: Path,
    params: dict[str, Any],
    operation: Callable[[Path], Any]
) -> dict[str, Any]:
    """
    Base handler for file operations with security checks.
    
    Pattern:
    1. Resolve path against workspace
    2. Security check (stay within workspace)
    3. Check existence
    4. Execute operation
    5. Return structured result
    """
    file_path = workspace / params["path"]
    
    # Security: Ensure path is within workspace
    try:
        resolved = file_path.resolve()
        resolved.relative_to(workspace.resolve())
    except ValueError:
        return {
            "success": False,
            "error": "Access denied: path outside workspace"
        }
    
    # Execute operation
    try:
        result = operation(resolved)
        return {"success": True, "result": result}
    except FileNotFoundError:
        return {"success": False, "error": f"File not found: {params['path']}"}
    except PermissionError:
        return {"success": False, "error": f"Permission denied: {params['path']}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### Pattern 2: Search/Query Tool

For tools that search and return multiple results:

```python
class SearchParams(BaseModel):
    """Standard search parameters."""
    query: str = Field(description="Search query or pattern")
    path: str = Field(default=".", description="Search scope")
    max_results: int = Field(default=50, description="Maximum results to return")
    case_sensitive: bool = Field(default=False, description="Case sensitivity")


async def search_base(
    workspace: Path,
    params: dict[str, Any],
    search_func: Callable[[Path, str], Iterator[Any]]
) -> dict[str, Any]:
    """
    Base handler for search operations.
    
    Pattern:
    1. Validate search scope
    2. Execute search with limits
    3. Format results
    4. Include metadata (count, truncated)
    """
    search_path = workspace / params["path"]
    
    if not search_path.exists():
        return {"success": False, "error": f"Path not found: {params['path']}"}
    
    results = []
    truncated = False
    
    for item in search_func(search_path, params["query"]):
        results.append(item)
        if len(results) >= params["max_results"]:
            truncated = True
            break
    
    return {
        "success": True,
        "results": results,
        "count": len(results),
        "truncated": truncated
    }
```

### Pattern 3: Command Execution Tool

For tools that run external commands:

```python
class CommandParams(BaseModel):
    """Standard command parameters."""
    command: str = Field(description="Command to execute")
    cwd: str = Field(default=".", description="Working directory")
    timeout: int = Field(default=30, description="Timeout in seconds")
    env: dict[str, str] = Field(default_factory=dict, description="Environment variables")


# Dangerous patterns to block
BLOCKED_PATTERNS = [
    r"rm\s+-rf\s+/",         # rm -rf /
    r"rm\s+-rf\s+~",         # rm -rf ~
    r">\s*/dev/sd",          # Write to disk devices
    r"mkfs\.",               # Format filesystem
    r"dd\s+if=",             # Raw disk operations
    r":\(\)\{:\|:&\};:",     # Fork bomb
]


async def execute_command_safe(
    workspace: Path,
    params: dict[str, Any]
) -> dict[str, Any]:
    """
    Safe command execution with security checks.
    
    Pattern:
    1. Validate working directory
    2. Check against blocked patterns
    3. Execute with timeout
    4. Capture stdout/stderr
    5. Return structured result
    """
    import re
    import asyncio
    
    # Security: Check blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, params["command"]):
            return {
                "success": False,
                "error": f"Blocked: command matches dangerous pattern"
            }
    
    # Validate working directory
    cwd = workspace / params["cwd"]
    try:
        cwd = cwd.resolve()
        cwd.relative_to(workspace.resolve())
    except ValueError:
        return {
            "success": False,
            "error": "Working directory must be within workspace"
        }
    
    # Execute
    try:
        proc = await asyncio.wait_for(
            asyncio.create_subprocess_shell(
                params["command"],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
                env={**os.environ, **params.get("env", {})}
            ),
            timeout=params["timeout"]
        )
        
        stdout, stderr = await proc.communicate()
        
        return {
            "success": proc.returncode == 0,
            "return_code": proc.returncode,
            "stdout": stdout.decode("utf-8", errors="replace")[:10000],
            "stderr": stderr.decode("utf-8", errors="replace")[:5000]
        }
        
    except asyncio.TimeoutError:
        return {
            "success": False,
            "error": f"Command timed out after {params['timeout']}s"
        }
```

### Pattern 4: API Integration Tool

For tools that call external APIs:

```python
class APIParams(BaseModel):
    """Standard API call parameters."""
    endpoint: str = Field(description="API endpoint URL")
    method: str = Field(default="GET", description="HTTP method")
    headers: dict[str, str] = Field(default_factory=dict)
    body: dict[str, Any] | None = Field(default=None)
    timeout: int = Field(default=30)


async def api_call_base(params: dict[str, Any]) -> dict[str, Any]:
    """
    Base handler for API calls.
    
    Pattern:
    1. Validate endpoint (allowlist or pattern)
    2. Build request
    3. Execute with timeout
    4. Parse response
    5. Handle errors gracefully
    """
    import httpx
    
    async with httpx.AsyncClient(timeout=params["timeout"]) as client:
        try:
            response = await client.request(
                method=params["method"],
                url=params["endpoint"],
                headers=params.get("headers", {}),
                json=params.get("body")
            )
            
            # Parse response body
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                body = response.json()
            else:
                body = response.text[:10000]
            
            return {
                "success": response.is_success,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": body
            }
            
        except httpx.TimeoutException:
            return {"success": False, "error": "Request timed out"}
        except httpx.RequestError as e:
            return {"success": False, "error": str(e)}
```

### Pattern 5: Analysis Tool

For tools that analyze code or data:

```python
class AnalysisParams(BaseModel):
    """Standard analysis parameters."""
    target: str = Field(description="Path to analyze")
    depth: int = Field(default=3, description="Analysis depth")
    include_patterns: list[str] = Field(default_factory=list)
    exclude_patterns: list[str] = Field(default_factory=list)


async def analysis_base(
    workspace: Path,
    params: dict[str, Any],
    analyzer: Callable[[Path], dict[str, Any]]
) -> dict[str, Any]:
    """
    Base handler for analysis operations.
    
    Pattern:
    1. Resolve target
    2. Apply include/exclude filters
    3. Run analysis with depth limit
    4. Aggregate results
    5. Include summary statistics
    """
    target = workspace / params["target"]
    
    if not target.exists():
        return {"success": False, "error": f"Target not found: {params['target']}"}
    
    # Get files to analyze
    files = []
    if target.is_file():
        files = [target]
    else:
        for pattern in params.get("include_patterns", ["**/*"]):
            files.extend(target.glob(pattern))
        
        # Apply excludes
        exclude_patterns = params.get("exclude_patterns", [])
        files = [f for f in files if not any(
            f.match(ex) for ex in exclude_patterns
        )]
    
    # Analyze
    results = []
    for f in files[:100]:  # Limit file count
        if f.is_file():
            results.append(analyzer(f))
    
    return {
        "success": True,
        "target": params["target"],
        "files_analyzed": len(results),
        "results": results,
        "summary": _summarize_analysis(results)
    }
```

---

## Parameter Design

### Guidelines

1. **Use clear names**: `file_path` not `fp`
2. **Provide defaults**: Make tools usable with minimal input
3. **Add descriptions**: Help the LLM understand usage
4. **Validate early**: Use Pydantic constraints

### Common Parameter Types

```python
from pydantic import Field, constr, conint

class WellDesignedParams(BaseModel):
    # String with constraints
    name: constr(min_length=1, max_length=100) = Field(
        description="A short identifier"
    )
    
    # Path (relative)
    path: str = Field(
        default=".",
        description="Relative path from workspace root"
    )
    
    # Integer with range
    limit: conint(ge=1, le=1000) = Field(
        default=100,
        description="Maximum items to process"
    )
    
    # Boolean flag
    recursive: bool = Field(
        default=False,
        description="Process subdirectories"
    )
    
    # Enum-like choices
    format: str = Field(
        default="json",
        description="Output format: json, yaml, or text"
    )
    
    # Optional complex type
    filters: dict[str, str] | None = Field(
        default=None,
        description="Key-value filters to apply"
    )
```

### JSON Schema Output

The `to_json_schema()` method generates SDK-compatible schemas:

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "File path relative to workspace"
    },
    "content": {
      "type": "string",
      "description": "Content to write"
    },
    "create_dirs": {
      "type": "boolean",
      "description": "Create parent directories if needed",
      "default": true
    }
  },
  "required": ["path", "content"]
}
```

---

## Error Handling

### Return Structure

Always return a consistent structure:

```python
# Success
{"success": True, "result": {...}, "metadata": {...}}

# Failure
{"success": False, "error": "Human-readable error message"}

# Partial success
{"success": True, "result": [...], "warnings": ["Item 3 skipped"]}
```

### Error Categories

```python
class ToolError(Exception):
    """Base class for tool errors."""
    pass

class ValidationError(ToolError):
    """Invalid parameters."""
    pass

class PermissionError(ToolError):
    """Access denied."""
    pass

class NotFoundError(ToolError):
    """Resource not found."""
    pass

class ExecutionError(ToolError):
    """Failed to execute."""
    pass

class TimeoutError(ToolError):
    """Operation timed out."""
    pass
```

### Error Handling Pattern

```python
async def robust_tool_handler(params: dict[str, Any]) -> dict[str, Any]:
    """Handler with comprehensive error handling."""
    try:
        # Validate
        validated = MyParams.model_validate(params)
        
        # Execute
        result = await do_operation(validated)
        
        return {"success": True, "result": result}
        
    except ValidationError as e:
        return {"success": False, "error": f"Invalid parameters: {e}"}
    except PermissionError:
        return {"success": False, "error": "Access denied"}
    except NotFoundError as e:
        return {"success": False, "error": f"Not found: {e}"}
    except TimeoutError:
        return {"success": False, "error": "Operation timed out"}
    except Exception as e:
        # Log unexpected errors
        logger.exception("Unexpected error in tool", error=str(e))
        return {"success": False, "error": f"Unexpected error: {e}"}
```

---

## Security Considerations

### Path Traversal Prevention

```python
def safe_path(workspace: Path, user_path: str) -> Path | None:
    """
    Safely resolve a user-provided path.
    
    Returns None if the path escapes the workspace.
    """
    try:
        # Resolve to absolute
        full_path = (workspace / user_path).resolve()
        
        # Verify it's within workspace
        full_path.relative_to(workspace.resolve())
        
        return full_path
    except ValueError:
        return None
```

### Command Injection Prevention

```python
import shlex

def safe_command(cmd: str, args: list[str]) -> list[str]:
    """
    Build a safe command list.
    
    Uses shlex to properly escape arguments.
    """
    return [cmd] + [shlex.quote(arg) for arg in args]
```

### Secrets Protection

```python
SENSITIVE_PATTERNS = [
    r"password",
    r"secret",
    r"api_key",
    r"token",
    r"credential"
]

def redact_sensitive(text: str) -> str:
    """Redact potentially sensitive values from output."""
    import re
    for pattern in SENSITIVE_PATTERNS:
        text = re.sub(
            rf"({pattern}['\"]?\s*[:=]\s*)['\"]?[^'\"\s]+['\"]?",
            r"\1[REDACTED]",
            text,
            flags=re.IGNORECASE
        )
    return text
```

---

## Testing Tools

### Unit Test Pattern

```python
import pytest
from tool_factory import ToolFactory

@pytest.fixture
def factory(tmp_path):
    """Create factory with temporary workspace."""
    return ToolFactory(workspace=tmp_path)

@pytest.fixture
def sample_files(tmp_path):
    """Create sample files for testing."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('hello')")
    return tmp_path

class TestReadFileTool:
    async def test_read_existing_file(self, factory, sample_files):
        result = await factory.execute_tool(
            "read_file",
            {"path": "src/main.py"}
        )
        assert result["success"]
        assert "print('hello')" in result["content"]
    
    async def test_read_nonexistent_file(self, factory, sample_files):
        result = await factory.execute_tool(
            "read_file",
            {"path": "nonexistent.py"}
        )
        assert not result["success"]
        assert "not found" in result["error"].lower()
    
    async def test_path_traversal_blocked(self, factory, sample_files):
        result = await factory.execute_tool(
            "read_file",
            {"path": "../../../etc/passwd"}
        )
        assert not result["success"]
        assert "access denied" in result["error"].lower()
```

### Integration Test Pattern

```python
class TestToolIntegration:
    async def test_read_modify_write_workflow(self, factory, sample_files):
        # Read
        content = await factory.execute_tool(
            "read_file",
            {"path": "src/main.py"}
        )
        assert content["success"]
        
        # Modify
        new_content = content["content"].replace("hello", "world")
        
        # Write
        write_result = await factory.execute_tool(
            "write_file",
            {"path": "src/main.py", "content": new_content}
        )
        assert write_result["success"]
        
        # Verify
        verify = await factory.execute_tool(
            "read_file",
            {"path": "src/main.py"}
        )
        assert "world" in verify["content"]
```

---

## Tool Quick Reference

| Tool Name | Category | Description | Key Params |
|-----------|----------|-------------|------------|
| `read_file` | File | Read file contents | `path`, `encoding` |
| `write_file` | File | Write content to file | `path`, `content` |
| `list_directory` | File | List directory contents | `path`, `recursive` |
| `search_code` | Analysis | Search for patterns | `pattern`, `path` |
| `analyze_code` | Analysis | Analyze code structure | `target`, `depth` |
| `run_command` | System | Execute shell command | `command`, `timeout` |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024 | Initial patterns |
