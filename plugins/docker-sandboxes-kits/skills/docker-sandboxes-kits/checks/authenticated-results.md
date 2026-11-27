# Authenticated v3 verification — 2026-11-02

## Final verdict

**Composition and runtime connectivity passed on sbx v0.50.1 after correcting
the mixin's capability requirement.** No Sandboxes code or installed binary
was changed. The original failures are retained below.

| Step | Original expectation | Actual result / corrected expectation |
| --- | --- | --- |
| A1 | Isolated builder and scratch | Pass on each attempt; reused only the explicitly authenticated app `kit-v3-1102`. |
| A2 | Prints both typed capability names | Original expectation fails: normal inspect succeeds but shows a legacy-shaped summary. JSON includes the npm allow list, not raw capability declarations. Corrected A2 passes. |
| A3 | cacheonly succeeds | Pass on corrected asset. |
| A4 | TCK reports no failures | Pass: 19 checks, 19 passed. TCK descriptor inspection prints both capability types and optional context. |
| A5 | Unknown `capabilites` fails | Pass: expected exit 1 names the misspelled field. |
| A6 | Normal validate must fail | Original expectation contradicted: normal validation exits 0, `valid (directory)`. Offline exits 1 by design. Corrected A6 passes. |
| A7 | Compose and observe host decision | Initially failed on required `agent-context@2`, then on workload name collision. After fixes, sandbox starts; policy allows npm:443; curl returns HTTP 200. |
| A8 | Remove only test resources | Pass: sandbox, three named builders, all scratch directories, isolated daemon and app runtime state removed. |

## Versions and fixture

- macOS arm64; installed `/opt/homebrew/bin/sbx` v0.50.1,
  revision `ddb0268d7124b9cf98955d0b08ffd71a0dfcebe4`.
- Docker client/engine 29.9.1 / Desktop 4.96.0; Buildx v0.38.0,
  revision `0dbe87f36ed472fe36b6796c3f70b4210a731fc5`.
- TCK commit `4d932451613f8df89c8468e2bb7c5286882897ca`, Go module version
  `v3.0.0-m.11.0.20261031103226-4d932451613f`, Go 1.26.10.
  The version command prints `dev`; build metadata retains the pin.
- Kit frontend `3.0.0-m.11 (92835bb7)`:
  `sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805`.
- Trusted fixture: `tests/e2e/kits/testdata/shell` in the operator's Sandboxes
  checkout `aaa96b72111a83a8326419630ab6ad18c0fde0c5`. A disposable copy pins
  `docker.io/sbx/shell-docker-image` to index digest
  `sha256:6c84996b07b743154fc8f26c662b642cee8fb6dd410803b2c40d5d3a537c838d`
  and renames the companion pair to `kit-probe/kit-probe.yaml` and
  `kit-probe/kit-probe.dockerfile`. Its only capability is `sbx@1`; entrypoint
  is `sh`. The source checkout was not modified.

## Corrections and limits

1. `--app-name` isolates credentials. The operator explicitly signed in to
   the test app. Offline is not a workaround: it deliberately omits the v3
   builder. Both normal inspect and validate build/import through the daemon.
2. v0.50.1 uses `newKitV2View` for inspect JSON even for v3. Its output is a
   projection, not authoring YAML. TCK descriptor inspection is the verified
   way to see the raw typed requests in the exported layout.
3. Validation does not select all required capabilities for composition.
   The original asset validated but failed to run because v0.50.1 does not
   support required `agent-context@2`. The note is explanatory, so the asset
   now marks only that capability `optional: true`. Network policy remains
   required. Delivery of the optional note is **not** verified on this host.
4. A local workload named `shell` collides with v0.50.1's built-in agent.
   Renaming only the disposable fixture avoids it. Use `--detach`, not the
   runbook's earlier `--detached` spelling.
5. The successful test used the isolated app's balanced policy. Policy check
   reported "Allowed" and "Local policy only"; policy listing also reported
   managed governance. We record both outputs without generalizing governance
   semantics. HTTP 200 confirms connectivity, **not** that the mixin alone
   granted access: existing package-registry rules may also permit it. No
   differential deny/allow control or security-boundary test was performed.
6. The shipped descriptor is readable at
   `/usr/share/sandbox/kit/extra-egress/kit.yaml`, and exec ran as uid 1000.
   No arbitrary tool-overlay, cloud, publication, signing or other capability
   behavior is established by this test.
7. Cleanup removed 3.2 GiB of this app's runtime state after stopping its
   daemon. No default daemon/state was touched. The operator-created isolated
   keychain sign-in is preserved (no logout). Standard Go/download caches and
   Docker's shared builder image may remain; no global prune ran.

## Commands and output

The three transcripts below retain failures and exit codes. `$WORK` replaces
each run's generated short canonical temp directory, `$SKILLS_REPO` and
`$SANDBOXES_REPO` replace checkout paths, and `$HOME` replaces the home path.
The managed policy identifier is redacted. After the passing run, the asset's
verification-status comment was updated; descriptor fields are unchanged. Each attempt used one zsh process:

```sh
unset DOCKER_CLI_PLUGIN_ORIGINAL_CLI_COMMAND DOCKER_CLI_PLUGIN_SOCKET
export NO_COLOR=1 BUILDKIT_PROGRESS=plain
APP=kit-v3-1102
WORK=$(mktemp -d /tmp/kit-v3.XXXXXX)
WORK=$(cd "$WORK" && pwd -P)
BUILDER="kit-live-$$"
export BUILDX_BUILDER="$BUILDER"
# Capture each exit code; continue expected failures; EXIT trap performs A8.
# Select the scratch TCK after installation: export PATH="$WORK/bin:$PATH"
```

