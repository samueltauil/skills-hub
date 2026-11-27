# v3 descriptor and capabilities

Adapted from the `create-kit-v3` skill in docker/sandbox-kit-spec at
`4d932451613f8df89c8468e2bb7c5286882897ca`. Claims here rest on that source
and the pinned public spec. Only the bundled egress example was exercised
on a live `sbx`; see [sources.md](sources.md) for the cross-check and limits. Section numbers
(§) refer to SPEC-v3 as cited by the source.

The source describes the schema-3 grammar as unfinished, and says that where
the docs and the Go implementation disagree, the code wins. Treat fine
details as provisional and re-check the spec before depending on them.

## Authoring forms and layout

A kit is one OCI image. Its layers are the content and a manifest annotation
carries the **descriptor**: what the kit offers, what it needs from the host
as typed capability requests, and what it needs from other kits. An engine
that does not read the annotation runs it as an ordinary image.

The default authoring form is a companion pair found by filename stem:

```text
<kit>/
  <kit>.yaml           # the descriptor; first line `# syntax=docker/sandbox-kit:3`
  <kit>.dockerfile     # the content recipe (omit for a declaration-only mixin)
  README.md
```

No `dockerfile:` field is needed. Three other forms exist: an inline `build:`
block, a `# kit:` comment descriptor inside a Dockerfile, and a `kind: set`
list of other kits (SPEC-v3 §3). For a complete declaration-only mixin, see
`assets/v3-mixin-egress.yaml`.

## Descriptor skeleton

This is a fragment, not a complete kit: it needs a companion
`<kit>.dockerfile` whose `ARG GH_VERSION` receives the `buildArg` and installs
that exact release. The companion recipe was not part of the source, so none
is shown for `gh`; use the overlay pattern in `references/v3-recipes.md`.

```yaml
# syntax=docker/sandbox-kit:3
schemaVersion: "3"
kind: mixin
displayName: GitHub CLI
description: gh, installed from the official release tarball
sourceUrl: https://github.com/cli/cli
licenses: [MIT]

# One value drives the install, the provide, the published version and the tag.
version: "${{ kit.args.version }}"

args:
  version:
    default: "2.98.0"
    pattern: '^[0-9]+\.[0-9]+\.[0-9]+$'
    description: GitHub CLI release to install
    buildArg: GH_VERSION

provides: ["gh@${{ kit.args.version }}"]
# No requires: this overlay ships a release tarball and needs nothing from the
# workload. Add entries only for what the composed runtime must already have.

capabilities:
  - type: com.docker.sandbox/network-policy@1
    config:
      runtime:
        allow: [github.com, api.github.com]

  - type: com.docker.sandbox/agent-context@2
    config:
      content: Use gh for GitHub operations.
```

Every key is `lowerCamelCase` with acronyms title-cased (`sourceUrl`,
`apiKey`). Decoding is **strict**: an unrecognized key anywhere is an error,
so a misspelled key cannot silently leave a policy absent.

## Capabilities

An optional entry-level `name` gives a short display label and `description`
its explanation. Names may contain spaces and need not be unique; they change
no identity, permission, or merge key. When entries merge, the first nonempty
label in contribution order wins. This label is separate from config fields
such as `apiKey.name`.

A capability is a typed request the host answers. `optional: true` means the
kit degrades without it; the default is required, which fails resolution
closed. Read the capability page for each type you emit; each is normative
for its config and for what a runtime must do. Types below are written
without their `com.docker.sandbox/` prefix.

