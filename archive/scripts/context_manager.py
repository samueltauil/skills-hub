"""
Context Manager for Copilot Orchestrator
=========================================

This module handles the critical task of preparing context for SDK transfer.
Context management is essential because:

1. LLMs have finite context windows (8K - 128K tokens)
2. Relevant context improves response quality
3. Too much context causes confusion and hallucination
4. Token costs scale with context size

Architecture:
------------

    ┌─────────────────────────────────────────────────────────────────┐
    │                    CONTEXT MANAGER PIPELINE                     │
    │                                                                 │
    │  ┌─────────┐   ┌───────────┐   ┌──────────┐   ┌─────────────┐  │
    │  │ GATHER  │──▶│ PRIORITIZE│──▶│ COMPRESS │──▶│ SERIALIZE   │  │
    │  │         │   │           │   │          │   │             │  │
    │  │ • Files │   │ • Score   │   │ • Token  │   │ • Envelope  │  │
    │  │ • Errors│   │ • Sort    │   │   count  │   │ • Checksum  │  │
    │  │ • Deps  │   │ • Filter  │   │ • Trim   │   │ • Metadata  │  │
    │  └─────────┘   └───────────┘   └──────────┘   └─────────────┘  │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘

Key Classes:
-----------
- ContextGatherer: Collects raw context from various sources
- ContextPrioritizer: Ranks chunks by relevance to task
- ContextCompressor: Fits context within token budget
- ContextManager: Orchestrates the full pipeline

Usage:
-----
    manager = ContextManager()
    
    # Gather context from workspace
    raw_context = await manager.gather(
        workspace_path=Path("./src"),
        task_type=TaskType.IMPLEMENT,
        focus_files=["models.py", "routes.py"]
    )
    
    # Compress to fit budget
    compressed = await manager.compress(
        raw_context,
        budget=TokenBudget(input_max=8000)
    )
    
    # Use in task envelope
    envelope = TaskEnvelope(
        original_request="add validation",
        compressed_context=compressed
    )
"""

from __future__ import annotations

import asyncio
import hashlib
import re
from pathlib import Path
from typing import Any, Callable

import structlog
import tiktoken

from models import (
    CompressedContext,
    ContextChunk,
    ContextPriority,
    TaskType,
    TokenBudget,
)

# Configure structured logging
logger = structlog.get_logger(__name__)


# =============================================================================
# TOKEN COUNTING - Accurate budget management
# =============================================================================


class TokenCounter:
    """
    Token counter using tiktoken for accurate counts.
    
    Uses cl100k_base encoding (GPT-4, GPT-4.1 compatible).
    Falls back to character-based estimation if tiktoken fails.
    
    Why accurate counting matters:
    - Undercount: Context gets truncated unexpectedly
    - Overcount: Waste budget, miss important context
    
    Attributes:
        encoding: The tiktoken encoding to use
        _cache: LRU cache of content hashes to token counts
    """
    
    def __init__(self, model: str = "gpt-4.1") -> None:
        """
        Initialize counter with model-appropriate encoding.
        
        Args:
            model: Model name to select encoding
        """
        try:
            # cl100k_base works for GPT-4 family
            self.encoding = tiktoken.get_encoding("cl100k_base")
        except Exception:
            logger.warning("tiktoken unavailable, using estimation")
            self.encoding = None
        
        self._cache: dict[str, int] = {}
    
    def count(self, text: str) -> int:
        """
        Count tokens in text.
        
        Args:
            text: The text to count tokens for
            
        Returns:
            Number of tokens
        """
        if not text:
            return 0
        
        # Check cache first (content hash → token count)
        content_hash = hashlib.md5(text.encode()).hexdigest()[:16]
        if content_hash in self._cache:
            return self._cache[content_hash]
        
        # Count tokens
        if self.encoding:
            count = len(self.encoding.encode(text))
        else:
            # Fallback: ~4 characters per token for English
            count = len(text) // 4
        
        # Cache and return
        self._cache[content_hash] = count
        return count
    
    def count_many(self, texts: list[str]) -> list[int]:
        """Count tokens for multiple texts efficiently."""
        return [self.count(text) for text in texts]
    
    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """
        Truncate text to fit within token limit.
        
        Tries to truncate at sentence boundaries for readability.
        
        Args:
            text: Text to truncate
            max_tokens: Maximum tokens allowed
            
        Returns:
            Truncated text
        """
        if self.count(text) <= max_tokens:
            return text
        
        if self.encoding:
            tokens = self.encoding.encode(text)
            truncated_tokens = tokens[:max_tokens]
            return self.encoding.decode(truncated_tokens)
        else:
            # Fallback: character-based truncation
            max_chars = max_tokens * 4
            return text[:max_chars]


