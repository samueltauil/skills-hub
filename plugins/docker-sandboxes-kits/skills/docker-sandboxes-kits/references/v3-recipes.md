# v3 content recipes

Patterns for the `<kit>.dockerfile` beside a v3 descriptor, and the
invariants an overlay has to satisfy. Adapted from `RECIPES.md` in
docker/sandbox-kit-spec at `4d932451613f8df89c8468e2bb7c5286882897ca`; not
re-run against a live `sbx`. See [sources.md](sources.md) for provenance and
limits. For the surrounding workflow, see
[Build, run, and verify](../SKILL.md#v3-build-run-and-verify).

The base images, URLs, and tool names below are illustrative placeholders. The
`dhi.io/*` base images are the source's choice for carrying the runtime's
platform floor; their public availability is not verified here.

## A workload

A workload's layers are the root filesystem, so its recipe is an ordinary
image build. Build on a base carrying the runtime's platform floor: `bash`,
`sh`, `curl`, `git`, a CA store, and a non-root `agent` user at uid 1000 with
home `/home/agent`. The source names the hardened `dhi.io/sbx-templates:*`
images as providing it. A bare distro base builds fine and fails at agent
launch.

```dockerfile
# syntax=docker/dockerfile:1
ARG BASE_IMAGE=dhi.io/sbx-templates:shell-docker
FROM ${BASE_IMAGE}

ARG TOOL_VERSION
USER root
# Prefer pinning a vendor-published checksum as well; none is shown because it
# is specific to each tool and architecture.
RUN set -eux; \
    curl -fsSL "https://example.com/releases/${TOOL_VERSION}/tool-linux-$(dpkg --print-architecture)" \
      -o /usr/local/bin/tool; \
    chmod 0755 /usr/local/bin/tool; \
    # The pin is a claim about content: make the build enforce it.
    reported=$(tool --version); \
    test "$reported" = "tool ${TOOL_VERSION}"

# The runtime contract lives in the image config, not the descriptor.
ENV IS_SANDBOX=1
USER agent
WORKDIR /home/agent/workspace
# Add launch flags only after verifying them against the tool's real CLI. Do not
# copy a flag that disables the agent's own permission prompts unless you intend
# the agent to run unprompted inside the sandbox.
ENTRYPOINT ["tool"]
```

The version assertion assumes the tool prints exactly `tool VERSION` on
stdout and exits successfully. Adapt that complete literal format to the
real CLI (or use its machine-readable version field); never use a substring
or regex match. A command failure, extra suffix, or different version must
fail the build.

`ENTRYPOINT` plus `CMD` is the headless argv. Use `CMD` only for default
*arguments* to the entrypoint's binary; a `CMD` that repeats the binary
appends a stray argument. An interactive argv tail has no image-config slot
and goes in `lifecycle@1`'s `interactive:` field.

## A mixin overlay

An overlay lands on a filesystem you have never seen. Stage everything under
`/out` in a build stage and copy that into `scratch`:

```dockerfile
# syntax=docker/dockerfile:1
FROM dhi.io/debian-base:trixie-dev AS build
ARG TOOL_VERSION
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
RUN set -eux; \
    mkdir -p /out/usr/local/bin; \
    curl -fsSL "https://example.com/releases/${TOOL_VERSION}/tool" -o /out/usr/local/bin/tool; \
    chmod 0755 /out/usr/local/bin/tool

# The overlay: lands on any base.
FROM scratch
COPY --from=build /out /

# Static env belongs on the FINAL stage: a build stage's config is discarded.
# A mixin's additive config merges, so this reaches the composed image and the
# agent process; an /etc/profile.d drop would only reach a login shell.
ENV TOOL_HOME=/opt/tool
```

A merged env key other than `PATH` is first-writer-owned: a second kit may
restate the same value, and a different one refuses the composition. Keep
`ENV` to keys the tool owns. A key a base may already set to something else
(`BROWSER`, `TERM`, `LANG`) is what the source's `codex-mixin` and
`cursor-mixin` examples leave to a login profile instead, which applies over
the base's value and reaches only login shells.

Prefer `/usr/local` and `/opt`, and **avoid the agent's home entirely** where
you can: whatever is at `/home/agent` on the composed base may be a mounted
volume, and staging there is how the ownership traps below get hit.

Where the install cannot be relocated (an installer with no prefix option, a
language toolchain that bakes absolute paths), run the unmodified install on
the workload's own base as the build stage, then copy the specific resulting
paths out. Say in a comment why that shape was chosen. **Not apt packages**:
copying selected paths out of one leaves its dpkg state and shared-library
closure behind, so the copy-out shape produces a broken overlay rather than a
portable one.

Some things genuinely cannot travel in an overlay, and the honest move is to
document the limitation rather than fake it: apt packages (they need the
composed base's dpkg database and their shared-library closure), and anything
that must *merge* into a file the base also writes, since a layer replaces a
file rather than merging it.

**A virtualenv travels only if its interpreter travels with it.** A venv keeps
packages in `lib/python3.<minor>` and points `bin/python` at an absolute
interpreter path. Point it at the build base's `/usr/bin/python3` and the
copied tree resolves the *composed* base's python instead, looks for
site-packages under that base's minor version, and fails with
`ModuleNotFoundError` after the launcher has started, so the kit reports
success at create and breaks at use. Two ways out:

- **Bundle the interpreter.** `uv tool install --managed-python --python 3.14`
  downloads a standalone CPython into `~/.local/share/uv`, which the overlay
  copies, so `bin/python` resolves inside the tree it ships with. Verify by
  composing onto a base with **no python at all** and running the tool.
- **Leave it a create-time hook.** Where the venv must use the base's own
  python (because an apt hook installs that python in the first place), the
  install belongs at create, and the overlay carries only what is portable
  (an `ENV` and a wrapper script, say).

The failure is invisible when the build base and the test base happen to
share a minor version, so check `readlink -f <venv>/bin/python`: a path under
the overlay's own tree is self-contained, `/usr/bin/python3` is not.

## Ownership

**An overlay's directory entries override the base's**, so an overlay states
ownership for every level it ships, and both directions are bugs:

- `/home` owned by uid 1000 hands the agent a directory it should not own.
- `/home/agent` owned by root takes `$HOME` from the agent user, and the
  entrypoint runs as that user, so its own `chown` would be a no-op.

Three ways to get this wrong, all seen in practice per the source:

```dockerfile
COPY --chown=1000:1000 x /home/agent/x   # BuildKit chowns every parent it creates → /home is 1000
RUN chown -R 1000:1000 /out              # same result, via the staging root
RUN chown -R 1000:1000 /out/home/agent/x # one level too deep → /home/agent stays root
```

The idiom that gets both right starts the chown exactly at the agent's home:

```dockerfile
USER root
RUN mkdir -p /out/home/agent \
 && cp -a /home/agent/.local /out/home/agent/.local \
 && chown -R 1000:1000 /out/home/agent
```

Numeric ids, because `scratch` carries no `/etc/passwd` for a name to resolve
against.

**Foreign owners ride along in package trees.** npm and PyPI tarballs and
vendor release archives preserve whatever uid the publisher's machine had,
and `cp -a` or `tar -x` carries it in. Real examples are `501:20` (a macOS
developer), `1001:1001` and `2000:2000` (CI runners). Harmless in a build
stage; as image content on an unknown base those ids may be real accounts,
and a file's owner can rewrite it whatever its mode says. Normalize a copied
package tree with `chown -R 0:0`, which is what a root-run install leaves
anyway: the agent needs write access to a *prefix directory* to add packages,
not to the tool's own tree.

## Verifying an overlay

A build proves the recipe ran. It does not prove the overlay works.

Select the named `kit-builder` container builder created in
[Build, run, and verify](../SKILL.md#v3-build-run-and-verify).

**Judge the exported layout with `kit-tck`:**

```sh
docker buildx build --builder kit-builder . -f <kit>.yaml -t <kit>:<version> \
  --output type=oci,dest=/tmp/layout,tar=false
kit-tck validate --layout /tmp/layout <version>
```

`kit-tck` judges the two directory levels on every platform manifest:
`overlay-home-ownership` fails an overlay that ships `/home` owned by anyone
but root or `/home/agent` by anyone but uid 1000 (`/home` handed to the
agent, or `/home/agent` taken from it). An overlay shipping neither directory
passes, because it is staying out of the home entirely. The same run warns
under `overlay-links-resolve` for every symlink the overlay's own layers do
not resolve; see the composition shortcut below for why that is a warning.

What it does not judge is **every other owner**. Use the bundled audit,
resolving `SKILL_DIR` to this installed skill's directory (Python 3.11+):

```sh
python3 "$SKILL_DIR/scripts/audit-layer-owners.py" /tmp/layout <version>
```

The audit follows the selected tag through OCI indexes/manifests and reads
only referenced filesystem layers, not arbitrary config/manifest JSON blobs.
It checks blob digests, lists numeric uid/gid pairs without extracting files,
and fails on missing, corrupt, unreadable or unsupported-compression layers.
It emits counts only after every selected layer has been read successfully.
Uncompressed and gzip layers are supported; re-export with gzip if the audit
rejects zstd or another compression format. Buildx attestation manifests are
explicitly excluded by their `vnd.docker.reference.type` annotation.

Every count should be `0/0` or `1000/1000`; other owners produce a nonzero
exit status. This is an owner inventory, not a merged-filesystem proof.
Directory-level ownership and symlink semantics remain `kit-tck`'s job.

**Compose it for real and run the tool.** The assembler is the only thing
that performs an actual composition, so it is the check that counts:

```sh
sbx run ./<workload> --kit ./<kit> --detach --name t .
sbx exec t tool --version
```

`sbx exec` is the verb that runs a command. Arguments after `--` on `sbx run`
are **agent** arguments appended to the agent's start command, so
`sbx run … -- tool --version` starts the workload's agent with
`tool --version` tacked on and never executes the overlay's binary at all.

That merges the additive image config (the `ENV` and `PATH` the overlay sets
on its final stage) and puts the overlay on a base that carries the platform
floor, which is what the kit is entitled to assume. The test sandbox `t` is
yours to clean up afterwards: removal is destructive, so confirm first and use
`docker-sandboxes-lifecycle` for the exact `sbx rm` form.

There is a faster filesystem-only shortcut, but know what it does **not** do
before trusting it:

```sh
docker buildx build --builder kit-builder . -f <kit>.yaml -t <kit>-test:local --load
printf 'FROM <the workload base>\nCOPY --from=<kit>-test:local / /\n' \
  | docker build -t compose-test -
docker run --rm --user 1000:1000 compose-test sh -lc 'tool --version'
```

`COPY --from` transfers the overlay's **files and nothing else**: its image
config is discarded, so the `ENV` and `PATH` entries the assembler would have
merged are simply absent. A correct mixin whose tool depends on either will
fail here, and that failure is an artifact of the shortcut rather than a
defect in the kit. Export those variables by hand if you use it. Use the
*workload's* base rather than a stock `ubuntu:24.04` for the same class of
reason: a bare distro image lacks parts of the platform floor, so a kit that
legitimately relies on `git` or the `agent` user fails for reasons the real
composition would not produce.

The Dockerfile arrives on **stdin** so the build context stays empty;
pointing it at `/tmp` uploads whatever else is sitting there, including the
layout you just exported, to build two lines. And `sh -lc` sources any
`/etc/profile.d` drop the overlay ships, which a bare `sh -c` does not. The
`-test:local` image and `compose-test` image are local build artifacts you
created; removing them is destructive, so confirm before you do
(`docker-destructive-guardrails`).

What the shortcut is genuinely good for is **dangling symlinks** against a
real base. Installers routinely relocate a launcher without its payload (a
`--prefix` or `INSTALL_DIR` option moves the symlink while the real tree
stays in `$TOOL_HOME` or a `downloads/` directory), and a build-stage
`test -x` on the launcher passes because the payload is still sitting behind
it *in that stage*. The overlay then ships a link to nothing. `kit-tck`'s
`overlay-links-resolve` warns about every link the overlay cannot resolve by
itself, but only warns: from the artifact alone, a link into the base looks
the same as one into a vanished build stage. The composition tells the two
apart. Gate on the resolved binary, and confirm with the real composition
above.