| Type | Use it for | Easy to get wrong |
|---|---|---|
| `network-policy@1` | egress by host | **Phase-scoped**: an absent phase grants nothing. Hosts your install hooks reach go in `install`, hosts the running agent (or a startup hook) reaches go in `runtime`, hosts both reach go in both. |
| `network-policy@2` | egress bounded by HTTP method and path | Same phases, plus entries that grant only matching requests. Pick `@2` when a host should carry one API and not the rest; stay on `@1` when host alone is the grant. **Exclusive with `@1`**: declaring both is an error, and a bounded allow entry must name its hosts literally. **Verify the bound you rely on**: declare the tightest correct policy, but confirm against your target runtime which parts it enforces before treating one as a security boundary. A refusal is a `403` from the boundary, which an origin can also return, so test a case the origin would allow. |
| `credential@1` | one service's auth | Entries are **required by default**; add `optional: true` unless the kit genuinely cannot run unauthenticated. `phase` accepts a single phase or `[install, runtime]` with shared configuration. Every `inject[].domain` must appear in every listed phase's allow list, matched **exactly**: a `*.example.com` wildcard does not satisfy `api.example.com`. |
| `ssh-agent@1` | git over SSH, SSH commit signing | Set `unrestricted: false` to bound it. `sign: [git]` is all commit signing needs; `authenticate: [git@github.com]` is a login to one server. An entry with `unrestricted: true` (the default) signs anything with every key the user's agent holds: declare that only when a client cannot bind sessions (OpenSSH can), and prefer `credential@1` with HTTPS when a token will do. `optional: true` unless the kit cannot work without it, since many users have no agent running. A hook that uses it declares `SSH_AUTH_SOCK` in `env:`, and only hooks of the granted phase get it. `authenticate` grants a signature, not a connection: the server must also be reachable under the network policy. `phase` accepts a single phase or `[install, runtime]` with shared rules. Commit signing needs git config too (`gpg.format=ssh`, `gpg.ssh.defaultKeyCommand="ssh-add -L"`). |
| `lifecycle@1` | install/startup hooks, staged files | Hook environments are **deny-by-default**. Declare every variable in `env:`, including ones only a child process reads: `curl`, `pip` and `npm` need `HTTP_PROXY`/`HTTPS_PROXY`, and `docker` needs `DOCKER_HOST`. |
| `volume@1` | persistent paths | Declare needed capacity with `size`; omission leaves it unspecified and conflicts with another kit's explicit request. Retained volume settings cannot change on recreation. |
| `host-mount@1` | host-shared caches, datasets, or artifacts | Declare only the absolute, canonical in-container `path` and optional octal `mode`. The runtime owns the host location. Data is shared across sandboxes of the declaring kit, survives sandbox removal, and is visible to the host user. Use an optional group to couple cache setup with the mount. |
| `agent-context@2` | inline instructions the agent reads | v0.50.1 rejects required requests at composition time. Use a supporting host, or `optional: true` only for nonessential guidance. Use `content:` for every body; `contentFile` is rejected. Profile destinations and precedence match @1, but every effective profile contains all selected guidance and the runtime materializes it directly. Kit args and final `kit.env` references expand normally; shell variables remain literal. Do not mix selected @1 and @2 requests. Rebuild every member of a migrated set. The serialized descriptor warns above 64 KiB and fails above 512 KiB after expansion and composition. |
| `agent-context@1` | legacy progressive instructions the agent reads | A workload can supply the legacy workspace-sibling `filename`. An agent workload or mixin supplies `filename` plus an absolute `directory` at its discovery location, which overrides the legacy fallback. Different explicit destinations each get a profile, so agent mixins stack. Tool mixins contribute bodies alone. Use `contentFile:` for a static body, but inline `content:` when the body interpolates an arg, because a staged body is never arg-expanded. |
| `long-running@1` | workloads or service mixins that outlive client sessions | Config-less; a request from any kit applies to the whole sandbox. A background hook or published port does not prevent session auto-stop. Required by default; use `optional: true` only if auto-stop is tolerable. This does not request restart after failure. |
| `git-identity@1` | commits attributed to the runtime-provided user | Config-less; requests only user.name and user.email, not a configuration-source mount. Requires permission; optional when missing identity is tolerable. Signing and authentication are separate grants. |
| `sbx@1` | "launch this as an agent" | Workload-only and config-less, and enforced: a mixin declaring it fails validation. |
| `agent-skill@1` | one bundled skill | `path` names the image directory containing `SKILL.md` and supporting files. The basename is the discovery name unless `config.name` overrides it; the entry-level `name` remains only a display label. |
| `agent-skills@1` | where an agent discovers skills | Declare on the agent workload or agent mixin. The runtime links or otherwise exposes every selected `agent-skill@1` bundle here, and includes host-shared skills when available and enabled. Missing host skills never block startup; `mode` bounds host-store access only. |
| `acp@1` | how to run an ACP agent | Declare on the kit that supplies the launch command, workload or mixin. `agent` is its unversioned provides name; another composed kit may provide it. `command` is a complete non-TTY stdio command, never an argv tail. `env` overlays the session environment; positive `protocolVersion` defaults to 1 and names the protocol major version, not a package release. Use `optional: true` for older hosts. Different configs for one normalized agent conflict. |
| `agent-sessions@1` | the headless verbs a harness drives (run one prompt, continue, resume, list) | Argv tails appended to the launch argv; `prompt` must reference `{{.Prompt}}` and `resume` `{{.SessionID}}`. Most agent kits declare both this and `agent-interactive-sessions@1`; an agent with no interactive mode declares only this. Verify every flag against the tool's real CLI; never invent one. |
| `agent-interactive-sessions@1` | the TUI verbs a human-facing host launches (seeded prompt, continue, resume, session picker, list) | The sibling of `agent-sessions@1` for an agent whose CLI has an interactive mode. **Presence is meaning**: a present key is supported, an absent key is not, and for `continue`, `newSession` and `sessionPicker` `[]` is the launch argv alone (`prompt` and `resume` carry their placeholders, so they are never empty). `newSession` is the exception: omit it when a bare launch opens the TUI, because it then defaults to `lifecycle@1`'s `interactive` launch; if you state both `newSession` and `interactive` they must be the same argv, an explicit `[]` included. `list` is the same command as in `agent-sessions@1`. Declare only verbs you verified. |
| `host-port@1` | one host loopback TCP or UDP service | `host` is required (1-65535); `container` defaults to `host` (also when zero); `transport` is `tcp` (default when empty) or `udp`. `family` selects host loopback: `ipv4` (default), `ipv6`, or `dual` when either reaches the same service; it is part of the grant. The sandbox endpoint stays IPv4 loopback. A mapping conflicts with `port@1` on the same sandbox port and transport. This grants raw access to a host service, not general egress or a published guest port. |
| `dockerd@1` | a Docker Engine (Docker-in-Docker) | Singleton; any kind may declare it. Omit `config` to have the runtime start the engine; `autoStart: false` leaves starting it, waiting for `GET /_ping` to return 200, and the socket's permissions to the kit's own root startup hook, with the same elevation and store (and no wider surface). When kits disagree, the merged entry starts it, so that hook must tolerate an engine already running. Engine settings go in the image's `/etc/docker/daemon.json`. It counts as `privileged@1` plus storage at `/var/lib/docker` on the permission surface, so declaring `privileged@1` beside it is redundant, not refused. By default the runtime starts the `dockerd` on the composed image config's `PATH` before startup hooks and owns `/var/lib/docker`: a `volume@1` or `host-mount@1` at or under it is refused. It does not install the engine; a mixin relying on the workload's keeps `requires: ["deb/docker-ce"]`. Use the `com.docker.sandboxes.start-docker` label only as a transition, beside an optional `dockerd@1`, for runtimes that predate it. |
| `port@1`, `resources@1`, `privileged@1` | inbound ports, limits, elevation | Do not declare on speculation; `privileged@1` is the largest widening available. For an engine inside the sandbox, declare `dockerd@1` instead. |

