# Referencing a kit from sbxenv.yaml

What a kit author or consumer needs to know about how an `sbxenv.yaml`
environment file (`schemaVersion: "1"`, experimental `sbx env`) references
and configures a kit. The file's own schema `"1"` is unrelated to a kit
descriptor's `schemaVersion: "3"`. This page covers only the `agent:` and
`kits:` fields and the fields a kit's capabilities map onto. The rest of the
file (lifecycle hooks, approval plan, merging, secrets provisioning) is not
covered by this catalog; answer it from the Docker Docs
[environment files](https://docs.docker.com/ai/sandboxes/configuration/environment-files/)
page. Provenance is in `sources.md`.

## `agent:` and `kits:`

```yaml
schemaVersion: "1"
agent: shell                                   # built-in agent, or a workload kit's handle
kits:
  - sbx/example:1.2.3                          # OCI, tag
  - sbx/example:1.2.3@sha256:<digest>          # OCI, tag + digest (reproducible)
  - source: sbx/example-mixin:4.5.6            # OCI with kit args
    args:
      model: ${{ env.args.model }}
  - ./kits/dev-tools                           # local directory, built on create
  - ./dist/tool.zip                            # local ZIP
  - git+https://github.com/org/repo.git#ref=<commit>&dir=kits/tool   # git, pinned (or git+ssh://)
workspace: .
```

The references above illustrate shapes only; they are not recommendations.
Resolve a real reference's tag and digest from the registry at the time you
write it.

- **One workload.** A composition has exactly one workload and any number of
  mixins. `agent:` is a built-in agent (`claude`, `codex`, `shell`, …) or the
  **handle** of the one `kind: workload` kit under `kits:`. To add tools to a
  built-in agent, keep the built-in name and list only mixins. On sbx v0.51.0
  the built-in `shell` agent resolves as the kit `docker.io/sbx/shell`.
- **Handle.** A v3 kit's handle is the last path segment of its repository
  (`sbx/claude` → `claude`); for a git source it is the `dir=` basename, for
  a local directory the directory name. This is why a workload's directory
  name matters: a local workload named after a built-in agent (for example
  `shell`) collides with it.
- **`X` and `X-mixin`.** When both exist, `X` is the workload and `X-mixin`
  layers that agent onto another workload. Use the mixin only when the user
  wants a different base.
- **Relative sources.** Only `./…`, `../…`, `.`, `..`, or a path ending in
  `.zip` are file paths, resolved against the **declaring file's directory**.
  A bare `kits/tool` is a registry reference.
- **Pin for reproducibility.** A tag can be republished (on 2026-11-12
  `sbx/playwright:1.61.1` moved to a new digest), so a tag alone is not
  reproducible. Prefer `tag@sha256:<digest>` for OCI and `#ref=<commit>` for
  git. Pick the highest version release tag, not the most recently pushed
  tag or `latest`.
- **Allowed sources.** Remote sources must match the `kit.allowedSources`
  setting (Docker Hub by default). `sbx settings set kit.allowedSources
  '[...]'` replaces the whole allowlist.
- **Merged files.** When several environment files are merged, `kits`
  entries naming the same source fold into one entry whose `args` merge key
  by key.
- **Changes need recreation.** On an existing environment, changes to
  `kits:`, kit host mounts, ports, secrets, bindings, workspaces, and
  `sandboxOptions` take effect only after `sbx env rm` and a new create.

## Upgrading a referenced kit

Before moving an entry to a new release, compare the old and new descriptors
(for example the published `/usr/share/sandbox/kit/<kit>/kit.yaml` inside a
disposable sandbox composed with each release), and reconcile:

- **args:** remove an arg the new release no longer declares, set a new
  required arg, and check the file's values against a tightened
  `enum`/`pattern`.
- **credentials:** a new service, mechanism, or domain needs a binding change.
- **kind and handle:** a changed handle or kind can require changing `agent:`;
  a new required grant (such as `ssh-agent@1`) needs a prerequisite note.

To pin, resolve the digest of the exact tag you inspected, for example with
`docker buildx imagetools inspect <org>/<kit>:<tag>`, and write
`<org>/<kit>:<tag>@sha256:<digest>`. This skill does not search or rank the
public kit catalog.

## Kit args

- Keys in an entry's `args:` are the bare create-phase arg names the kit
  declares. An undeclared arg is an error, and values must satisfy the kit's
  `enum`/`pattern`.
- A **published (OCI) kit accepts only create-phase args.** Build-phase args
  (typically `version`) were fixed at publish time; choose another tag to
  change them. Local-directory and git sources build on create, so their build
  args apply. Build secrets are build inputs only, never runtime credentials.
- For a kit author this is why the single build-phase `version` arg described
  in `SKILL.md` drives the tag: consumers change the tool version by changing
  the tag, not with an arg.
- `--kit-arg name=value` (all kits) or `--kit-arg <handle>.name=value` (one
  kit) overrides `args` for one invocation; `--kit-args-file` reads
  `name=value` lines. Both are experimental. Never pass a secret as an arg; use
  `credential@1` and the credential store.

## Where a kit's capabilities surface in the file

| Kit declares | Consumer's `sbxenv.yaml` |
|---|---|
| `credential@1` (required) | A `bindings.<service>` entry naming only the mechanism used: `apiKey` with the kit's inject domains (an `apiKey` read only through `apiKeyEnv`, with no inject rules, has an empty domain list), or `oauth` (a one-time host sign-in, no secret). Without it, create fails. An optional credential without a binding is skipped silently. The secret value lives in the sbx credential store (see `docker-sandboxes-network-credentials`), never in the file. A service or domain that references a kit arg resolves from the value the file sets; never copy a `${{ … }}` expression into a binding. |
| `host-mount@1` | A grant the user is asked to approve. The runtime owns the host location by default; an optional top-level `mounts:` entry binds the kit's sandbox path to a chosen existing host directory instead (local only). |
| `port@1` | Optional `ports:` entry to pin the host port; otherwise the host port is ephemeral. |
| `ssh-agent@1` (required) | A prerequisite: an SSH agent with a key loaded on the host (`ssh-add -l`). |
| `privileged@1`, `dockerd@1`, `host-port@1`, `host-mount@1` | Grants the user is asked to approve; explain them before asking. |
| A private kit image | A `registries:` entry for that registry. |

## What a clean plan does and does not prove

- `sbx env plan` does **not** resolve kit references. On sbx v0.51.0 it
  planned cleanly for a nonexistent tag and a nonexistent kit; the missing tag
  failed only at create, after approval. An unknown field, by contrast, fails
  strict decoding.
- A mixin can under-declare `requires`. On sbx v0.51.0, `sbx/playwright`
  reported `requires: []`, but composing it onto the bare `shell` agent
  failed at create with `env: 'node': No such file or directory`. A kit
  author should treat that as a reason to make the install hook probe and
  fail with an actionable message; a consumer should treat only a disposable
  `sbx env create` (reviewed plan, no `--force`) followed by `sbx env rm` as
  proof that a composition installs.