# Global token counter instance
_token_counter = TokenCounter()


def count_tokens(text: str) -> int:
    """Convenience function for token counting."""
    return _token_counter.count(text)


# =============================================================================
# CONTEXT GATHERING - Collect raw context from sources
# =============================================================================


class ContextGatherer:
    """
    Collects raw context from various sources.
    
    Sources include:
    - Workspace files (source code, configs)
    - Error messages and stack traces
    - Project structure (directory tree)
    - Dependencies (package.json, requirements.txt)
    - Git history (recent changes)
    
    The gatherer doesn't make decisions about what to include -
    it just collects everything that might be relevant.
    The ContextPrioritizer decides what actually goes in.
    
    Attributes:
        workspace: Root path of the workspace
        max_file_size: Skip files larger than this (bytes)
        ignore_patterns: Glob patterns to skip
    """
    
    # File extensions to include by default
    CODE_EXTENSIONS = {
        ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java",
        ".c", ".cpp", ".h", ".hpp", ".cs", ".rb", ".php", ".swift",
        ".kt", ".scala", ".sh", ".bash", ".ps1", ".sql"
    }
    
    CONFIG_EXTENSIONS = {
        ".json", ".yaml", ".yml", ".toml", ".xml", ".ini", ".env",
        ".config", ".cfg"
    }
    
    DOC_EXTENSIONS = {".md", ".txt", ".rst", ".adoc"}
    
    # Directories to always ignore
    IGNORE_DIRS = {
        "node_modules", ".git", "__pycache__", ".venv", "venv",
        "dist", "build", ".next", ".nuxt", "target", "bin", "obj",
        ".pytest_cache", ".mypy_cache", ".ruff_cache", "coverage"
    }
    
    def __init__(
        self,
        workspace: Path,
        max_file_size: int = 100_000,  # 100KB
        ignore_patterns: list[str] | None = None
    ) -> None:
        """
        Initialize the context gatherer.
        
        Args:
            workspace: Root directory to search
            max_file_size: Maximum file size to read (bytes)
            ignore_patterns: Additional glob patterns to ignore
        """
        self.workspace = workspace
        self.max_file_size = max_file_size
        self.ignore_patterns = ignore_patterns or []
        
        logger.info(
            "context_gatherer_initialized",
            workspace=str(workspace),
            max_file_size=max_file_size
        )
    
    async def gather_all(
        self,
        focus_files: list[str] | None = None,
        include_structure: bool = True,
        include_deps: bool = True
    ) -> list[ContextChunk]:
        """
        Gather all available context.
        
        Args:
            focus_files: Specific files to prioritize
            include_structure: Include directory tree
            include_deps: Include dependency information
            
        Returns:
            List of context chunks (unprioritized)
        """
        chunks: list[ContextChunk] = []
        
        # Gather in parallel for efficiency
        tasks = [
            self._gather_files(focus_files),
        ]
        
        if include_structure:
            tasks.append(self._gather_structure())
        
        if include_deps:
            tasks.append(self._gather_dependencies())
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                logger.error("gather_error", error=str(result))
            elif isinstance(result, list):
                chunks.extend(result)
        
        logger.info("context_gathered", chunk_count=len(chunks))
        return chunks
    
    async def _gather_files(
        self,
        focus_files: list[str] | None = None
    ) -> list[ContextChunk]:
        """
        Gather context from source files.
        
        Reads files and creates chunks with appropriate metadata.
        Focus files get CRITICAL priority, others get MEDIUM.
        """
        chunks: list[ContextChunk] = []
        focus_set = set(focus_files or [])
        
        # Find all relevant files
        all_extensions = (
            self.CODE_EXTENSIONS | 
            self.CONFIG_EXTENSIONS | 
            self.DOC_EXTENSIONS
        )
        
        for file_path in self._walk_files(all_extensions):
            try:
                content = await self._read_file(file_path)
                if content is None:
                    continue
                
                # Determine priority
                relative_path = str(file_path.relative_to(self.workspace))
                is_focus = any(
                    relative_path.endswith(f) or f in relative_path
                    for f in focus_set
                )
                
                priority = (
                    ContextPriority.CRITICAL if is_focus
                    else ContextPriority.MEDIUM
                )
                
                # Determine chunk type
                ext = file_path.suffix.lower()
                if ext in self.CODE_EXTENSIONS:
                    chunk_type = "file"
                elif ext in self.CONFIG_EXTENSIONS:
                    chunk_type = "metadata"
                else:
                    chunk_type = "file"
                
                chunks.append(ContextChunk(
                    content=content,
                    source=relative_path,
                    chunk_type=chunk_type,
                    priority=priority,
                    token_count=count_tokens(content),
                    metadata={
                        "language": self._detect_language(file_path),
                        "size_bytes": len(content.encode()),
                    }
                ))
                
            except Exception as e:
                logger.warning(
                    "file_read_error",
                    file=str(file_path),
                    error=str(e)
                )
        
        return chunks
    
    async def _gather_structure(self) -> list[ContextChunk]:
        """
        Gather project directory structure.
        
        Creates a tree representation that helps the LLM
        understand the project layout.
        """
        tree_lines = []
        
        def build_tree(path: Path, prefix: str = "") -> None:
            """Recursively build directory tree."""
            entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name))
            
            for i, entry in enumerate(entries):
                is_last = i == len(entries) - 1
                connector = "└── " if is_last else "├── "
                
                if entry.is_dir():
                    if entry.name in self.IGNORE_DIRS:
                        continue
                    tree_lines.append(f"{prefix}{connector}{entry.name}/")
                    extension = "    " if is_last else "│   "
                    build_tree(entry, prefix + extension)
                else:
                    tree_lines.append(f"{prefix}{connector}{entry.name}")
        
        try:
            tree_lines.append(f"{self.workspace.name}/")
            build_tree(self.workspace)
            
            content = "\n".join(tree_lines)
            
            return [ContextChunk(
                content=content,
                source="project_structure",
                chunk_type="structure",
                priority=ContextPriority.LOW,
                token_count=count_tokens(content),
                metadata={"entry_count": len(tree_lines)}
            )]
        except Exception as e:
            logger.warning("structure_gather_error", error=str(e))
            return []
    
    async def _gather_dependencies(self) -> list[ContextChunk]:
        """
        Gather dependency information.
        
        Reads package.json, requirements.txt, pyproject.toml, etc.
        to understand project dependencies.
        """
        chunks: list[ContextChunk] = []
        
        dep_files = [
            "package.json",
            "requirements.txt",
            "pyproject.toml",
            "Cargo.toml",
            "go.mod",
            "pom.xml",
            "build.gradle",
        ]
        
        for dep_file in dep_files:
            file_path = self.workspace / dep_file
            if file_path.exists():
                try:
                    content = await self._read_file(file_path)
                    if content:
                        chunks.append(ContextChunk(
                            content=content,
                            source=dep_file,
                            chunk_type="dependency",
                            priority=ContextPriority.MEDIUM,
                            token_count=count_tokens(content),
                            metadata={"type": "dependency_manifest"}
                        ))
                except Exception as e:
                    logger.warning(
                        "dependency_read_error",
                        file=dep_file,
                        error=str(e)
                    )
        
        return chunks
    
    def _walk_files(self, extensions: set[str]) -> list[Path]:
        """
        Walk workspace and yield files matching extensions.
        
        Respects ignore patterns and directory exclusions.
        """
        files: list[Path] = []
        
        for path in self.workspace.rglob("*"):
            # Skip directories
            if path.is_dir():
                continue
            
            # Skip ignored directories
            if any(ignored in path.parts for ignored in self.IGNORE_DIRS):
                continue
            
            # Skip by extension
            if path.suffix.lower() not in extensions:
                continue
            
            # Skip large files
            try:
                if path.stat().st_size > self.max_file_size:
                    continue
            except OSError:
                continue
            
            files.append(path)
        
        return files
    
    async def _read_file(self, path: Path) -> str | None:
        """
        Read file content asynchronously.
        
        Returns None if file can't be read or is binary.
        """
        try:
            # Read in executor to not block event loop
            loop = asyncio.get_event_loop()
            content = await loop.run_in_executor(
                None,
                lambda: path.read_text(encoding="utf-8", errors="replace")
            )
            return content
        except Exception:
            return None
    
    def _detect_language(self, path: Path) -> str:
        """Detect programming language from file extension."""
        ext_to_lang = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".jsx": "jsx",
            ".tsx": "tsx",
            ".go": "go",
            ".rs": "rust",
            ".java": "java",
            ".c": "c",
            ".cpp": "cpp",
            ".h": "c",
            ".hpp": "cpp",
            ".cs": "csharp",
            ".rb": "ruby",
            ".php": "php",
            ".swift": "swift",
            ".kt": "kotlin",
            ".scala": "scala",
            ".sh": "bash",
            ".bash": "bash",
            ".ps1": "powershell",
            ".sql": "sql",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".toml": "toml",
            ".xml": "xml",
            ".md": "markdown",
        }
        return ext_to_lang.get(path.suffix.lower(), "text")