Build commands with context `.` ran in `$WORK/extra-egress` or `$WORK/typo`
as appropriate. Other commands use absolute paths. The first two attempts
aborted A7 before sandbox creation, so their cleanup reports "not found";
the final attempt successfully removes the running sandbox. Only the last
run reaches the policy, HTTP and in-sandbox descriptor checks.

## Attempt 1: original required context

```text
UTC: 2026-11-02T16:00:47Z
APP=kit-v3-1102
WORK=$WORK
BUILDER=kit-live-26464

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 version
sbx version v0.50.1 ddb0268d7124b9cf98955d0b08ffd71a0dfcebe4
[exit 0]

$ docker buildx version
github.com/docker/buildx v0.38.0 0dbe87f36ed472fe36b6796c3f70b4210a731fc5
[exit 0]

$ mkdir $WORK/extra-egress $WORK/shell $WORK/workspace
[exit 0]

$ cp $SKILLS_REPO/skills/docker-sandboxes-kits/assets/v3-mixin-egress.yaml $WORK/extra-egress/extra-egress.yaml
[exit 0]

$ cp $SANDBOXES_REPO/tests/e2e/kits/testdata/shell/shell.yaml $WORK/shell/shell.yaml
[exit 0]

$ python3 -c from\ pathlib\ import\ Path\;\ import\ sys\;\ p=Path\(sys.argv\[1\]\)\;\ Path\(sys.argv\[2\]\).write_text\(p.read_text\(\).replace\(\"docker.io/sbx/shell-docker-image:latest\",\ \"docker.io/sbx/shell-docker-image@sha256:6c84996b07b743154fc8f26c662b642cee8fb6dd410803b2c40d5d3a537c838d\"\)\) $SANDBOXES_REPO/tests/e2e/kits/testdata/shell/shell.dockerfile $WORK/shell/shell.dockerfile
[exit 0]

$ cat $WORK/shell/shell.yaml $WORK/shell/shell.dockerfile
# syntax=docker/sandbox-kit:3
schemaVersion: "3"
kind: workload
description: Shell workload for shortcut selection and reattachment.
capabilities:
  - type: com.docker.sandbox/sbx@1
# syntax=docker/dockerfile:1
FROM docker.io/sbx/shell-docker-image@sha256:6c84996b07b743154fc8f26c662b642cee8fb6dd410803b2c40d5d3a537c838d
ENTRYPOINT ["sh"]
[exit 0]

$ docker buildx create --name kit-live-26464 --driver docker-container --bootstrap
#1 [internal] booting buildkit
#1 pulling image moby/buildkit:buildx-stable-1
#1 pulling image moby/buildkit:buildx-stable-1 1.0s done
#1 creating container buildx_buildkit_kit-live-264640
#1 creating container buildx_buildkit_kit-live-264640 0.4s done
#1 DONE 1.4s
kit-live-26464
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 daemon start --detach --policy balanced
  ✓ daemon — started (PID 26490)
      socket $HOME/.sbx/run_kit-v3-1102/d/sandboxd.sock
      logs $HOME/Library/Application Support/com.docker.sandboxes/sandboxes-kit-v3-1102/sandboxd/daemon.log
[exit 0]

=== A2 normal inspection ===

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 kit inspect $WORK/extra-egress

KITS
  ○ $WORK/extra-egress — building…
  ✓ $WORK/extra-egress — built (7s)
      sbx-kit-src:extra-egress-e50b7db3b40b

  Name:         extra-egress
  Kind:         mixin
  Schema:       v3
  Display:      Extra egress
  Description:  Requests runtime egress to the npm registry and says so to the agent.
  Template:     sbx-kit-src:extra-egress-e50b7db3b40b
  Policies:
    Network:    1 allow, 0 deny
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 kit inspect $WORK/extra-egress --format json

KITS
  ✓ $WORK/extra-egress — cached
      sbx-kit-src:extra-egress-e50b7db3b40b
{
  "schemaVersion": "3",
  "kind": "mixin",
  "name": "extra-egress",
  "displayName": "Extra egress",
  "description": "Requests runtime egress to the npm registry and says so to the agent.",
  "sandbox": {
    "image": "sbx-kit-src:extra-egress-e50b7db3b40b"
  },
  "permissions": {
    "network": {
      "allow": [
        "registry.npmjs.org"
      ]
    }
  }
}
[exit 0]

=== A6 normal and offline validation ===

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 kit validate $WORK/extra-egress

KITS
  ✓ $WORK/extra-egress — cached
      sbx-kit-src:extra-egress-e50b7db3b40b
  ✓ $WORK/extra-egress — valid (directory)
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 kit validate $WORK/extra-egress --offline
error: kit $WORK/extra-egress is a v3 source kit and this load path has no kit builder configured; artifact validation failed
[exit 1]

=== A7 runtime composition ===

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 run $WORK/shell --kit $WORK/extra-egress --detach --name kit-v3-check --cpus 2 --memory 2g $WORK/workspace

KITS
  ○ $WORK/shell — building…
  ✓ $WORK/shell — built (49s)
      sbx-kit-src:shell-884aec520dce
  ✓ $WORK/extra-egress — cached
      sbx-kit-src:extra-egress-e50b7db3b40b
error: resolve kits: $WORK/extra-egress:1:269: capabilities[1]: required capability selection rejected (item capabilities[1]); original source $WORK/extra-egress capabilities[1]; unsupported capability type com.docker.sandbox/agent-context@2   | 1 | {"schemaVersion":"3","displayName":"Extra egress","description":"Requests runtime egress to the npm registry and says so to the agent.","kind":"mixin","capabilities":[{"type":"com.docker.sandbox/network-policy@1","config":{"runtime":{"allow":["registry.npmjs.org"]}}},{"type":"com.docker.sandbox/agent-context@2","config":{"content":"This kit requests runtime egress to registry.npmjs.org. The host decides whether the request is granted."}}]}   |                                                                                                                                                                                                                                                                             ^
[exit 1]

=== A8 cleanup ===

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 rm --force kit-v3-check
error: sandbox 'kit-v3-check' not found
  try: sbx ls
[exit 1]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 daemon stop
Stopped daemon
[exit 0]

$ docker buildx rm kit-live-26464
kit-live-26464 removed
[exit 0]

$ rm -rf $WORK
[exit 0]

$ test ! -e $WORK
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 daemon status
  Status:  stopped
  Socket:  $HOME/.sbx/run_kit-v3-1102/d/sandboxd.sock (not connected)
[exit 0]
```

