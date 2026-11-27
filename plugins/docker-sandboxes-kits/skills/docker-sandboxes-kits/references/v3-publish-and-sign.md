# Publishing and signing a v3 kit

Adapted from the `create-kit-v3` skill in docker/sandbox-kit-spec at
`4d932451613f8df89c8468e2bb7c5286882897ca`; publishing and signing have not
been re-run. Local build/conformance and source-load attempts are recorded in
[the authenticated results](../checks/authenticated-results.md). See [sources.md](sources.md)
for provenance and limits. Do not
use `sbx kit push` or `sbx kit sign` for a v3 kit; publishing and signing
here use `docker buildx` and `cosign`.

## Before you push

Publishing writes to a registry and cannot be undone by this skill: tags are
mutable, `latest` moves, and deleting a published tag or digest is
registry-specific and outside the source material. So:

- Get the user's explicit approval for the exact registry, repository, and
  tags before any `--push`. Never publish to a shared or production
  repository as a trial; use a scratch namespace.
- Verify first, locally: build, `kit-tck validate --layout`, and a real
  composition (`references/v3-recipes.md`). Publish only the kit you verified.
- Use credentials already configured for the registry through your normal
  Docker login. Never paste tokens into commands, descriptors, or build args.
- Signing is a separate, additive step. State plainly what was signed.

## Publishing is the build

A kit is an OCI artifact and the frontend has already written its
annotations, staged sources and config, so the thing in the registry is the
kit: there is no pack step, no sidecar artifact and no `kit push` subcommand
to look for. Add `--push` to the build that produced the kit you verified:

```sh
docker buildx build --builder kit-builder . -f <kit>.yaml \
  --platform linux/amd64,linux/arm64 --provenance=mode=min --push \
  -t <registry>/<kit>:<version> -t <registry>/<kit>:latest \
  --metadata-file /tmp/<kit>-push.json
kit-tck validate <registry>/<kit>:<version>
```

Validate after pushing: build-time checks cannot see annotations lost by an
exporter or registry. Explicit `--provenance=mode=min` also makes
single-platform index annotation predictable; Buildx's default provenance can
produce an index without kit annotations. Index annotations are an
optimization; consumers fall back to the platform manifest when the index
omits them (§9.3). An OCI layout's outer `index.json` is a catalog, separate
from any image index it references.

The named container builder matters here too. The `docker` driver with the
classic image store can drop manifest annotations during publication,
leaving an image that is no longer a kit.

**Push both platforms in one invocation.** One build writes the index
consumers resolve through; two single-platform builds pushed to the same tag
replace each other, leaving a tag that serves whichever ran last and silently
fails for everyone on the other architecture.

Tag the version and `latest` together. `<version>` is the descriptor's
expanded `version:`, so where a `version` arg drives the install it also
names the tag, and the tag says exactly what the image contains.

## Several kits in one repository

A repository per kit is the simple case; a repository holding a family of
them distinguishes kits *by tag*, which leaves `<kit>:<version>` nowhere to
put the version. Join them and keep the bare name as the moving tag:

```sh
docker buildx build --builder kit-builder . -f <kit>.yaml \
  --platform linux/amd64,linux/arm64 --provenance=mode=min --push \
  -t <registry>/<kits-repo>:<kit>-<version> \
  -t <registry>/<kits-repo>:<kit>
```

Publishing only the bare name leaves consumers no way to ask for a particular
build, or to notice they were moved onto a different one. Reference the
immutable tag from anything that has to keep working. A version-shaped *tag*
is also one of the inputs that answers an unversioned `provides` entry, which
`<kit>-<version>` is not; that is a reason to state `version:` in the
descriptor rather than leaning on how you tagged.

## Signing (optional, orthogonal)

Nothing in the kit grammar requires a signature and no consumer needs
`cosign` to run a kit. A signature is stored as its own object in the
repository rather than as part of the image, so it changes neither the kit's
digest nor its annotations, and a signed kit's `kit-tck` verdict is the one it
already had:

