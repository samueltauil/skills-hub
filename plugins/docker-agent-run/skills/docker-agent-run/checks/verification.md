# Verification Runbook for `docker agent run`

## 1. Credentials and model are resolvable before running
```bash
docker agent doctor ./agent.yaml
```
Pass: the resolved model/provider is reported reachable with credentials
found. Fail: "No model is currently available" — follow the Troubleshooting
section in this skill's `SKILL.md`, then rerun this check.

## 2. The chosen safety mode matches the run context
```bash
docker agent run --exec --safety restricted ./agent.yaml "Delete all files in /tmp/scratch"
```
Use a task that deliberately triggers a non-safe tool call (a destructive
shell command against a throwaway agent/directory is a good probe). Pass
(unattended/CI run): the command exits promptly without hanging on an
approval prompt, and the output reports the destructive call was **denied**
rather than silently executed. Fail: the run hangs waiting for approval —
the mode is too strict for a headless run — or the destructive command
actually executes — the mode is too permissive; move to `balanced`/`strict`.

## 3. A sandboxed run has the network access it needs
```bash
docker agent run --sandbox ./agent.yaml
```
Pass: the run's printed launch summary shows the allowlisted hosts and no
`403 Blocked by network policy` errors occur for hosts the agent actually
needs. Fail: a `403` for a specific host — run
`docker agent sandbox allow <host>` and rerun.

## 4. An alias resolves to the config and options you expect
```bash
docker agent alias list --json
```
Pass: the alias's `path`, `model`, `safety`, and `sandbox`/`yolo` fields
match what you configured. Fail: missing or wrong fields — recreate the
alias with `docker agent alias add <name> <path> [flags]`.
