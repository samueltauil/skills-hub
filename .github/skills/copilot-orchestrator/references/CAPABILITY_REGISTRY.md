# Capability Registry

> **Version:** 1.0.0  
> **Purpose:** Map user intents to orchestrator configurations

This registry documents all capabilities the orchestrator can fulfill, mapping natural language intents to specific task types, tools, and configurations.

---

## Overview

The Capability Registry serves as:

1. **Intent Router**: Maps user phrases to task types
2. **Tool Selector**: Specifies which tools each capability needs
3. **Configuration Guide**: Provides optimal settings per capability
4. **Documentation**: Helps users discover available features

```
User Intent ──▶ [Capability Match] ──▶ TaskType + Tools + Config
```

---

## Registry Structure

Each capability is defined as:

```yaml
capability:
  id: unique_identifier
  name: Human-readable name
  description: What this capability does
  
  triggers:
    keywords: [list, of, trigger, words]
    patterns:
      - regex patterns for matching
    examples:
      - "Example user request"
  
  configuration:
    task_type: IMPLEMENT | ANALYZE | DEBUG | ...
    tools:
      required: [must_have_tools]
      optional: [nice_to_have_tools]
    token_budget: 8000
    priority_boosts:
      - pattern: "*.test.*"
        boost: 200
```

---

## Core Capabilities

### 1. Code Implementation

**ID:** `implement_code`

| Aspect | Details |
|--------|---------|n| **Description** | Create new code, features, or functionality |
| **Task Type** | `IMPLEMENT` |
| **Required Tools** | `read_file`, `write_file`, `list_directory` |
| **Optional Tools** | `search_code`, `analyze_code`, `run_command` |

**Trigger Keywords:**
```
implement, create, add, build, make, write, develop,
code, new feature, add endpoint, create function,
build component, make module
```

**Example Requests:**
- "Implement user authentication with JWT"
- "Create a REST API for product management"
- "Add a caching layer to the database service"
- "Build a file upload component"

**Optimal Configuration:**
```python
{
    "token_budget": 8000,
    "context_priority": {
        "interfaces": "CRITICAL",
        "existing_patterns": "HIGH",
        "tests": "MEDIUM",
        "docs": "LOW"
    }
}
```

---

### 2. Code Analysis

**ID:** `analyze_code`

| Aspect | Details |
|--------|---------|n| **Description** | Understand, review, or explain existing code |
| **Task Type** | `ANALYZE` |
| **Required Tools** | `read_file`, `list_directory`, `analyze_code` |
| **Optional Tools** | `search_code` |

**Trigger Keywords:**
```
analyze, review, explain, understand, inspect, audit,
what does, how does, check, examine, find issues
```

**Example Requests:**
- "Analyze the authentication flow"
- "Review this pull request for security issues"
- "Explain how the caching system works"
- "What does the UserService class do?"

**Optimal Configuration:**
```python
{
    "token_budget": 12000,  # More context for analysis
    "context_priority": {
        "target_files": "CRITICAL",
        "dependencies": "HIGH",
        "callers": "HIGH",
        "tests": "MEDIUM"
    }
}
```

---

### 3. Bug Fixing / Debugging

**ID:** `debug_fix`

| Aspect | Details |
|--------|---------|n| **Description** | Find and fix bugs, errors, or issues |
| **Task Type** | `DEBUG` |
| **Required Tools** | `read_file`, `write_file`, `search_code` |
| **Optional Tools** | `run_command`, `analyze_code` |

**Trigger Keywords:**
```
debug, fix, error, bug, issue, problem, broken,
failing, crash, exception, not working, broken,
why is, doesn't work
```

**Example Requests:**
- "Fix the TypeError in the payment processor"
- "Debug why login is failing"
- "The API returns 500 errors, please fix"
- "Why does this test fail?"

**Optimal Configuration:**
```python
{
    "token_budget": 10000,
    "context_priority": {
        "error_location": "CRITICAL",
        "stack_trace_files": "CRITICAL",
        "recent_changes": "HIGH",
        "related_tests": "HIGH"
    }
}
```

---

### 4. Code Refactoring

**ID:** `refactor_code`

| Aspect | Details |
|--------|---------|n| **Description** | Improve code structure without changing behavior |
| **Task Type** | `REFACTOR` |
| **Required Tools** | `read_file`, `write_file`, `search_code` |
| **Optional Tools** | `analyze_code`, `run_command` |

**Trigger Keywords:**
```
refactor, improve, optimize, clean, restructure,
simplify, reorganize, extract, rename, move,
clean up, make better
```

**Example Requests:**
- "Refactor the UserService to use dependency injection"
- "Extract the validation logic into a separate module"
- "Clean up the duplicate code in handlers"
- "Simplify this complex function"