## Attempt 2: optional context, workload name collision

```text
UTC: 2026-11-02T16:02:23Z
APP=kit-v3-1102
WORK=$WORK
BUILDER=kit-live-26681

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 version
sbx version v0.50.1 ddb0268d7124b9cf98955d0b08ffd71a0dfcebe4
[exit 0]

$ docker buildx version
github.com/docker/buildx v0.38.0 0dbe87f36ed472fe36b6796c3f70b4210a731fc5
[exit 0]

$ mkdir $WORK/extra-egress $WORK/shell $WORK/workspace
[exit 0]

$ cp $SKILLS_REPO/skills/docker-sandboxes-kits/assets/v3-mixin-egress.yaml $WORK/extra-egress/extra-egress.yaml
[exit 0]

$ cp $SANDBOXES_REPO/tests/e2e/kits/testdata/shell/shell.yaml $WORK/shell/shell.yaml
[exit 0]

$ python3 -c from\ pathlib\ import\ Path\;\ import\ sys\;\ p=Path\(sys.argv\[1\]\)\;\ Path\(sys.argv\[2\]\).write_text\(p.read_text\(\).replace\(\"docker.io/sbx/shell-docker-image:latest\",\ \"docker.io/sbx/shell-docker-image@sha256:6c84996b07b743154fc8f26c662b642cee8fb6dd410803b2c40d5d3a537c838d\"\)\) $SANDBOXES_REPO/tests/e2e/kits/testdata/shell/shell.dockerfile $WORK/shell/shell.dockerfile
[exit 0]

$ cat $WORK/shell/shell.yaml $WORK/shell/shell.dockerfile
# syntax=docker/sandbox-kit:3
schemaVersion: "3"
kind: workload
description: Shell workload for shortcut selection and reattachment.
capabilities:
  - type: com.docker.sandbox/sbx@1
# syntax=docker/dockerfile:1
FROM docker.io/sbx/shell-docker-image@sha256:6c84996b07b743154fc8f26c662b642cee8fb6dd410803b2c40d5d3a537c838d
ENTRYPOINT ["sh"]
[exit 0]

$ docker buildx create --name kit-live-26681 --driver docker-container --bootstrap
#1 [internal] booting buildkit
#1 pulling image moby/buildkit:buildx-stable-1
#1 pulling image moby/buildkit:buildx-stable-1 0.9s done
#1 creating container buildx_buildkit_kit-live-266810
#1 creating container buildx_buildkit_kit-live-266810 0.4s done
#1 DONE 1.3s
kit-live-26681
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 daemon start --detach --policy balanced
  ✓ daemon — started (PID 26707)
      socket $HOME/.sbx/run_kit-v3-1102/d/sandboxd.sock
      logs $HOME/Library/Application Support/com.docker.sandboxes/sandboxes-kit-v3-1102/sandboxd/daemon.log
[exit 0]

=== A2 normal inspection ===

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 kit inspect $WORK/extra-egress

KITS
  ○ $WORK/extra-egress — building…
  ✓ $WORK/extra-egress — built (2s)
      sbx-kit-src:extra-egress-53991acf39c0

  Name:         extra-egress
  Kind:         mixin
  Schema:       v3
  Display:      Extra egress
  Description:  Requests runtime egress to the npm registry and says so to the agent.
  Template:     sbx-kit-src:extra-egress-53991acf39c0
  Policies:
    Network:    1 allow, 0 deny
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 kit inspect $WORK/extra-egress --format json

KITS
  ✓ $WORK/extra-egress — cached
      sbx-kit-src:extra-egress-53991acf39c0
{
  "schemaVersion": "3",
  "kind": "mixin",
  "name": "extra-egress",
  "displayName": "Extra egress",
  "description": "Requests runtime egress to the npm registry and says so to the agent.",
  "sandbox": {
    "image": "sbx-kit-src:extra-egress-53991acf39c0"
  },
  "permissions": {
    "network": {
      "allow": [
        "registry.npmjs.org"
      ]
    }
  }
}
[exit 0]

=== A6 normal and offline validation ===

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 kit validate $WORK/extra-egress

KITS
  ✓ $WORK/extra-egress — cached
      sbx-kit-src:extra-egress-53991acf39c0
  ✓ $WORK/extra-egress — valid (directory)
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 kit validate $WORK/extra-egress --offline
error: kit $WORK/extra-egress is a v3 source kit and this load path has no kit builder configured; artifact validation failed
[exit 1]

=== Corrected asset conformance and strict decoding ===

$ mkdir $WORK/bin $WORK/typo
[exit 0]

$ env GOBIN=$WORK/bin go install github.com/docker/sandbox-kit-spec/v3/cmd/kit-tck@4d932451613f8df89c8468e2bb7c5286882897ca
go: github.com/docker/sandbox-kit-spec/v3@v3.0.0-m.11.0.20261031103226-4d932451613f requires go >= 1.26.10; switching to go1.26.10
[exit 0]

$ kit-tck version
dev
[exit 0]

$ go version -m $WORK/bin/kit-tck
$WORK/bin/kit-tck: go1.26.10
	path	github.com/docker/sandbox-kit-spec/v3/cmd/kit-tck
	mod	github.com/docker/sandbox-kit-spec/v3	v3.0.0-m.11.0.20261031103226-4d932451613f	h1:dS5huJIhcyTPidx3Z/+gS6vKwv1N/ttTzJJiXvOnj2U=
	dep	github.com/containerd/log	v0.2.0	h1:BewD/umNgVnoczglOpX8eRMyEy5t5iPlu5AIpnWDONc=
	dep	github.com/containerd/platforms	v1.0.0-rc.5	h1:vXd569rDrz8LeMXzAnBsy6LADV5YtsD8oyaRarxdmSU=
	dep	github.com/distribution/reference	v0.6.0	h1:0IXCQ5g4/QMHHkarYzh5l+u8T3t73zM5QvfrDyIgxBk=
	dep	github.com/klauspost/compress	v1.20.3	h1:zWNoFqq/lSuYQRim3dUXlXeA0IqwuZGicdG5ZTfY5j4=
	dep	github.com/opencontainers/go-digest	v1.0.0	h1:apOUWs51W5PlhuyGyz9FCeeBIOUDA/6nW8Oi/yOhh5U=
	dep	github.com/opencontainers/image-spec	v1.1.1	h1:y0fUlFfIZhPF1W537XOLg0/fcx6zcHCJwooC2xJA040=
	dep	github.com/sirupsen/logrus	v1.10.2	h1:G2SED73/qrAu6YwbdxOD6peLkCBI3z7L+ykJFTXJBBo=
	dep	golang.org/x/crypto	v0.58.0	h1:COkYLr4k7nDI4r6QtMML2AfzeIswWHAJthLS6K/M/54=
	dep	golang.org/x/sync	v0.24.0	h1:iqiDrGoDgyuvAKrhLQthUEzU/R378N78gXbBjxed7oA=
	dep	golang.org/x/sys	v0.49.0	h1:XbzkgYJHdqh/8m2Uu0W/dQv8nktxx4BFHp1M0gROTXA=
	dep	golang.org/x/term	v0.47.0	h1:cpyOwQkr2Nzxe2p6KnrTG7Ei2wtzjsuSjhpXXepZ/BM=
	dep	gopkg.in/yaml.v3	v3.0.1	h1:fxVm/GzAzEWqLHuvctI91KS9hhNmmWOoWu0XTYJS7CA=
	dep	oras.land/oras-go/v2	v2.6.4	h1:l4uv+UT7QK4Hju+KOEZ/c8iOjq3iZH7cULoRpUnSDAU=
	build	-buildmode=exe
	build	-compiler=gc
	build	CGO_ENABLED=1
	build	CGO_CFLAGS=
	build	CGO_CPPFLAGS=
	build	CGO_CXXFLAGS=
	build	CGO_LDFLAGS=
	build	GOARCH=arm64
	build	GOOS=darwin
	build	GOARM64=v8.0
[exit 0]

$ docker buildx build --builder kit-live-26681 . -f extra-egress.yaml --output type=cacheonly
#0 building with "kit-live-26681" instance using docker-container driver

#1 [internal] load build definition from extra-egress.yaml
#1 transferring dockerfile: 937B done
#1 DONE 0.0s

#2 resolve image config for docker-image://docker.io/docker/sandbox-kit:3
#2 DONE 0.2s

#3 docker-image://docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805
#3 resolve docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805 done
#3 CACHED

#4 [internal] load kit descriptor extra-egress.yaml · sandbox-kit 3.0.0-m.11 (92835bb7)
#4 transferring dockerfile: 39B done
#4 DONE 0.0s

#5 [kit] stage sources /usr/share/sandbox/kit/extra-egress
#5 CACHED

View build details: docker-desktop://dashboard/build/kit-live-26681/kit-live-266810/my12u8y0ig64biaq8brjjy0zd
[exit 0]

$ docker buildx build --builder kit-live-26681 . -f extra-egress.yaml -t extra-egress:0.0.0 --output type=oci,dest=$WORK/layout,tar=false
#0 building with "kit-live-26681" instance using docker-container driver

#1 [internal] load build definition from extra-egress.yaml
#1 transferring dockerfile: 937B done
#1 DONE 0.0s

#2 resolve image config for docker-image://docker.io/docker/sandbox-kit:3
#2 DONE 0.2s

#3 docker-image://docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805
#3 resolve docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805 done
#3 CACHED

#4 [internal] load kit descriptor extra-egress.yaml · sandbox-kit 3.0.0-m.11 (92835bb7)
#4 transferring dockerfile: 39B done
#4 DONE 0.0s

#5 [kit] stage sources /usr/share/sandbox/kit/extra-egress
#5 CACHED

#6 exporting to oci image format
#6 exporting layers done
#6 exporting manifest sha256:731ae4ec7a2d7ba09a0576a4c3f7a6fcc493364dc30ea1c048bdbe91a07fc5db done
#6 exporting config sha256:98526907c4ac9bdccc85a81963d9582347b613a8c23e24aee9e7d0367eceb283 done
#6 DONE 0.0s

View build details: docker-desktop://dashboard/build/kit-live-26681/kit-live-266810/pjc85rocit5jtkc69abrdd5if
[exit 0]

$ kit-tck validate --layout $WORK/layout 0.0.0
kit-tck dev · validate · $WORK/layout 0.0.0

  19 checks · 19 passed

✓ conforms
[exit 0]

$ kit-tck inspect --descriptor --layout $WORK/layout 0.0.0
schemaVersion: "3"
displayName: Extra egress
description: Requests runtime egress to the npm registry and says so to the agent.
kind: mixin
capabilities:
  - type: com.docker.sandbox/network-policy@1
    config:
      runtime:
        allow:
          - registry.npmjs.org
  - type: com.docker.sandbox/agent-context@2
    optional: true
    config:
      content: This kit requests runtime egress to registry.npmjs.org. The host decides whether the request is granted.
[exit 0]

$ python3 -c from\ pathlib\ import\ Path\;\ import\ sys\;\ Path\(sys.argv\[2\]\).write_text\(Path\(sys.argv\[1\]\).read_text\(\).replace\(\"capabilities:\",\"capabilites:\",1\)\) $WORK/extra-egress/extra-egress.yaml $WORK/typo/typo.yaml
[exit 0]

$ docker buildx build --builder kit-live-26681 . -f typo.yaml --output type=cacheonly
#0 building with "kit-live-26681" instance using docker-container driver

#1 [internal] load build definition from typo.yaml
#1 transferring dockerfile: 928B done
#1 DONE 0.0s

#2 resolve image config for docker-image://docker.io/docker/sandbox-kit:3
#2 DONE 0.2s

#3 docker-image://docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805
#3 resolve docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805 done
#3 CACHED

#4 [internal] load kit descriptor typo.yaml · sandbox-kit 3.0.0-m.11 (92835bb7)
#4 transferring dockerfile: 928B done
#4 DONE 0.0s
ERROR: failed to build: failed to solve: decode kit descriptor: yaml: unmarshal errors:
  line 10: field capabilites not found in type spec.Descriptor

View build details: docker-desktop://dashboard/build/kit-live-26681/kit-live-266810/fwj4sug32v94ddyhgth6bixaj
[exit 1]

=== A7 runtime composition ===

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 run $WORK/shell --kit $WORK/extra-egress --detach --name kit-v3-check --cpus 2 --memory 2g $WORK/workspace

KITS
  ✓ $WORK/shell — cached
      sbx-kit-src:shell-884aec520dce
  ✓ $WORK/extra-egress — cached
      sbx-kit-src:extra-egress-53991acf39c0
error: agent "shell" is already registered (built-in agents cannot be overridden by a kit)
[exit 1]

=== A8 cleanup ===

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 rm --force kit-v3-check
error: sandbox 'kit-v3-check' not found
  try: sbx ls
[exit 1]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 daemon stop
Stopped daemon
[exit 0]

$ docker buildx rm kit-live-26681
kit-live-26681 removed
[exit 0]

$ rm -rf $WORK
[exit 0]

$ test ! -e $WORK
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 daemon status
  Status:  stopped
  Socket:  $HOME/.sbx/run_kit-v3-1102/d/sandboxd.sock (not connected)
[exit 0]
```

