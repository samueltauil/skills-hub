# Manual v3 verification — 2026-11-02

## Superseded by authenticated verification

This is the initial unauthenticated transcript, retained as historical evidence.
The [authenticated follow-up](authenticated-results.md) records successful
inspection/validation and runtime composition after making explanatory context
optional and renaming the test workload. The original A2 output expectation
and A6 mandatory-failure expectation were wrong; neither should be used as a
current acceptance criterion. See the corrected runbook and follow-up verdict.

## Scope and verdict

Ran A1-A6 and A8 from `skills/docker-sandboxes-kits` on macOS arm64.
A7 was skipped: no trusted v3 workload was supplied. **Build and layout
conformance passed; source inspection failed; runtime behavior is unverified.**
The prerequisite of a working v3 source-inspection path was not met on the
installed stable CLI. Buildx/TCK checks are independent of that limitation.

| Step | Result against runbook | Observation |
| --- | --- | --- |
| A1 | Pass | Created a unique container builder and scratch directory. |
| A2 | Fail | Normal inspect requires sign-in in the isolated app. Offline retry recognizes v3 but fails with `no kit builder configured`; no capabilities printed. |
| A3 | Pass | `cacheonly` build succeeds. |
| A4 | Pass | OCI directory export succeeds; bare-tag TCK validation reports 19 checks, 19 passed. |
| A5 | Pass (expected failure) | Exit 1 names unknown field `capabilites`. |
| A6 | Pass with qualification | Normal command exits 1 for sign-in, which is inconclusive. Offline retry exits 1 explicitly rejecting the v3 source load path. |
| A7 | Skipped | No composition, effective host-policy decision, or runtime egress test. |
| A8 | Pass | Removed only the run's builder and scratch directory; confirmed scratch removal and builder absence. |

## Versions and reproducibility

- Skill checkout HEAD before edits: `f571e99312b6880cf2c09a87fef7cdd43f84d887`.
- `sbx v0.50.1`, revision `ddb0268d7124b9cf98955d0b08ffd71a0dfcebe4`.
- Buildx `v0.38.0`, revision `0dbe87f36ed472fe36b6796c3f70b4210a731fc5`.
- Docker client/engine `29.9.1`, Docker Desktop `4.96.0 (243774)`.
- TCK installed into scratch `GOBIN` from commit
  `4d932451613f8df89c8468e2bb7c5286882897ca`. `kit-tck version` prints `dev`;
  `go version -m` identifies module version
  `v3.0.0-m.11.0.20261031103226-4d932451613f`, built with Go `1.26.10`.
- Frontend `docker/sandbox-kit:3` resolved to
  `sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805`,
  reporting `sandbox-kit 3.0.0-m.11 (92835bb7)`.
- Ran once on the original asset, then again after changing only its comment
  from "unexecuted" to the observed verification status. Results matched.
  The transcript below is the second run, including its asset SHA-256.

## Surprises and limits

1. Inherited `DOCKER_CLI_PLUGIN_ORIGINAL_CLI_COMMAND` and
   `DOCKER_CLI_PLUGIN_SOCKET` caused `sbx version` to print Docker plugin help,
   and `sbx --app-name ...` to reject that flag. Unsetting these variables in
   the test shell exposed the standalone CLI. No installed tool was replaced.
2. A2 did not reach authenticated source inspection. `--offline` bypasses daemon-backed policy, not the loader;
   it fails even for this declaration-only mixin. No successful inspection
   release or minimum runtime version was established. No sign-in attempted.
3. A6 demonstrates offline rejection only, not rejection by normal validate. An auth failure
   alone would not substantiate the claim. Future releases must be rechecked.
4. A pinned Go installation still reports TCK version `dev`; build metadata
   records the actual pin. Go downloaded the required toolchain automatically.
5. The runbook does access registries to pull the builder/frontend, but
   publishes and signs nothing. Successful pull using the existing Docker
   configuration does not prove anonymous availability.