**Optimal Configuration:**
```python
{
    "token_budget": 12000,
    "context_priority": {
        "target_files": "CRITICAL",
        "dependents": "CRITICAL",  # Files that depend on this
        "tests": "CRITICAL",  # Must not break tests
        "similar_patterns": "HIGH"
    }
}
```

---

### 5. Testing

**ID:** `write_tests`

| Aspect | Details |
|--------|---------|n| **Description** | Create or improve tests |
| **Task Type** | `TEST` |
| **Required Tools** | `read_file`, `write_file`, `run_command` |
| **Optional Tools** | `search_code`, `list_directory` |

**Trigger Keywords:**
```
test, tests, testing, spec, coverage, unit test,
integration test, e2e, end-to-end, mock, fixture,
assert, verify, validate
```

**Example Requests:**
- "Write unit tests for the AuthService"
- "Add integration tests for the API endpoints"
- "Create test fixtures for the user model"
- "Improve test coverage for the utils module"

**Optimal Configuration:**
```python
{
    "token_budget": 10000,
    "context_priority": {
        "module_under_test": "CRITICAL",
        "existing_tests": "HIGH",
        "test_utilities": "HIGH",
        "fixtures": "MEDIUM"
    }
}
```

---

### 6. Code Generation / Scaffolding

**ID:** `generate_scaffold`

| Aspect | Details |
|--------|---------|n| **Description** | Generate boilerplate, templates, or project structure |
| **Task Type** | `GENERATE` / `SCAFFOLD` |
| **Required Tools** | `write_file`, `list_directory` |
| **Optional Tools** | `read_file`, `run_command` |

**Trigger Keywords:**
```
generate, scaffold, template, boilerplate, starter,
init, setup, bootstrap, create project, new project,
structure, skeleton
```

**Example Requests:**
- "Generate a new Express.js API project"
- "Scaffold a React component with tests"
- "Create the folder structure for a microservice"
- "Generate CRUD endpoints for the Product model"

**Optimal Configuration:**
```python
{
    "token_budget": 6000,  # Less context needed
    "context_priority": {
        "existing_patterns": "HIGH",
        "config_files": "MEDIUM",
        "project_structure": "MEDIUM"
    }
}
```

---

### 7. Deployment & CI/CD

**ID:** `deploy_cicd`

| Aspect | Details |
|--------|---------|n| **Description** | Configure deployment, CI/CD pipelines |
| **Task Type** | `DEPLOY` |
| **Required Tools** | `read_file`, `write_file` |
| **Optional Tools** | `run_command`, `list_directory` |

**Trigger Keywords:**
```
deploy, deployment, release, publish, ship,
production, staging, ci/cd, pipeline, docker,
kubernetes, github actions, azure devops
```

**Example Requests:**
- "Create a GitHub Actions workflow for CI/CD"
- "Add Docker configuration for the API"
- "Set up Kubernetes deployment manifests"
- "Configure automatic deployments to staging"

**Optimal Configuration:**
```python
{
    "token_budget": 6000,
    "context_priority": {
        "existing_pipelines": "HIGH",
        "config_files": "HIGH",
        "dockerfile": "HIGH",
        "package_json": "MEDIUM"
    }
}
```

---

### 8. Automation & Scripting

**ID:** `automate_script`

| Aspect | Details |
|--------|---------|n| **Description** | Create scripts, automate tasks |
| **Task Type** | `AUTOMATE` |
| **Required Tools** | `write_file`, `run_command` |
| **Optional Tools** | `read_file`, `list_directory` |

**Trigger Keywords:**
```
automate, script, workflow, action, schedule,
cron, batch, pipeline, process, task,
run automatically
```

**Example Requests:**
- "Create a script to backup the database"
- "Automate the deployment process"
- "Write a cron job to clean old logs"
- "Create a pre-commit hook for linting"

**Optimal Configuration:**
```python
{
    "token_budget": 6000,
    "context_priority": {
        "existing_scripts": "HIGH",
        "config_files": "MEDIUM",
        "documentation": "LOW"
    }
}
```

---

### 9. Migration

**ID:** `migrate_upgrade`

| Aspect | Details |
|--------|---------|n| **Description** | Migrate to new versions, frameworks, or patterns |
| **Task Type** | `MIGRATE` |
| **Required Tools** | `read_file`, `write_file`, `search_code` |
| **Optional Tools** | `run_command`, `analyze_code` |

**Trigger Keywords:**
```
migrate, upgrade, convert, port, transition,
switch, move to, update from, replace with,
deprecate
```

**Example Requests:**
- "Migrate from Jest to Vitest"
- "Upgrade React from v17 to v18"
- "Convert the codebase from JavaScript to TypeScript"
- "Move from REST to GraphQL"

