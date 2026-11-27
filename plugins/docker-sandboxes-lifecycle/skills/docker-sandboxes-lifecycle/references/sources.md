# Sources

## Local pinned source (repository docker/sandboxes, commit df5c96ba60484fa2c375469dbac912c205da6c37)

Paths below are relative to the repository root.

- `AGENTS.md` — repository-level agent instructions, isolated `--app-name` testing rule.
- `README.md` — `sbx login` / `sbx run claude` quick-start; pointer to docs.docker.com/ai/sandboxes/.
- `cli-plugin/commands/run.go` — `resolveCloneWorkdirForExistingSandbox` (reattach `--clone`: no-op only on an existing clone-mode sandbox; errors on a plain/bind-mounted sandbox or a legacy worktree sandbox missing its label), `warnDeprecatedRunPositionalName` (bare `sbx run NAME` prints a deprecation warning but is still accepted — `legacyPositionalAttach`), `directLookupCandidate`/`legacyPositionalAttach` wiring in `executeRun`.
- `cli-plugin/commands/create.go` — `validateCloneOptions` (the four `--clone` preconditions: explicit workspace path, inside a Git repository, not a Git worktree, `.git` a real directory not a file/submodule pointer), `addCreateAgentSubcommand` (`:ro` semantics: "holds that one path out of reach inside a workspace the sandbox can otherwise write" — a write restriction, not a read restriction).
- `cli-plugin/commands/rm.go` — `warnUnsavedCloneChanges` (the exact `git fetch sandbox-<name>` / `refs/remotes/sandbox-<name>/*` vs. survivor `refs/sandboxes/<name>/*` / `git branch <local> refs/sandboxes/<name>/<branch>` recovery text), `removeAll`/`removeByNameConfirmedWithSecretRemoval` (confirmation-prompt and `--force` semantics for `sbx rm`/`sbx rm --all`), `errRemovalDeclined`.
- `cli-plugin/commands/root.go` — `rootFlags` (`--app-name`, hidden persistent flag, "Storagekit application name for isolated daemon instance"), `commandsWithoutDaemon`/`needDaemonAutoStart` (daemon-free commands).
- `docs/yml/sbx_ls.yaml` — agent/status/published-ports/workspace listing,
  `--json`, and `-q`/`--quiet` (sandbox names only).
- `docs/yml/sbx_stop.yaml` — stops one or more sandboxes without removing
  them; retains state for restart with `sbx run`.
- `docs/yml/sbx_exec.yaml` — starts a stopped sandbox before execution;
  local exec flags `-i`, `-t`, `-d`, `-u`, `-w`, `-e`, `--env-file`, and
  `--privileged`.
- `docs/yml/sbx_cp.yaml` — exactly one of SRC/DST must be `SANDBOX:PATH`;
  the other is local, and sandbox-to-sandbox copies are unsupported.
- `docs/yml/sbx_ports.yaml` — lists ports or changes existing bindings with
  `--publish`/`--unpublish`.
- `docs/yml/sbx_create.yaml` / `docs/yml/sbx_run.yaml` — `-p`/`--publish`
  applies at creation only; run's flag explicitly says reattach ignores it
  and directs users to `sbx ports`.
- `docs/yml/sbx_prune.yaml` — current, pinned-source usage text: `--filter until=TIMESTAMP` ("stopped before TIMESTAMP... RFC 3339 timestamp, Unix timestamp, or Go duration relative to now, e.g. until=168h"), not `since=`.

## Captured standalone CLI help, cross-checked against an older installed build

Installed `sbx` reports `v0.42.0-503-g951b7f6d7` (commit
`951b7f6d7f6bb260fac15077b607109ffe8ae012`), older than the pinned source
HEAD. Verified name/version with `sbx version`; captured with
`sbx <cmd> --help` under an isolated `--app-name`, no daemon started.

- **`sbx prune --help` differs from the pinned source**: the installed
  build's help still advertises `--filter since=DURATION` as the supported
  filter syntax. The pinned source's `docs/yml/sbx_prune.yaml` (generated
  from the same `--help` text at commit df5c96ba) instead documents
  `--filter until=VALUE` (RFC 3339 / Unix timestamp / duration). This is an
  explicit source-vs-installed-help difference: prefer `until=` per the
  pinned source, and treat `since=` as a legacy alias an older installed
  build may still show.
- Every other command this skill covers (`create`, `run`, `ls`, `stop`,
  `rm`, `exec`, `cp`, `ports`) showed no source-only difference between the
  installed help and the pinned-source `docs/yml/*.yaml`.

## Not verified / explicitly excluded

- `sbx --cloud` (Docker Cloud Sandboxes) flags appear in the generated
  reference as inherited options but are out of scope for this skill, which
  covers the local daemon only; not exercised or asserted beyond noting
  their existence.
- No docs.docker.com URL beyond the canonical product page
  (https://docs.docker.com/ai/sandboxes/) is cited here: this review did not
  independently fetch any deeper docs.docker.com page, so no more specific
  URL is asserted as a source for any rule above. Every rule above traces to
  a repository path and/or a captured `--help` output, not to a fetched
  docs page.
