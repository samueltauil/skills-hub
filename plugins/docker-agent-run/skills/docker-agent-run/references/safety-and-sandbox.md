# Safety modes and sandbox reference

## Safety mode / flag interaction
| Mode | Approval behavior | Typical use |
| --- | --- | --- |
| `strict` | Ask before every tool call | First run of an untrusted agent |
| `balanced` | Auto-approve calls classified as safe, ask for the rest | Everyday interactive use |
| `restricted` | Auto-approve safe calls, **deny** the rest | Unattended/CI runs, server modes (`serve` default) |
| `autonomous` (`--yolo`) | Approve everything | Fully trusted or already-sandboxed agent |

Precedence: an explicit `--safety`/`--yolo` on the `docker agent run` command
line always overrides an alias's stored safety option, which in turn
overrides any default baked into `agent.yaml`.

Source: https://docs.docker.com/ai/docker-agent/features/cli/ (Commands >
`docker agent serve chat` shows `restricted` as the serve default;
`docker agent run --help` for the four mode names).

## Sandbox trust boundary
- Boundary: a hypervisor-isolated microVM per sandbox. No shared memory or
  processes with the host.
- Crosses into the VM: the mounted workspace directory (read-write by
  default), host-injected credential headers (raw values never enter the
  VM), and allowlisted outbound TCP.
- Not isolated by default: workspace file changes are live on the host in
  direct mode (the default); Git hooks under `.git/` run with host
  permissions when a modified script executes; the default network allowlist
  includes broad wildcards (e.g. `*.googleapis.com`).
- Local stdio MCP servers run **outside** the sandbox VM, on the host —
  treat them as trusted host integrations, not sandboxed ones.

Source: https://docs.docker.com/ai/sandboxes/security/.

## Sandbox network allowlist commands
```bash
docker agent sandbox allow <host>[:<port>]   # persist an allowlist entry
docker agent sandbox list                    # show persisted entries
docker agent sandbox deny <host>             # remove one
```
Persisted entries live in `~/.config/cagent/config.yaml` and are unioned with
the inferred and agent-declared allowlists on every `--sandbox` run.

Source: https://docs.docker.com/ai/docker-agent/configuration/sandbox/.