## Attempt 3: corrected mixin and renamed workload

```text
UTC: 2026-11-02T16:02:55Z
APP=kit-v3-1102
WORK=$WORK
BUILDER=kit-live-26938

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 version
sbx version v0.50.1 ddb0268d7124b9cf98955d0b08ffd71a0dfcebe4
[exit 0]

$ docker buildx version
github.com/docker/buildx v0.38.0 0dbe87f36ed472fe36b6796c3f70b4210a731fc5
[exit 0]

$ mkdir $WORK/extra-egress $WORK/kit-probe $WORK/workspace
[exit 0]

$ cp $SKILLS_REPO/skills/docker-sandboxes-kits/assets/v3-mixin-egress.yaml $WORK/extra-egress/extra-egress.yaml
[exit 0]

$ cp $SANDBOXES_REPO/tests/e2e/kits/testdata/shell/shell.yaml $WORK/kit-probe/kit-probe.yaml
[exit 0]

$ python3 -c from\ pathlib\ import\ Path\;\ import\ sys\;\ p=Path\(sys.argv\[1\]\)\;\ Path\(sys.argv\[2\]\).write_text\(p.read_text\(\).replace\(\"docker.io/sbx/shell-docker-image:latest\",\ \"docker.io/sbx/shell-docker-image@sha256:6c84996b07b743154fc8f26c662b642cee8fb6dd410803b2c40d5d3a537c838d\"\)\) $SANDBOXES_REPO/tests/e2e/kits/testdata/shell/shell.dockerfile $WORK/kit-probe/kit-probe.dockerfile
[exit 0]

$ cat $WORK/kit-probe/kit-probe.yaml $WORK/kit-probe/kit-probe.dockerfile
# syntax=docker/sandbox-kit:3
schemaVersion: "3"
kind: workload
description: Shell workload for shortcut selection and reattachment.
capabilities:
  - type: com.docker.sandbox/sbx@1
# syntax=docker/dockerfile:1
FROM docker.io/sbx/shell-docker-image@sha256:6c84996b07b743154fc8f26c662b642cee8fb6dd410803b2c40d5d3a537c838d
ENTRYPOINT ["sh"]
[exit 0]

$ docker buildx create --name kit-live-26938 --driver docker-container --bootstrap
#1 [internal] booting buildkit
#1 pulling image moby/buildkit:buildx-stable-1
#1 pulling image moby/buildkit:buildx-stable-1 0.9s done
#1 creating container buildx_buildkit_kit-live-269380
#1 creating container buildx_buildkit_kit-live-269380 0.4s done
#1 DONE 1.3s
kit-live-26938
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 daemon start --detach --policy balanced
  ✓ daemon — started (PID 26963)
      socket $HOME/.sbx/run_kit-v3-1102/d/sandboxd.sock
      logs $HOME/Library/Application Support/com.docker.sandboxes/sandboxes-kit-v3-1102/sandboxd/daemon.log
[exit 0]

=== A2 normal inspection ===

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 kit inspect $WORK/extra-egress

KITS
  ✓ $WORK/extra-egress — cached
      sbx-kit-src:extra-egress-53991acf39c0

  Name:         extra-egress
  Kind:         mixin
  Schema:       v3
  Display:      Extra egress
  Description:  Requests runtime egress to the npm registry and says so to the agent.
  Template:     sbx-kit-src:extra-egress-53991acf39c0
  Policies:
    Network:    1 allow, 0 deny
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 kit inspect $WORK/extra-egress --format json

KITS
  ✓ $WORK/extra-egress — cached
      sbx-kit-src:extra-egress-53991acf39c0
{
  "schemaVersion": "3",
  "kind": "mixin",
  "name": "extra-egress",
  "displayName": "Extra egress",
  "description": "Requests runtime egress to the npm registry and says so to the agent.",
  "sandbox": {
    "image": "sbx-kit-src:extra-egress-53991acf39c0"
  },
  "permissions": {
    "network": {
      "allow": [
        "registry.npmjs.org"
      ]
    }
  }
}
[exit 0]

=== A6 normal and offline validation ===

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 kit validate $WORK/extra-egress

KITS
  ✓ $WORK/extra-egress — cached
      sbx-kit-src:extra-egress-53991acf39c0
  ✓ $WORK/extra-egress — valid (directory)
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 kit validate $WORK/extra-egress --offline
error: kit $WORK/extra-egress is a v3 source kit and this load path has no kit builder configured; artifact validation failed
[exit 1]

=== Corrected asset conformance and strict decoding ===

$ mkdir $WORK/bin $WORK/typo
[exit 0]

$ env GOBIN=$WORK/bin go install github.com/docker/sandbox-kit-spec/v3/cmd/kit-tck@4d932451613f8df89c8468e2bb7c5286882897ca
go: github.com/docker/sandbox-kit-spec/v3@v3.0.0-m.11.0.20261031103226-4d932451613f requires go >= 1.26.10; switching to go1.26.10
[exit 0]

$ kit-tck version
dev
[exit 0]

$ go version -m $WORK/bin/kit-tck
$WORK/bin/kit-tck: go1.26.10
	path	github.com/docker/sandbox-kit-spec/v3/cmd/kit-tck
	mod	github.com/docker/sandbox-kit-spec/v3	v3.0.0-m.11.0.20261031103226-4d932451613f	h1:dS5huJIhcyTPidx3Z/+gS6vKwv1N/ttTzJJiXvOnj2U=
	dep	github.com/containerd/log	v0.2.0	h1:BewD/umNgVnoczglOpX8eRMyEy5t5iPlu5AIpnWDONc=
	dep	github.com/containerd/platforms	v1.0.0-rc.5	h1:vXd569rDrz8LeMXzAnBsy6LADV5YtsD8oyaRarxdmSU=
	dep	github.com/distribution/reference	v0.6.0	h1:0IXCQ5g4/QMHHkarYzh5l+u8T3t73zM5QvfrDyIgxBk=
	dep	github.com/klauspost/compress	v1.20.3	h1:zWNoFqq/lSuYQRim3dUXlXeA0IqwuZGicdG5ZTfY5j4=
	dep	github.com/opencontainers/go-digest	v1.0.0	h1:apOUWs51W5PlhuyGyz9FCeeBIOUDA/6nW8Oi/yOhh5U=
	dep	github.com/opencontainers/image-spec	v1.1.1	h1:y0fUlFfIZhPF1W537XOLg0/fcx6zcHCJwooC2xJA040=
	dep	github.com/sirupsen/logrus	v1.10.2	h1:G2SED73/qrAu6YwbdxOD6peLkCBI3z7L+ykJFTXJBBo=
	dep	golang.org/x/crypto	v0.58.0	h1:COkYLr4k7nDI4r6QtMML2AfzeIswWHAJthLS6K/M/54=
	dep	golang.org/x/sync	v0.24.0	h1:iqiDrGoDgyuvAKrhLQthUEzU/R378N78gXbBjxed7oA=
	dep	golang.org/x/sys	v0.49.0	h1:XbzkgYJHdqh/8m2Uu0W/dQv8nktxx4BFHp1M0gROTXA=
	dep	golang.org/x/term	v0.47.0	h1:cpyOwQkr2Nzxe2p6KnrTG7Ei2wtzjsuSjhpXXepZ/BM=
	dep	gopkg.in/yaml.v3	v3.0.1	h1:fxVm/GzAzEWqLHuvctI91KS9hhNmmWOoWu0XTYJS7CA=
	dep	oras.land/oras-go/v2	v2.6.4	h1:l4uv+UT7QK4Hju+KOEZ/c8iOjq3iZH7cULoRpUnSDAU=
	build	-buildmode=exe
	build	-compiler=gc
	build	CGO_ENABLED=1
	build	CGO_CFLAGS=
	build	CGO_CPPFLAGS=
	build	CGO_CXXFLAGS=
	build	CGO_LDFLAGS=
	build	GOARCH=arm64
	build	GOOS=darwin
	build	GOARM64=v8.0
[exit 0]

$ docker buildx build --builder kit-live-26938 . -f extra-egress.yaml --output type=cacheonly
#0 building with "kit-live-26938" instance using docker-container driver

#1 [internal] load build definition from extra-egress.yaml
#1 transferring dockerfile: 937B done
#1 DONE 0.0s

#2 resolve image config for docker-image://docker.io/docker/sandbox-kit:3
#2 ...

#3 [auth] docker/sandbox-kit:pull token for registry-1.docker.io
#3 DONE 0.0s

#2 resolve image config for docker-image://docker.io/docker/sandbox-kit:3
#2 DONE 1.2s

#4 docker-image://docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805
#4 resolve docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805 done
#4 sha256:e82cb93883f6d13d4487a7059dded45fd79fdec4147dfc96d597285c8b5cca38 0B / 6.70MB 0.2s
#4 sha256:e82cb93883f6d13d4487a7059dded45fd79fdec4147dfc96d597285c8b5cca38 1.05MB / 6.70MB 0.6s
#4 sha256:e82cb93883f6d13d4487a7059dded45fd79fdec4147dfc96d597285c8b5cca38 2.10MB / 6.70MB 0.9s
#4 sha256:e82cb93883f6d13d4487a7059dded45fd79fdec4147dfc96d597285c8b5cca38 3.15MB / 6.70MB 1.4s
#4 sha256:e82cb93883f6d13d4487a7059dded45fd79fdec4147dfc96d597285c8b5cca38 4.19MB / 6.70MB 1.7s
#4 sha256:e82cb93883f6d13d4487a7059dded45fd79fdec4147dfc96d597285c8b5cca38 5.24MB / 6.70MB 2.1s
#4 sha256:e82cb93883f6d13d4487a7059dded45fd79fdec4147dfc96d597285c8b5cca38 6.29MB / 6.70MB 2.4s
#4 sha256:e82cb93883f6d13d4487a7059dded45fd79fdec4147dfc96d597285c8b5cca38 6.70MB / 6.70MB 2.5s done
#4 extracting sha256:e82cb93883f6d13d4487a7059dded45fd79fdec4147dfc96d597285c8b5cca38 0.1s done
#4 DONE 2.6s

#5 [internal] load kit descriptor extra-egress.yaml · sandbox-kit 3.0.0-m.11 (92835bb7)
#5 transferring dockerfile: 937B done
#5 DONE 0.0s

#6 [kit] stage sources /usr/share/sandbox/kit/extra-egress
#6 DONE 0.0s

View build details: docker-desktop://dashboard/build/kit-live-26938/kit-live-269380/c9l2bydydlduvo1zscryojtiq
[exit 0]

$ docker buildx build --builder kit-live-26938 . -f extra-egress.yaml -t extra-egress:0.0.0 --output type=oci,dest=$WORK/layout,tar=false
#0 building with "kit-live-26938" instance using docker-container driver

#1 [internal] load build definition from extra-egress.yaml
#1 transferring dockerfile: 937B done
#1 DONE 0.0s

#2 resolve image config for docker-image://docker.io/docker/sandbox-kit:3
#2 DONE 0.2s

#3 docker-image://docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805
#3 resolve docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805 done
#3 CACHED

#4 [internal] load kit descriptor extra-egress.yaml · sandbox-kit 3.0.0-m.11 (92835bb7)
#4 transferring dockerfile: 39B done
#4 DONE 0.0s

#5 [kit] stage sources /usr/share/sandbox/kit/extra-egress
#5 CACHED

#6 exporting to oci image format
#6 exporting layers 0.0s done
#6 exporting manifest sha256:b45820c1c7cfc2cd6c8c10b46dc26bd0f427f20786fbd2b87fbb75ca99ab6832 done
#6 exporting config sha256:dcb9a44b48756814f2edca2bf71147996c18784a65755557bc7902e9d98d8b13 done
#6 DONE 0.1s

View build details: docker-desktop://dashboard/build/kit-live-26938/kit-live-269380/r593fau2jbcwud213rgvm0zam
[exit 0]

$ kit-tck validate --layout $WORK/layout 0.0.0
kit-tck dev · validate · $WORK/layout 0.0.0

  19 checks · 19 passed

✓ conforms
[exit 0]

$ kit-tck inspect --descriptor --layout $WORK/layout 0.0.0
schemaVersion: "3"
displayName: Extra egress
description: Requests runtime egress to the npm registry and says so to the agent.
kind: mixin
capabilities:
  - type: com.docker.sandbox/network-policy@1
    config:
      runtime:
        allow:
          - registry.npmjs.org
  - type: com.docker.sandbox/agent-context@2
    optional: true
    config:
      content: This kit requests runtime egress to registry.npmjs.org. The host decides whether the request is granted.
[exit 0]

$ python3 -c from\ pathlib\ import\ Path\;\ import\ sys\;\ Path\(sys.argv\[2\]\).write_text\(Path\(sys.argv\[1\]\).read_text\(\).replace\(\"capabilities:\",\"capabilites:\",1\)\) $WORK/extra-egress/extra-egress.yaml $WORK/typo/typo.yaml
[exit 0]

$ docker buildx build --builder kit-live-26938 . -f typo.yaml --output type=cacheonly
#0 building with "kit-live-26938" instance using docker-container driver

#1 [internal] load build definition from typo.yaml
#1 transferring dockerfile: 928B done
#1 DONE 0.0s

#2 resolve image config for docker-image://docker.io/docker/sandbox-kit:3
#2 DONE 0.3s

#3 docker-image://docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805
#3 resolve docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805 done
#3 CACHED

#4 [internal] load kit descriptor typo.yaml · sandbox-kit 3.0.0-m.11 (92835bb7)
#4 transferring dockerfile: 928B done
#4 DONE 0.0s
ERROR: failed to build: failed to solve: decode kit descriptor: yaml: unmarshal errors:
  line 10: field capabilites not found in type spec.Descriptor

View build details: docker-desktop://dashboard/build/kit-live-26938/kit-live-269380/c5j2nrmc8uw2dmtrtctdfvvsz
[exit 1]

=== A7 runtime composition ===

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 run $WORK/kit-probe --kit $WORK/extra-egress --detach --name kit-v3-check --cpus 2 --memory 2g $WORK/workspace

KITS
  ○ $WORK/kit-probe — building…
  ✓ $WORK/kit-probe — built (4m31s)
      sbx-kit-src:kit-probe-6f3084bb320f
  ✓ $WORK/extra-egress — cached
      sbx-kit-src:extra-egress-53991acf39c0

SANDBOX
  Name:       kit-v3-check
  Agent:      kit-probe
  Kits:       $WORK/kit-probe
              $WORK/extra-egress
  Workspace:  $WORK/workspace (rw)
  Image:      sbx-kit-src:kit-probe-6f3084bb320f
  CPU:        2
  Memory:     2g

IMAGE
  ○ image — checking…
  ✓ image — ready

AGENT
    assembling kit image from 2 kits
    pulling kit image $WORK/extra-egress
  ✓ assembled kit image (19 layers)

  ✓ Created sandbox kit-v3-check

  ✓ sandbox kit-v3-check — running detached
      workspace $WORK/workspace
c897aa43-4036-481f-b70a-90d00fbc477a
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 policy check network --sandbox kit-v3-check registry.npmjs.org
  Allowed:     registry.npmjs.org:443
  Governance:  Local policy only
  Context:     sandbox:kit-v3-check
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 policy ls kit-v3-check
  Policy for sandbox:  kit-v3-check
Governance: Managed by docker · Sync: OK, last synced 17:07:59


NETWORK
  • allow 196 hosts from [managed-policy-id], local-policy

FILESYSTEM
  • read allow all paths from local-policy
  • write allow all paths from local-policy

[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 exec kit-v3-check curl --max-time 30 --silent --show-error --output /dev/null --write-out HTTP\ %\{http_code\}\\n https://registry.npmjs.org/
HTTP 200
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 exec kit-v3-check sh -c id\;\ ls\ /usr/share/sandbox/kit\;\ cat\ /usr/share/sandbox/kit/extra-egress/kit.yaml
uid=1000(agent) gid=1000(agent) groups=1000(agent),27(sudo),1001(docker)
extra-egress
kit-probe
# syntax=docker/sandbox-kit:3
# Complete declaration-only v3 mixin. Save it as <kit>/<kit>.yaml (for example
# extra-egress/extra-egress.yaml). It ships no content, so it needs no companion
# <kit>.dockerfile. Build and conformance tested; runtime grants remain untested.
# Recheck on your tools before relying on it (see checks/verification.md).
schemaVersion: "3"
kind: mixin
displayName: Extra egress
description: Requests runtime egress to the npm registry and says so to the agent.
capabilities:
    - type: com.docker.sandbox/network-policy@1
      config:
        runtime:
            allow: [registry.npmjs.org]
    - type: com.docker.sandbox/agent-context@2
      # Explanatory only: older hosts may omit this note, but not the network request.
      optional: true
      config:
        content: This kit requests runtime egress to registry.npmjs.org. The host decides whether the request is granted.
[exit 0]

=== A8 cleanup ===

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 rm --force kit-v3-check
Removed sandbox kit-v3-check
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 daemon stop
Stopped daemon
[exit 0]

$ docker buildx rm kit-live-26938
kit-live-26938 removed
[exit 0]

$ rm -rf $WORK
[exit 0]

$ test ! -e $WORK
[exit 0]

$ /opt/homebrew/bin/sbx --app-name kit-v3-1102 daemon status
  Status:  stopped
  Socket:  $HOME/.sbx/run_kit-v3-1102/d/sandboxd.sock (not connected)
[exit 0]
```

## Final app-scoped cleanup

```text
Scoped cleanup after daemon stop (credentials preserved; no logout)
$ du -sh $HOME/Library/Application\ Support/com.docker.sandboxes/sandboxes-kit-v3-1102
3.2G	$HOME/Library/Application Support/com.docker.sandboxes/sandboxes-kit-v3-1102
$ pgrep -lf sandboxes-kit-v3-1102
[exit 1; 1 means no matching process]
$ rm -rf $HOME/Library/Application\ Support/com.docker.sandboxes/sandboxes-kit-v3-1102 $HOME/.sbx/run_kit-v3-1102 /tmp/sboxd-501-sandboxes-kit-v3-1102
PASS: absent: $HOME/Library/Application Support/com.docker.sandboxes/sandboxes-kit-v3-1102
PASS: absent: $HOME/.sbx/run_kit-v3-1102
PASS: absent: /tmp/sboxd-501-sandboxes-kit-v3-1102
$ docker ps --filter name=kit-live- --format {{.Names}}
```