# =============================================================================
# CONTEXT PRIORITIZATION - Rank chunks by relevance
# =============================================================================


class ContextPrioritizer:
    """
    Ranks context chunks by relevance to the task.
    
    Prioritization Strategy:
    -----------------------
    1. Start with base priority from ContextPriority enum
    2. Apply task-specific boosters
    3. Apply recency boosters (recent files rank higher)
    4. Apply keyword matching boosters
    5. Sort by final score
    
    This ensures the most relevant context gets included when
    budget is limited.
    
    Scoring System:
    --------------
    - CRITICAL priority: 1000 base
    - HIGH priority: 800 base
    - MEDIUM priority: 500 base
    - LOW priority: 200 base
    - MINIMAL priority: 50 base
    
    Boosters can add 10-200 points based on relevance signals.
    """
    
    # Base scores by priority level
    PRIORITY_SCORES = {
        ContextPriority.CRITICAL: 1000,
        ContextPriority.HIGH: 800,
        ContextPriority.MEDIUM: 500,
        ContextPriority.LOW: 200,
        ContextPriority.MINIMAL: 50,
    }
    
    # Task type to relevant file patterns
    TASK_PATTERNS: dict[TaskType, list[str]] = {
        TaskType.IMPLEMENT: ["model", "service", "handler", "controller", "route"],
        TaskType.TEST: ["test", "spec", "mock", "fixture"],
        TaskType.DEBUG: ["error", "exception", "log"],
        TaskType.DEPLOY: ["docker", "kubernetes", "ci", "cd", "pipeline", "deploy"],
        TaskType.REFACTOR: ["util", "helper", "common", "shared"],
        TaskType.OPTIMIZE: ["performance", "cache", "index", "query"],
    }
    
    def __init__(self, task_type: TaskType, keywords: list[str] | None = None) -> None:
        """
        Initialize prioritizer for a specific task.
        
        Args:
            task_type: The type of task being performed
            keywords: Additional keywords to boost matching chunks
        """
        self.task_type = task_type
        self.keywords = [kw.lower() for kw in (keywords or [])]
        
        logger.debug(
            "prioritizer_initialized",
            task_type=task_type.value,
            keyword_count=len(self.keywords)
        )
    
    def prioritize(self, chunks: list[ContextChunk]) -> list[ContextChunk]:
        """
        Sort chunks by relevance score.
        
        Args:
            chunks: Unprioritized context chunks
            
        Returns:
            Chunks sorted by score (highest first)
        """
        scored_chunks = [
            (chunk, self._score_chunk(chunk))
            for chunk in chunks
        ]
        
        # Sort by score descending
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        
        # Log top chunks for debugging
        top_sources = [c[0].source for c in scored_chunks[:5]]
        logger.debug("prioritization_complete", top_sources=top_sources)
        
        return [chunk for chunk, _ in scored_chunks]
    
    def _score_chunk(self, chunk: ContextChunk) -> int:
        """
        Calculate relevance score for a chunk.
        
        Combines base priority with various boosters.
        """
        score = self.PRIORITY_SCORES.get(chunk.priority, 500)
        
        # Boost for task-relevant patterns
        patterns = self.TASK_PATTERNS.get(self.task_type, [])
        source_lower = chunk.source.lower()
        for pattern in patterns:
            if pattern in source_lower:
                score += 100
                break
        
        # Boost for keyword matches
        content_lower = chunk.content.lower()
        for keyword in self.keywords:
            if keyword in source_lower:
                score += 150  # Strong boost for filename match
            elif keyword in content_lower:
                score += 50   # Moderate boost for content match
        
        # Boost for error/exception content in debug tasks
        if self.task_type == TaskType.DEBUG:
            if "error" in content_lower or "exception" in content_lower:
                score += 200
        
        # Boost for test files in test tasks
        if self.task_type == TaskType.TEST:
            if "test" in source_lower or "spec" in source_lower:
                score += 150
        
        return score