6. Final `buildx ls` reported unavailable sockets for four pre-existing,
   unrelated builders. These were not used, repaired, or removed. Their names
   and paths below are replaced with placeholders for publication.
7. Scratch included the TCK binary and OCI layout and was deleted. Standard
   Go download caches and the builder image pulled into Docker may remain;
   no global cache or image pruning was performed. No sandbox was created.

## Commands and output

Transcript normalization: `$WORK` replaces the generated absolute temporary
path and `$HOME` replaces the operator's home directory. Other output, including
failures and exit codes, is retained, except the unrelated builder identifiers
noted above. Commands ran in one zsh process. A3/A4 build commands ran in
`$WORK/extra-egress`; A5's build ran in `$WORK/typo`, each in a subshell.
Other commands ran from the skill directory. Setup and logging wrapper:

```sh
unset DOCKER_CLI_PLUGIN_ORIGINAL_CLI_COMMAND DOCKER_CLI_PLUGIN_SOCKET
export NO_COLOR=1 BUILDKIT_PROGRESS=plain
cd skills/docker-sandboxes-kits
APP="k-$(date +%s)-$$"
BUILDER="kit-eval-$$"
WORK=$(mktemp -d)
# kit-tck is installed below into $WORK/bin, then selected with:
export PATH="$WORK/bin:$PATH"
# Each command's status is captured so expected failures do not stop the run.
# An EXIT trap removes the named builder and scratch directory (A8).
```