```sh
digest=$(jq -r '."containerimage.digest"' /tmp/<kit>-push.json)
cosign sign --yes <registry>/<kit>@"$digest"
```

**Sign the digest, never the tag.** `--metadata-file` reports the digest the
push actually produced; a tag is mutable, so a signature naming one attests
to whatever it happened to point at.

For a multi-platform build that digest is the **index's**, and signing it
signs the index alone: the per-platform manifests beneath it carry no
signature of their own, so a consumer verifying a platform digest directly
finds nothing. Add `--recursive` to sign each discrete image as well, or say
plainly that only the index is signed and expect verification to name the
index.

In CI, keyless signing avoids managing a key at all: grant the job
`id-token: write` and cosign takes its identity from the OIDC token. The
matching verification names the identity rather than a public key, and for
GitHub Actions that identity is the **workflow**, not the repository:

```sh
cosign verify <registry>/<kit>@"$digest" \
  --certificate-identity 'https://github.com/<org>/<repo>/.github/workflows/publish.yml@refs/tags/<tag>' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

**Name the whole identity, not a prefix of it.** An identity regexp like
`^https://github\.com/<org>/` accepts a certificate from *any* workflow in
*any* repository in the organization, so any job anywhere in the org with
`id-token: write` can mint something that passes, and verification then
proves only that the signature came from somebody in your org, which is not
the question being asked. The signature is only evidence of provenance when
the identity pins the repository, the workflow file and the ref. Where a tag
varies, keep the rest exact and vary only that part:

```sh
  --certificate-identity-regexp '^https://github\.com/<org>/<repo>/\.github/workflows/publish\.yml@refs/tags/'
```

## Tooling notes

- **`docker buildx`**: nothing to install for the frontend; BuildKit pulls
  `docker/sandbox-kit:3` from the `# syntax=` line. It was pulled successfully
  in the recorded 2026-11-02 run; PR CI also confirmed anonymous manifest
  availability and amd64/arm64 entries. This does not test anonymous layer
  downloads or establish a pinning policy. Consider pinning the recorded digest.
- **`sbx`**: install the stable CLI from Docker Docs, and see the
  `docker/sbx-releases` repository for releases. The source says current
  releases support Kits v3 in local and cloud mode and gives no minimum
  version. On tested `sbx v0.50.1`, both `kit validate --offline` and
  `kit inspect --offline` reject the supplied v3 source mixin with "no kit
  builder configured". This is intentional: offline omits the builder.
  Normal inspect and validate supply it and require an authenticated daemon.
- **`kit-tck`**: the source installs it with
  `go install github.com/docker/sandbox-kit-spec/v3/cmd/kit-tck@latest`.
  `@latest` floats, so install a pinned release tag or commit instead and
  record it, in the same way you would pin any build tool. A pinned `go install`
  may still print `dev` for `kit-tck version`; record `go version -m` on the
  installed binary to retain the actual module revision.
- **`cosign`**: only if you sign.
- **Local builds**: recipe-based local source builds use host Docker Buildx
  when Docker is available, otherwise the shared builder sandbox. The host
  builder needs OCI export support. Select the named builder with
  `BUILDX_BUILDER=kit-builder sbx kit inspect ./<kit>`, or use
  `SBX_KIT_BUILDER=sandbox` to require the sandbox backend and
  `SBX_KIT_BUILDER=host` to require the host backend. `BUILDX_BUILDER` was
  exercised in the authenticated run; the `SBX_KIT_BUILDER` overrides were not. Do not infer that a declaration-only mixin
  bypasses the daemon requirement: both offline source commands intentionally
  omit the builder. Also, v0.50.1 uses Buildx even for declaration-only sources;
  the in-process synthesis optimization exists in the inspected checkout,
  not that release. Sandbox builder status, history and removal describe
  only that backend; removing it does not clear host-builder caches.