**Optimal Configuration:**
```python
{
    "token_budget": 16000,  # Large context for migrations
    "context_priority": {
        "affected_files": "CRITICAL",
        "config_files": "CRITICAL",
        "dependencies": "HIGH",
        "tests": "HIGH"
    }
}
```

---

### 10. Performance Optimization

**ID:** `optimize_performance`

| Aspect | Details |
|--------|---------|n| **Description** | Improve performance, reduce resource usage |
| **Task Type** | `OPTIMIZE` |
| **Required Tools** | `read_file`, `write_file`, `analyze_code` |
| **Optional Tools** | `run_command`, `search_code` |

**Trigger Keywords:**
```
optimize, performance, speed, fast, slow,
memory, cpu, efficient, bottleneck, profile,
latency, throughput
```

**Example Requests:**
- "Optimize the database queries in UserRepository"
- "Reduce memory usage in the image processor"
- "Speed up the API response time"
- "Find and fix the performance bottleneck"

**Optimal Configuration:**
```python
{
    "token_budget": 10000,
    "context_priority": {
        "target_code": "CRITICAL",
        "performance_tests": "HIGH",
        "metrics_config": "HIGH",
        "dependencies": "MEDIUM"
    }
}
```

---

## Capability Matching Algorithm

```python
def match_capability(user_input: str) -> Capability:
    """
    Match user input to the best capability.
    
    Algorithm:
    1. Tokenize and normalize input
    2. Score each capability:
       - Keyword matches × weight
       - Pattern matches × weight
       - Semantic similarity (if available)
    3. Apply context modifiers:
       - Project type (web, cli, library)
       - Recent activity (debugging session?)
    4. Return highest scoring capability
    """
    scores = {}
    
    for capability in REGISTRY:
        score = 0
        
        # Keyword matching
        for keyword in capability.triggers.keywords:
            if keyword in user_input.lower():
                score += keyword_weight(keyword)
        
        # Pattern matching
        for pattern in capability.triggers.patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                score += 50
        
        # Confidence boost for exact examples
        for example in capability.triggers.examples:
            similarity = compute_similarity(user_input, example)
            if similarity > 0.8:
                score += 100 * similarity
        
        scores[capability.id] = score
    
    return max(scores, key=scores.get)
```

---

## Custom Capability Registration

### Adding New Capabilities

```python
from models import TaskType
from capability_registry import register_capability

@register_capability(
    id="my_custom_capability",
    name="Custom Feature",
    description="Does something specific to my domain"
)
class MyCapability:
    task_type = TaskType.IMPLEMENT
    
    triggers = {
        "keywords": ["custom", "specific", "my feature"],
        "patterns": [r"do the (custom|specific) thing"],
        "examples": ["Do the custom thing for users"]
    }
    
    tools = {
        "required": ["read_file", "write_file"],
        "optional": ["my_custom_tool"]
    }
    
    @classmethod
    def configure(cls, context: dict) -> dict:
        """Return capability-specific configuration."""
        return {
            "token_budget": 8000,
            "priority_boosts": [
                ("*.custom.*", 200)
            ]
        }
```

---

## Capability Quick Reference

| ID | Task Type | Key Triggers | Primary Tools |
|----|-----------|--------------|---------------|
| `implement_code` | IMPLEMENT | implement, create, add | write, read, list |
| `analyze_code` | ANALYZE | analyze, explain, review | read, analyze |
| `debug_fix` | DEBUG | fix, debug, error | read, write, search |
| `refactor_code` | REFACTOR | refactor, improve, clean | read, write, search |
| `write_tests` | TEST | test, coverage, spec | read, write, run |
| `generate_scaffold` | GENERATE | generate, scaffold | write, list |
| `deploy_cicd` | DEPLOY | deploy, ci/cd, docker | read, write |
| `automate_script` | AUTOMATE | automate, script | write, run |
| `migrate_upgrade` | MIGRATE | migrate, upgrade, convert | read, write, search |
| `optimize_performance` | OPTIMIZE | optimize, slow, performance | read, write, analyze |

---

## Context Priority Matrix

| File Pattern | IMPLEMENT | ANALYZE | DEBUG | TEST | REFACTOR |
|--------------|-----------|---------|-------|------|----------|
| Target file | CRITICAL | CRITICAL | CRITICAL | CRITICAL | CRITICAL |
| Test files | MEDIUM | MEDIUM | HIGH | CRITICAL | CRITICAL |
| Config files | LOW | MEDIUM | MEDIUM | MEDIUM | LOW |
| Dependencies | HIGH | HIGH | HIGH | LOW | CRITICAL |
| Documentation | LOW | HIGH | LOW | LOW | LOW |
| Recent changes | LOW | LOW | HIGH | LOW | MEDIUM |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024 | Initial capability registry |
