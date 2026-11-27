# Verification runbook for v3 kits

A manual runbook for v3 kit descriptors. A1-A8 were exercised on 2026-11-02.
The corrected asset passed build/conformance and runtime composition on
sbx v0.50.1. See [initial results](runtime-results.md) and
[authenticated results](authenticated-results.md) for commands, failures,
corrections, versions and limits. A2/A6 expectations below incorporate the
observed CLI behavior; A7 verifies connectivity, not a policy security boundary.

Prerequisites: Docker with Buildx, a pinned `kit-tck` release or commit that
you have recorded, and an `sbx` release you have confirmed supports Kits v3.
Normal source inspection/validation and composition require sign-in to the
isolated app. `--app-name` isolates credentials too; arrange an interactive
`sbx --app-name "$APP" login` with the operator, never copy credentials.
This runbook publishes nothing and signs nothing. Builds may pull the builder
and frontend from registries; the exported layout is validated locally. It
creates one uniquely named builder and one scratch directory, and the cleanup
step removes only test resources, including app-scoped daemon state. Use an
isolated, unique `--app-name` (at most 20
characters) on every `sbx` invocation. Run from the skill directory in one
shell. If inherited `DOCKER_CLI_PLUGIN_ORIGINAL_CLI_COMMAND` and
`DOCKER_CLI_PLUGIN_SOCKET` make standalone `sbx` act as a Docker plugin,
unset them in this test shell first. Record `sbx version`, `docker buildx
version`, `kit-tck version`, and (for a Go-installed TCK) `go version -m`
on the binary. `kit-tck version` alone may print only `dev`.

## A1. Set up scratch resources

```bash
RUN_ID=$(python3 -c 'import uuid; print(uuid.uuid4().hex)')
APP="k-${RUN_ID:0:18}"        # fresh suffix, at most 20 characters
BUILDER="kit-eval-$RUN_ID"
BUILDER_CREATED=false
WORK=$(mktemp -d /tmp/kit-v3.XXXXXX)
WORK=$(cd "$WORK" && pwd -P)  # short canonical path for macOS runtime sockets
mkdir "$WORK/extra-egress" "$WORK/workspace"
cp assets/v3-mixin-egress.yaml "$WORK/extra-egress/extra-egress.yaml"
if docker buildx create --name "$BUILDER" --driver docker-container; then
  BUILDER_CREATED=true
  export BUILDX_BUILDER="$BUILDER"  # also select it for sbx source builds
  docker buildx inspect --builder "$BUILDER" --bootstrap
else
  printf '%s\n' 'Builder creation failed; stop here and perform A8 without removing that name.' >&2
fi
```
Continue only if create and bootstrap both succeeded. Creation and bootstrap
are separate so a bootstrap failure still leaves ownership recorded for A8.
A failed create never grants permission to remove that name, even if a builder
with it exists. Keep `BUILDER_CREATED` in this shell; do not recreate it by
checking whether the builder exists.

The v3 asset is a companion-pair kit by stem: `extra-egress/extra-egress.yaml`
with no `.dockerfile`, because it is declaration-only. Before A2, have the
operator sign in with this same `$APP` and initialize only its network policy:

```bash
sbx --app-name "$APP" login
sbx --app-name "$APP" daemon start --detach --policy balanced
```

Do not generate a new app name after signing in. Always perform A8, including
after a failed build or composition.

## A2. Inspect the declarations

```bash
sbx --app-name "$APP" kit inspect "$WORK/extra-egress"
sbx --app-name "$APP" kit inspect "$WORK/extra-egress" --format json
```
Pass on v0.50.1: both succeed, report schema v3/kind mixin, and JSON includes
`registry.npmjs.org` in the projected network allow list. This CLI uses a
legacy-shaped view (`sandbox`, `permissions`), not the raw v3 descriptor;
it does **not** print both typed capability names. Do not copy its output as
authoring YAML or treat inspection as capability selection/conformance proof.

The initial v0.50.1 run stopped at sign-in. Its `--offline` retry deliberately
omits the builder and cannot load v3 sources; that is not a substitute for
A2. Source inspection is daemon-backed and may build/import an image. After
operator sign-in, use this normal command. Do not classify an authentication
failure as an unsupported-v3 error.

## A3. Check the descriptor through the frontend

```bash
(cd "$WORK/extra-egress" && docker buildx build --builder "$BUILDER" . \
  -f extra-egress.yaml --output type=cacheonly)
```
Pass: the build succeeds. The descriptor is checked before any content is
built, so a bad field fails here quickly.

## A4. Export a layout and judge it with `kit-tck`