# =============================================================================
# CONTEXT COMPRESSION - Fit within token budget
# =============================================================================


class ContextCompressor:
    """
    Compresses context to fit within token budget.
    
    Compression Strategies:
    ----------------------
    1. Priority-based inclusion: Include highest-scored chunks first
    2. Truncation: Cut long files to most relevant sections
    3. Summarization: Replace large chunks with summaries (future)
    4. Deduplication: Remove redundant content
    
    The compressor aims to maximize information density within
    the given token budget.
    
    Attributes:
        token_counter: Token counting utility
    """
    
    def __init__(self) -> None:
        """Initialize the compressor."""
        self.token_counter = TokenCounter()
    
    def compress(
        self,
        chunks: list[ContextChunk],
        budget: TokenBudget
    ) -> CompressedContext:
        """
        Compress chunks to fit within budget.
        
        Algorithm:
        1. Calculate total tokens needed
        2. If under budget, include all
        3. If over budget:
           a. Include chunks in priority order
           b. Truncate large chunks if needed
           c. Track what was excluded
        
        Args:
            chunks: Prioritized context chunks
            budget: Token budget constraints
            
        Returns:
            Compressed context with included chunks
        """
        included: list[ContextChunk] = []
        excluded_sources: list[str] = []
        total_tokens = 0
        available = budget.input_available
        
        for chunk in chunks:
            tokens_needed = chunk.token_count
            
            if total_tokens + tokens_needed <= available:
                # Fits completely
                included.append(chunk)
                total_tokens += tokens_needed
            
            elif total_tokens < available:
                # Partial fit - truncate
                remaining = available - total_tokens
                truncated = self._truncate_chunk(chunk, remaining)
                if truncated:
                    included.append(truncated)
                    total_tokens += truncated.token_count
                excluded_sources.append(f"{chunk.source} (truncated)")
            
            else:
                # Doesn't fit
                excluded_sources.append(chunk.source)
        
        # Calculate compression ratio
        original_tokens = sum(c.token_count for c in chunks)
        ratio = original_tokens / total_tokens if total_tokens > 0 else 1.0
        
        logger.info(
            "compression_complete",
            original_tokens=original_tokens,
            compressed_tokens=total_tokens,
            ratio=round(ratio, 2),
            included_count=len(included),
            excluded_count=len(excluded_sources)
        )
        
        return CompressedContext(
            chunks=included,
            total_tokens=total_tokens,
            compression_ratio=ratio,
            excluded_sources=excluded_sources,
            summary=self._generate_summary(included) if included else None
        )
    
    def _truncate_chunk(
        self,
        chunk: ContextChunk,
        max_tokens: int
    ) -> ContextChunk | None:
        """
        Truncate a chunk to fit within token limit.
        
        Attempts intelligent truncation:
        - For code: Keep imports and function signatures
        - For errors: Keep stack trace summary
        - For docs: Keep first section
        """
        if max_tokens < 50:
            # Not enough space for meaningful content
            return None
        
        content = chunk.content
        
        # For code files, prioritize keeping structure
        if chunk.chunk_type == "file":
            content = self._smart_truncate_code(content, max_tokens)
        else:
            content = self.token_counter.truncate_to_tokens(content, max_tokens)
        
        return ContextChunk(
            chunk_id=chunk.chunk_id,
            content=content,
            source=chunk.source,
            chunk_type=chunk.chunk_type,
            priority=chunk.priority,
            token_count=self.token_counter.count(content),
            metadata={**chunk.metadata, "truncated": True}
        )
    
    def _smart_truncate_code(self, content: str, max_tokens: int) -> str:
        """
        Intelligently truncate code to preserve structure.
        
        Strategy:
        1. Always keep imports/requires
        2. Keep class/function definitions
        3. Truncate function bodies
        """
        lines = content.split("\n")
        
        # Separate imports and code
        imports: list[str] = []
        code: list[str] = []
        
        for line in lines:
            stripped = line.strip()
            if (stripped.startswith("import ") or 
                stripped.startswith("from ") or
                stripped.startswith("require(") or
                stripped.startswith("const ") and "require" in stripped):
                imports.append(line)
            else:
                code.append(line)
        
        # Budget tokens for imports (~30% of budget)
        import_budget = int(max_tokens * 0.3)
        import_text = "\n".join(imports)
        if self.token_counter.count(import_text) > import_budget:
            import_text = self.token_counter.truncate_to_tokens(import_text, import_budget)
        
        # Remaining budget for code
        code_budget = max_tokens - self.token_counter.count(import_text)
        code_text = "\n".join(code)
        code_text = self.token_counter.truncate_to_tokens(code_text, code_budget)
        
        return f"{import_text}\n\n# ... (truncated) ...\n\n{code_text}"
    
    def _generate_summary(self, chunks: list[ContextChunk]) -> str:
        """Generate a brief summary of included context."""
        sources = [c.source for c in chunks]
        types = set(c.chunk_type for c in chunks)
        
        return (
            f"Context includes {len(chunks)} chunks from: "
            f"{', '.join(sources[:5])}{'...' if len(sources) > 5 else ''}. "
            f"Types: {', '.join(types)}."
        )


