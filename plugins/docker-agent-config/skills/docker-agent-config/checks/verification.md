# Verification Runbook for agent.yaml

Before resolving a config or contacting a model:
- Inspect `instruction`, `instruction_file`, and command prompts for literal
  secrets or interpolated sensitive values. An env-file reference does not
  keep a value out of the resolved prompt.
- Confirm provider and tool/MCP credentials use their authentication mechanisms;
  a custom provider's `token_key` must name an environment variable, not expand
  its value into the config.
- Use throwaway values when testing interpolation. Do not print real credentials
  in resolved config output or send them to a model as a test. Secret redaction
  is pattern-based defense in depth, not proof that prompts contain no secrets.

## 1. The config resolves without errors
```bash
docker agent debug config ./agent.yaml
```
Pass: prints the fully-resolved YAML (defaults applied, provider/model
references resolved, `instruction_file` inlined). Fail: an error naming the
missing/invalid key — fix that key and rerun.

## 2. Every declared toolset actually exposes tools
```bash
docker agent debug toolsets ./agent.yaml
```
Pass: each agent lists at least the tools you expect (e.g. `filesystem` shows
`read_file`, `write_file`, `list_directory`; an MCP `ref:` shows the remote
server's tools). Fail (empty list for one agent, or an MCP ref shows none):
the `ref:` is wrong, the MCP server needs credentials, or the toolset type is
misspelled — check `references/toolsets-and-providers.md`.

## 3. The model/provider is reachable
```bash
docker agent doctor ./agent.yaml
```
Pass: reports the resolved model and provider as reachable, with credentials
found. Fail: "No model is currently available" — use `docker-agent-run` for
credential/DMR-model troubleshooting, then rerun this check. For a named-provider
configuration error, recheck `models:`/`providers:` spelling against
`docker agent debug config`.

## 4. A minimal smoke run behaves as instructed
```bash
docker agent run --exec ./agent.yaml "Say hello and list your tools"
```
Pass: the agent responds without a tool-call error and, if `toolsets` are
set, the tools it names match what `docker agent debug toolsets` reported.
Fail: a tool-call error naming a toolset — the toolset's `command`/`ref` is
misconfigured.