Declare the least that works: every required capability is a request the user
or host must answer, and `privileged@1`, `host-mount@1`, `host-port@1`,
`ssh-agent@1` with `unrestricted: true`, and `dockerd@1` widen what the kit
can touch. Do not put secret values in a descriptor, arg, or recipe; ask for
the credential with `credential@1` and let the host answer it.

## Volumes and host mounts

Host sharing is a separate grant from `volume@1`, including when the
in-container path stays the same. Do not supply a host path or assume a Linux
bind mount: runtimes may use VM filesystem sharing. Host-shared directories
may have weaker filesystem semantics than private volumes. Concurrent writers
coordinate access themselves. The initial `mode` does not reset existing
directory permissions on later creates. Two host mounts at one path, or a
host mount and a volume there, conflict.

Matching volume requests across kits merge on the cleaned destination;
different sizes, modes, or backing kinds conflict. Sizes compare by byte value
(suffixes use powers of 1024), modes by octal value, and omitted `tmpfs` is
false. Argument-backed sizes and modes remain strings, including byte sizes
such as `1024` and unpadded octal modes such as `755`. An unspecified size or
mode differs from an explicit value. Duplicate destinations within one
declaration block are rejected. When a published set re-exports a volume's
text input, publication keeps the requests separate until create expands and
selects them; matching concrete settings then merge. Do not pin a create-phase
size merely to avoid comparing its placeholder during publication.