# =============================================================================
# CONTEXT MANAGER - Main orchestration class
# =============================================================================


class ContextManager:
    """
    Main interface for context management.
    
    Orchestrates the full pipeline:
    1. Gather raw context
    2. Prioritize by relevance
    3. Compress to fit budget
    4. Package for SDK transfer
    
    Usage:
    -----
        manager = ContextManager(workspace=Path("./project"))
        
        compressed = await manager.prepare_context(
            task_type=TaskType.IMPLEMENT,
            request="add user authentication",
            focus_files=["auth.py"],
            budget=TokenBudget(input_max=8000)
        )
    """
    
    def __init__(
        self,
        workspace: Path | None = None,
        max_file_size: int = 100_000
    ) -> None:
        """
        Initialize context manager.
        
        Args:
            workspace: Root workspace path (defaults to cwd)
            max_file_size: Maximum file size to read
        """
        self.workspace = workspace or Path.cwd()
        self.gatherer = ContextGatherer(
            workspace=self.workspace,
            max_file_size=max_file_size
        )
        self.compressor = ContextCompressor()
        
        logger.info(
            "context_manager_initialized",
            workspace=str(self.workspace)
        )
    
    async def prepare_context(
        self,
        task_type: TaskType,
        request: str,
        focus_files: list[str] | None = None,
        budget: TokenBudget | None = None
    ) -> CompressedContext:
        """
        Prepare compressed context for SDK transfer.
        
        This is the main entry point for context preparation.
        
        Args:
            task_type: Type of task being performed
            request: Original user request (for keyword extraction)
            focus_files: Specific files to prioritize
            budget: Token budget constraints
            
        Returns:
            Compressed context ready for TaskEnvelope
        """
        budget = budget or TokenBudget()
        
        # Extract keywords from request
        keywords = self._extract_keywords(request)
        
        # Step 1: Gather all context
        logger.info("preparing_context", task_type=task_type.value)
        raw_chunks = await self.gatherer.gather_all(
            focus_files=focus_files,
            include_structure=True,
            include_deps=True
        )
        
        # Step 2: Prioritize
        prioritizer = ContextPrioritizer(
            task_type=task_type,
            keywords=keywords
        )
        prioritized = prioritizer.prioritize(raw_chunks)
        
        # Step 3: Compress
        compressed = self.compressor.compress(prioritized, budget)
        
        logger.info(
            "context_prepared",
            total_tokens=compressed.total_tokens,
            chunk_count=len(compressed.chunks)
        )
        
        return compressed
    
    def add_error_context(
        self,
        compressed: CompressedContext,
        error_message: str,
        stack_trace: str | None = None
    ) -> CompressedContext:
        """
        Add error context with CRITICAL priority.
        
        Error messages are always included as they're essential
        for debugging tasks.
        
        Args:
            compressed: Existing compressed context
            error_message: The error message
            stack_trace: Optional stack trace
            
        Returns:
            Updated compressed context
        """
        content = error_message
        if stack_trace:
            content = f"{error_message}\n\nStack trace:\n{stack_trace}"
        
        error_chunk = ContextChunk(
            content=content,
            source="error_context",
            chunk_type="error",
            priority=ContextPriority.CRITICAL,
            token_count=count_tokens(content)
        )
        
        # Prepend error to chunks (highest priority)
        new_chunks = [error_chunk] + compressed.chunks
        new_total = compressed.total_tokens + error_chunk.token_count
        
        return CompressedContext(
            chunks=new_chunks,
            total_tokens=new_total,
            compression_ratio=compressed.compression_ratio,
            excluded_sources=compressed.excluded_sources,
            summary=compressed.summary
        )
    
    def _extract_keywords(self, request: str) -> list[str]:
        """
        Extract relevant keywords from user request.
        
        Used for boosting matching files in prioritization.
        """
        # Remove common words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
            "for", "of", "with", "by", "from", "as", "is", "was", "are",
            "be", "been", "being", "have", "has", "had", "do", "does",
            "did", "will", "would", "could", "should", "may", "might",
            "must", "shall", "can", "need", "this", "that", "these",
            "those", "i", "you", "he", "she", "it", "we", "they", "my",
            "your", "his", "her", "its", "our", "their", "what", "which",
            "who", "whom", "when", "where", "why", "how", "all", "each",
            "every", "both", "few", "more", "most", "some", "any", "no",
            "not", "only", "own", "same", "so", "than", "too", "very",
            "just", "also", "now", "here", "there", "then", "once",
            "please", "add", "create", "make", "implement", "write",
            "update", "change", "modify"
        }
        
        # Extract words (alphanumeric, underscores, hyphens)
        words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9_-]*\b', request.lower())
        
        # Filter and return
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords[:10]  # Limit to top 10


