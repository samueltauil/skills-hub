# Sources

## Local pinned source (repository docker/sandboxes, commit df5c96ba60484fa2c375469dbac912c205da6c37)

Paths below are relative to the repository root.

- `AGENTS.md` — "The credential store is the sole runtime source for secrets;
  host environment variables never auto-inject" (repository-wide constraint,
  confirms the design principle behind `sbx secret import` needing explicit
  opt-in and behind never using host env vars as an implicit channel).

- `cli-plugin/commands/registry_secret.go` — `runRegistryCredentialDelete`
  removes exactly the requested sandbox scope; only an unscoped removal
  expands to both host-only and all-sandboxes entries.

- `sandboxlib/agentkits/agents/devin/spec.yaml` — OAuth passthrough without
  sentinels in the built-in Devin kit.
- `sandboxd/pkg/proxy/oauth_handler.go` — `rewriteTokenResponse` forwards
  the original token response when passthrough has no refresh sentinel.
  `oauth_handler_test.go` covers real-refresh-token forwarding and masking
  when a sentinel is configured. The generic help's no-exposure wording
  does not describe the passthrough exception.
- `vendor/github.com/docker/governor-lib/internal/authorization/definitions/allowlist/v0/matching.go`
  — domain glob and CIDR matching; `docs/yml/sbx_policy_deny.yaml` documents
  the domain-before-CIDR precedence caveat.

## Captured standalone CLI help, cross-checked against an older installed build

Installed `sbx` reports `v0.42.0-503-g951b7f6d7` (commit
`951b7f6d7f6bb260fac15077b607109ffe8ae012`), older than the pinned source
HEAD. Verified with `sbx <cmd> --help` under an isolated `--app-name`, no
daemon started. No source-only differences were found for the commands this
skill covers.

- `sbx policy --help` — subcommand list.
- `sbx policy init --help` — one-time setup requirement, `allow-all`/`balanced`/`deny-all` presets, distinction between initial global policy and per-sandbox rules.
- `sbx policy allow network --help` / `sbx policy deny network --help` — `RESOURCES` format (exact/wildcard/port/`**`), `--sandbox` scoping, deny precedence restated.
- `sbx policy check --help` / `sbx policy check network --help` — read-only check against the daemon-side authorizer, `--sandbox`, `--verbose`, `--json`.
- `sbx policy log --help` — allowed/blocked history with matching rule, positional `[SANDBOX]`, `--json`, `--limit`.
- `sbx policy ls --help` / `sbx policy inspect --help` — `--wide` rule IDs, org-governance read-only rules and their exact removal command or reason.
- `sbx policy rm network --help` — `--id` vs `--resource` removal, `--sandbox` scoping.
- `sbx policy reset --help` — exact destructive-scope text: "This deletes the local policy store and stops the daemon... If sandboxes are currently running, they will be stopped when the daemon shuts down." This is the direct source for the must-fix rule that `sbx policy reset` is never a routine diagnostic step.
- `sbx create --help` / `sbx run --help` — `--deny-network` creation-time flag description: "Safe under centralized governance because a local deny can only narrow, never widen, egress."
- `sbx secret --help` — service vs. registry secret model overview: "the proxy uses stored secrets to authenticate API requests on behalf of the agent. The secret is never exposed directly" and "registry credentials are host-only by default... not injected into sandboxes unless --all-sandboxes or --sandbox is set (the credential never enters the sandbox filesystem)."
- `sbx secret set --help` — service secrets list, `--sandbox` scope, dynamic secrets (`--ref` 1Password/AWS, `--command`, `--refresh`), registry credentials (`--registry`, `--all-sandboxes`, `--sandbox`, `--registry-auth-endpoint`, `--password-stdin`, `--username`).
- `sbx secret set-custom --help` — experimental custom-secret placeholder model, `--host` wildcard patterns, `--env`, `--sandbox`.
- `sbx secret ls --help` — scope/service filters, `--json` (never reveals values).
- `sbx secret rm --help` — `--all`, `--registry`, `--all-sandboxes`, `--sandbox`, `--force`; registry removal semantics ("removes host-only and global entries" vs. "--all-sandboxes ... removes only the global (all-sandboxes) registry credential").
- `sbx secret import --help` — host env-var detection, `--all`/`--force` semantics, OAuth-token-present skip rule.

## Not verified / explicitly excluded

- No docs.docker.com URL beyond the canonical product page
  (https://docs.docker.com/ai/sandboxes/) is cited here: this review did
  not independently fetch a dedicated network-policy or credentials docs
  page, so no more specific URL is asserted as a source for any rule above.
  Every rule above traces to a repository path and/or a captured `--help`
  output.