**Data lifetime (the inverse of declaring a volume).** Block-volume data
belongs to the sandbox instance, independently of the kits that requested it.
Restart and recreation retain it, including when mixins or the workload
change. Removing a declaration leaves its storage retained and unmounted;
restoring the path reattaches it. Recreation with different settings for a
retained destination refuses before replacing the container. New paths start
empty before hooks; reattachment preserves contents and permissions.
**Removing the instance deletes all its volumes**; creating another with the
same name starts fresh. Tmpfs is empty after stop or recreation. Host mounts
keep their separate sharing contract: their data survives sandbox removal.

## Bundled skills

Use `agent-skill@1` to package a skill as a mixin. Ship the whole directory
under a kit-specific prefix such as `/usr/share/example-skills/review`, and
declare that absolute source path. A source path must be literal after
publishing; use a build-phase argument if it varies. Supporting scripts and
references retain their relative paths. An optional `config.name` overrides
the source basename at discovery destinations; it does not rename or rewrite
the source.

Agent kits declare `agent-skills@1` at their discovery paths. The runtime
links or otherwise exposes every selected `agent-skill@1` bundle at each path,
even when the host store is missing, empty, or disabled. The same declaration
permits host sharing when available, bounded by `mode` and host policy; no
second directory declaration is needed. Runtime assembly of these sources is
implementation-specific. Different source paths claiming one effective name
conflict at composition, and an existing destination entry makes a skill
request unsatisfiable. Without any selected destination, a required skill
request fails; optional requests are skipped and recorded. Registration does
not execute scripts.

## Coupled optional features (groups)

Use a `group` when skipping a capability also needs to skip its hooks, files,
or guidance. Put `optional: true` on the group, never on its members (even
`optional: false` is invalid). Groups are nonempty and cannot nest; required
and one-member groups are valid.

The selection API includes every member or none, before composition. A runtime
supplies decisions on expanded entries; the API owns atomic selection and
ordering. Validate all member configs even in skipped groups. Selected entries
must still satisfy cross-entry rules, and a composition conflict is an error
rather than a reason to skip another group. Singleton arity is per declaration
block; lifecycle lists from selected blocks concatenate, and duplicate file
paths are errors.

Published sets may carry `declarationBlocks` on ordinary items or one-member
group wrappers. Preserve these descriptor-local IDs when reading a published
descriptor. Hand-authored kits normally omit this field.

Selection lasts for one sandbox installation, including restarts. Recreation
selects afresh. A failing selected hook is an execution failure, not optional
unavailability. Skipping a group does not remove old files from reused
volumes, omit image layers, or suppress argument environment exports. Group
names are display labels, not merge keys. Groups extend the unfinished
schema-3 grammar in place: descriptors using them require a reader
implementing this extension, and older strict readers reject them.

## Final environment references

Use `${{ kit.env.HOME }}` in capability configuration strings when a path
depends on the final container environment. Image defaults compose first,
argument `env` exports replace them, and runtime environment overrides win
last. Expansion happens before validation and selection, including inside
groups. Missing names fail; empty values remain empty. This is structural
string substitution, not shell evaluation: `$HOME`, `${HOME}`, and `~/` are
unchanged. Do not use environment references in mapping keys or kit metadata,
and do not pass kit placeholders inside argument or environment values.
Persist the expanded descriptor for restart.