# =============================================================================
# CHECKPOINT / RESTORATION - For session persistence
# =============================================================================


class ContextCheckpoint:
    """
    Checkpoint manager for saving/restoring context state.
    
    Enables:
    - Resuming interrupted tasks
    - Debugging context issues
    - Auditing what context was used
    
    Checkpoints are stored as JSON files in .context_checkpoints/
    """
    
    def __init__(self, checkpoint_dir: Path | None = None) -> None:
        """
        Initialize checkpoint manager.
        
        Args:
            checkpoint_dir: Directory for checkpoint files
        """
        self.checkpoint_dir = checkpoint_dir or Path(".context_checkpoints")
        self.checkpoint_dir.mkdir(exist_ok=True)
    
    async def save(self, task_id: str, context: CompressedContext) -> Path:
        """
        Save context checkpoint.
        
        Args:
            task_id: Task identifier
            context: Compressed context to save
            
        Returns:
            Path to checkpoint file
        """
        checkpoint_path = self.checkpoint_dir / f"{task_id}.json"
        
        # Serialize to JSON
        data = context.model_dump_json(indent=2)
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: checkpoint_path.write_text(data)
        )
        
        logger.info("checkpoint_saved", path=str(checkpoint_path))
        return checkpoint_path
    
    async def load(self, task_id: str) -> CompressedContext | None:
        """
        Load context checkpoint.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Restored context or None if not found
        """
        checkpoint_path = self.checkpoint_dir / f"{task_id}.json"
        
        if not checkpoint_path.exists():
            return None
        
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None,
            lambda: checkpoint_path.read_text()
        )
        
        context = CompressedContext.model_validate_json(data)
        logger.info("checkpoint_loaded", path=str(checkpoint_path))
        
        return context
    
    async def delete(self, task_id: str) -> bool:
        """
        Delete a checkpoint.
        
        Args:
            task_id: Task identifier
            
        Returns:
            True if deleted, False if not found
        """
        checkpoint_path = self.checkpoint_dir / f"{task_id}.json"
        
        if checkpoint_path.exists():
            checkpoint_path.unlink()
            logger.info("checkpoint_deleted", path=str(checkpoint_path))
            return True
        
        return False