```bash
(cd "$WORK/extra-egress" && docker buildx build --builder "$BUILDER" . \
  -f extra-egress.yaml -t extra-egress:0.0.0 \
  --output type=oci,dest="$WORK/layout",tar=false)
kit-tck validate --layout "$WORK/layout" 0.0.0
kit-tck inspect --descriptor --layout "$WORK/layout" 0.0.0
```
Pass: `kit-tck` reports no failures. Pass the tag alone (`0.0.0`), not
`extra-egress:0.0.0`. Descriptor inspection prints both typed capabilities,
with only the explanatory `agent-context@2` request marked optional. The
required network policy must not be made optional. A build alone is not
proof the kit works.

## A5. Confirm strict decoding rejects a misspelled key

```bash
mkdir "$WORK/typo"
python3 - "$WORK/extra-egress/extra-egress.yaml" "$WORK/typo/typo.yaml" <<'PYCODE'
import pathlib, sys
src = pathlib.Path(sys.argv[1]).read_text()
pathlib.Path(sys.argv[2]).write_text(src.replace('capabilities:', 'capabilites:', 1))
PYCODE
(cd "$WORK/typo" && docker buildx build --builder "$BUILDER" . \
  -f typo.yaml --output type=cacheonly)
```
Pass: the build fails with an unrecognized-key error naming `capabilites`, not
a silent no-op.

## A6. Compare daemon-backed validation with offline rejection

```bash
sbx --app-name "$APP" kit validate "$WORK/extra-egress"
sbx --app-name "$APP" kit validate "$WORK/extra-egress" --offline
```
Pass on v0.50.1: the normal command accepts this valid source through its
configured builder; the offline command rejects it with "no kit builder
configured". Authentication/daemon failures are blockers, not evidence that
the descriptor is invalid. Record both exit codes and messages. Other releases
must be checked rather than assumed to have the same behavior.

This corrects the original A6 expectation that normal validation must fail:
the exact v0.50.1 implementation wires a builder into both normal inspect and
validate. Neither command replaces the layout conformance check or A7.
Authenticated v0.50.1 validation subsequently succeeded; offline validation
failed as expected. Both outcomes are recorded in the results.

## A7. Optional: compose onto a v3 workload (manual)

Only if you have a v3 workload kit you trust at `./<workload>`; this skill
does not supply one. Use a short, canonical scratch workspace on macOS to
avoid Unix socket path limits (for example, `mktemp -d /tmp/kit-v3.XXXXXX`,
then resolve it with `pwd -P`). Initialize network policy only for the isolated
app, for example with `sbx --app-name "$APP" daemon start --detach --policy balanced`.

```bash
sbx --app-name "$APP" run ./<workload> --kit "$WORK/extra-egress" \
  --detach --name kit-v3-check "$WORK/workspace"
sbx --app-name "$APP" policy check network --sandbox kit-v3-check registry.npmjs.org
```
Use a workload stem that does not collide with an installed built-in agent:
v0.50.1 rejects a local workload named `shell`; a disposable copy named
`kit-probe/kit-probe.yaml` plus `kit-probe.dockerfile` avoids that collision.
The supplied mixin keeps its explanatory `agent-context@2` optional because
v0.50.1 does not support that capability at composition time. Hosts may omit
the note; the network request remains required.

Observe and record the decision. Do not assume the egress request was granted
just because it is declared; the host decides. For a mixin that ships a tool,
run the tool with `sbx exec` (not as an argument after `--` on `sbx run`).

## A8. Clean up (consented removal of only what this runbook created)

```bash
sbx --app-name "$APP" rm --force kit-v3-check   # only if A7 was run
sbx --app-name "$APP" daemon stop               # if any daemon-backed step ran
if [ "${BUILDER_CREATED:-false}" = true ]; then
  if docker buildx rm "$BUILDER"; then
    BUILDER_CREATED=false
  fi
fi
rm -rf "$WORK"
```
Normal A2/A6 may start a daemon even without A7. After confirming it stopped,
remove only this session's app-scoped runtime state. On the tested macOS host:

```bash
STATE_DIR="$HOME/Library/Application Support/com.docker.sandboxes/sandboxes-$APP"
RUN_DIR="$HOME/.sbx/run_$APP"
FALLBACK_ALIAS="/tmp/sboxd-$(id -u)-sandboxes-$APP"
# Verify these paths name only this session before removing them.
rm -rf "$STATE_DIR" "$RUN_DIR" "$FALLBACK_ALIAS"
```

Verify these paths are absent and no process for `sandboxes-$APP` remains.
Resolve platform-specific paths before using this on another OS. Never remove
the default app's state. This does not remove the isolated keychain sign-in;
coordinate logout separately with the operator.

The builder name is unique to this run. Do not remove a builder you did not
create, and do not substitute `docker buildx prune`, `docker system prune`,
or any unscoped removal.