```text
UTC: 2026-11-02T15:38:58Z
APP=k-1793633938-25255
BUILDER=kit-eval-25255
WORK=$WORK
Environment: unset DOCKER_CLI_PLUGIN_ORIGINAL_CLI_COMMAND DOCKER_CLI_PLUGIN_SOCKET; NO_COLOR=1 BUILDKIT_PROGRESS=plain

$ git rev-parse HEAD
f571e99312b6880cf2c09a87fef7cdd43f84d887
[exit 0]

$ sbx --app-name k-1793633938-25255 version
sbx version v0.50.1 ddb0268d7124b9cf98955d0b08ffd71a0dfcebe4
[exit 0]

$ docker buildx version
github.com/docker/buildx v0.38.0 0dbe87f36ed472fe36b6796c3f70b4210a731fc5
[exit 0]

$ docker version
Client:
 Version:           29.9.1
 API version:       1.56
 Go version:        go1.26.9
 Git commit:        dfc520d
 Built:             Wed Oct 14 18:31:22 2026
 OS/Arch:           darwin/arm64
 Context:           desktop-linux

Server: Docker Desktop 4.96.0 (243774)
 Engine:
  Version:          29.9.1
  API version:      1.56 (minimum version 1.40)
  Go version:       go1.26.9
  Git commit:       b26fb77
  Built:            Wed Oct 14 18:31:50 2026
  OS/Arch:          linux/arm64
  Experimental:     false
 containerd:
  Version:          v2.4.2
  GitCommit:        b7a25261e029d68978bbf290df0a62fc819b3c51
 runc:
  Version:          1.5.2
  GitCommit:        v1.5.2-0-g29dd3dc2
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
[exit 0]

=== A1: scratch resources ===

$ mkdir $WORK/extra-egress $WORK/workspace $WORK/bin
[exit 0]

$ cp assets/v3-mixin-egress.yaml $WORK/extra-egress/extra-egress.yaml
[exit 0]

$ shasum -a 256 assets/v3-mixin-egress.yaml
f82813e8ac7fb6adb268e05969930b64c1109f8e8022a2a5d11710006605a6e5  assets/v3-mixin-egress.yaml
[exit 0]

$ docker buildx create --name kit-eval-25255 --driver docker-container --bootstrap
#1 [internal] booting buildkit
#1 pulling image moby/buildkit:buildx-stable-1
#1 pulling image moby/buildkit:buildx-stable-1 0.9s done
#1 creating container buildx_buildkit_kit-eval-252550
#1 creating container buildx_buildkit_kit-eval-252550 0.4s done
#1 DONE 1.3s
kit-eval-25255
[exit 0]

=== Install pinned kit-tck (isolated GOBIN) ===

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

=== A2: inspect ===

$ sbx --app-name k-1793633938-25255 kit inspect $WORK/extra-egress
error: not signed in to Docker
  try: sbx login
[exit 1]

=== A2 diagnostic: bypass daemon policy, not descriptor decoding ===

$ sbx --app-name k-1793633938-25255 kit inspect $WORK/extra-egress --offline
error: kit $WORK/extra-egress is a v3 source kit and this load path has no kit builder configured
[exit 1]

=== A3: cacheonly ===

$ docker buildx build --builder kit-eval-25255 . -f extra-egress.yaml --output type=cacheonly
#0 building with "kit-eval-25255" instance using docker-container driver

#1 [internal] load build definition from extra-egress.yaml
#1 transferring dockerfile: 833B done
#1 DONE 0.0s

#2 resolve image config for docker-image://docker.io/docker/sandbox-kit:3
#2 ...

#3 [auth] docker/sandbox-kit:pull token for registry-1.docker.io
#3 DONE 0.0s

#2 resolve image config for docker-image://docker.io/docker/sandbox-kit:3
#2 DONE 1.1s

#4 docker-image://docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805
#4 resolve docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805 done
#4 sha256:e82cb93883f6d13d4487a7059dded45fd79fdec4147dfc96d597285c8b5cca38 2.10MB / 6.70MB 0.2s
#4 sha256:e82cb93883f6d13d4487a7059dded45fd79fdec4147dfc96d597285c8b5cca38 6.70MB / 6.70MB 0.2s done
#4 extracting sha256:e82cb93883f6d13d4487a7059dded45fd79fdec4147dfc96d597285c8b5cca38 0.1s done
#4 DONE 0.3s

#5 [internal] load kit descriptor extra-egress.yaml · sandbox-kit 3.0.0-m.11 (92835bb7)
#5 transferring dockerfile: 833B done
#5 DONE 0.0s

#6 [kit] stage sources /usr/share/sandbox/kit/extra-egress
#6 DONE 0.0s

View build details: docker-desktop://dashboard/build/kit-eval-25255/kit-eval-252550/czg4g4jo2ewbyfzl8vj9zg6br
[exit 0]

=== A4: export and conformance ===

$ docker buildx build --builder kit-eval-25255 . -f extra-egress.yaml -t extra-egress:0.0.0 --output type=oci,dest=$WORK/layout,tar=false
#0 building with "kit-eval-25255" instance using docker-container driver

#1 [internal] load build definition from extra-egress.yaml
#1 transferring dockerfile: 833B done
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
#6 exporting manifest sha256:621196cc8dc9f041a5cd3e5949a4f9db1aea1c5d517ea0ebd8b71953d9cf71ff done
#6 exporting config sha256:a029f184270ed55685e9f87024c9843fe1bb9bf7dfe8bd40d4bbea8b46529c15 done
#6 DONE 0.1s

View build details: docker-desktop://dashboard/build/kit-eval-25255/kit-eval-252550/hxq7xdrqsyucvrlqy7k4uo93r
[exit 0]

$ kit-tck validate --layout $WORK/layout 0.0.0
kit-tck dev · validate · $WORK/layout 0.0.0

  19 checks · 19 passed

✓ conforms
[exit 0]

=== A5: misspelled key ===

$ mkdir $WORK/typo
[exit 0]

$ python3 -c import\ pathlib,sys\;\ src=pathlib.Path\(sys.argv\[1\]\).read_text\(\)\;\ pathlib.Path\(sys.argv\[2\]\).write_text\(src.replace\(\"capabilities:\",\ \"capabilites:\",\ 1\)\) $WORK/extra-egress/extra-egress.yaml $WORK/typo/typo.yaml
[exit 0]

$ docker buildx build --builder kit-eval-25255 . -f typo.yaml --output type=cacheonly
#0 building with "kit-eval-25255" instance using docker-container driver

#1 [internal] load build definition from typo.yaml
#1 transferring dockerfile: 824B done
#1 DONE 0.0s

#2 resolve image config for docker-image://docker.io/docker/sandbox-kit:3
#2 DONE 0.2s

#3 docker-image://docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805
#3 resolve docker.io/docker/sandbox-kit:3@sha256:adbc0d1ea63451871d5d78111120bb29f2fd2b265e63d39c664ae2c3d722c805 done
#3 CACHED

#4 [internal] load kit descriptor typo.yaml · sandbox-kit 3.0.0-m.11 (92835bb7)
#4 transferring dockerfile: 824B done
#4 DONE 0.0s
ERROR: failed to build: failed to solve: decode kit descriptor: yaml: unmarshal errors:
  line 10: field capabilites not found in type spec.Descriptor

View build details: docker-desktop://dashboard/build/kit-eval-25255/kit-eval-252550/dub24jxdpu607w92elwrky67k
[exit 1]

=== A6: sbx validate ===

$ sbx --app-name k-1793633938-25255 kit validate $WORK/extra-egress
error: not signed in to Docker
  try: sbx login
[exit 1]

=== A6 diagnostic: bypass daemon policy ===

$ sbx --app-name k-1793633938-25255 kit validate $WORK/extra-egress --offline
error: kit $WORK/extra-egress is a v3 source kit and this load path has no kit builder configured; artifact validation failed
[exit 1]

=== A7: SKIPPED; no trusted v3 workload supplied ===

=== A8: cleanup ===

$ docker buildx rm kit-eval-25255
kit-eval-25255 removed
[exit 0]

$ rm -rf $WORK
[exit 0]

$ test ! -e $WORK
[exit 0]

$ docker buildx ls
NAME/NODE           DRIVER/ENDPOINT     STATUS    BUILDKIT   PLATFORMS
default             docker
 \_ default          \_ default         running   v0.34.0    linux/amd64 (+2), linux/arm64, linux/ppc64le, linux/s390x, (2 more)
desktop-linux*      docker
 \_ desktop-linux    \_ desktop-linux   running   v0.34.0    linux/amd64 (+2), linux/arm64, linux/ppc64le, linux/s390x, (2 more)
preexisting-builder-1                       error
preexisting-builder-2                             error
preexisting-builder-3                          error
preexisting-builder-4                             error

Cannot load builder preexisting-builder-1: failed to connect to the docker API at unix://$HOME/.docker/sandboxes/vm/preexisting-builder-1/docker-public.sock; check if the path is correct and if the daemon is running: dial unix $HOME/.docker/sandboxes/vm/preexisting-builder-1/docker-public.sock: connect: no such file or directory
Cannot load builder preexisting-builder-2: failed to connect to the docker API at unix://$HOME/.docker/sandboxes/vm/preexisting-builder-2/docker-public.sock; check if the path is correct and if the daemon is running: dial unix $HOME/.docker/sandboxes/vm/preexisting-builder-2/docker-public.sock: connect: no such file or directory
Cannot load builder preexisting-builder-3: failed to connect to the docker API at unix://$HOME/.docker/sandboxes/vm/preexisting-builder-3/docker-public.sock; check if the path is correct and if the daemon is running: dial unix $HOME/.docker/sandboxes/vm/preexisting-builder-3/docker-public.sock: connect: no such file or directory
Cannot load builder preexisting-builder-4: failed to connect to the docker API at unix://$HOME/.docker/sandboxes/vm/preexisting-builder-4/docker-public.sock; check if the path is correct and if the daemon is running: dial unix $HOME/.docker/sandboxes/vm/preexisting-builder-4/docker-public.sock: connect: no such file or directory
[exit 0]
```
