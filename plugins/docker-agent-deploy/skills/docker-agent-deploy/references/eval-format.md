# Eval session format and CLI flags

## Eval directory layout
```
my-agent/
├── agent.yaml
└── evals/
    ├── <uuid>.json               # one eval session
    └── results/                  # auto-created output
        ├── <run-name>.json
        ├── <run-name>.log
        ├── <run-name>.db
        └── <run-name>-sessions.json
```

## Eval session JSON schema
Use `assets/eval-session-example.json` (relative to the skill root) for the
complete example. The shape below is only a structural skeleton, not an
eval to run:

```json
{
  "id": "<session UUID>",
  "title": "<scenario title>",
  "messages": [],
  "evals": {}
}
```

- `messages` holds the recorded conversation. A user entry nests the message
  as `message.message`; assistant entries also set `message.agent_name`.
  Recorded tool calls live in `message.message.tool_calls`.
- `evals` holds scoring criteria and working-directory setup; see the fields
  below. Keep the concrete conversation and assertions in the asset rather
  than maintaining another copy here.

## `evals` object fields
| Field | Type | Description |
| --- | --- | --- |
| `relevance` | string[] | Statements that must be true about the response; scored by the LLM judge |
| `assertions` | object[] | Deterministic checks: `{name, type, value}` |
| `size` | string | Expected response size: `S`, `M`, `L`, `XL` |
| `working_dir` | string | Subdirectory under `evals/working_dirs/` mounted as the container's working dir |
| `setup` | string | Shell script run in the container before the agent executes |

## Assertion types
`contains`, `not_contains`, `equals`, `starts_with`, `ends_with`, `regex`,
`cost_threshold` (dollar amount ceiling), `tool_called`.

## CLI flags
| Flag | Default | Description |
| --- | --- | --- |
| `-c, --concurrency` | `16` | Concurrent evaluation runs |
| `--judge-model` | `anthropic/claude-opus-5` | Model for relevance scoring |
| `--output` | `<eval-dir>/results` | Results/logs/session-db directory |
| `--only` | (all) | Only run evals matching these filename patterns |
| `--base-image` | (default) | Custom base image for eval containers |
| `--container-runtime` | `docker` | Runtime executable (e.g. `podman`) |
| `--keep-containers` | `false` | Keep containers after evaluation for inspection |
| `-e, --env` | (none) | Extra env vars to forward into the container |
| `--repeat` | `1` | Repeat each eval k times; also unlocks `pass@k`/`pass^k` |
| `--baseline` | (none) | Prior run JSON to regress-test against |
| `--regression-tolerance` | `0` | Aggregate-rate drop allowed before `--baseline` fails |

Source: https://docs.docker.com/ai/docker-agent/features/evaluation/.
