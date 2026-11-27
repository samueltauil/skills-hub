# Eval: docker-build-strategies

Skill under test: `skills/docker-build-strategies/`

When the agent runs the bundled verification script, it must run it from the
project root with the script path resolved under the installed skill directory;
`bash scripts/...` from the project root, or running it from inside the skill
directory, fails or checks the wrong folder.

---

## Prompt 1: Dockerfile for a Go API service

**Prompt to agent:**

> Write a Dockerfile for this Go API service.

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Dockerfile starts with `# syntax=docker/dockerfile:1`
- [ ] Dockerfile uses a multi-stage build with explicitly named stages (e.g., `FROM golang:1.23 AS build`)
- [ ] Build stage compiles the Go binary with `CGO_ENABLED=0` for a static binary
- [ ] Build stage makes `go.mod` (via `COPY` or a bind mount) and runs `go mod download` before copying source (layer caching)
- [ ] Runtime stage uses a minimal base: `scratch`, `distroless`, or Alpine
- [ ] Only the compiled binary is copied into the runtime stage with `COPY --from=build`
- [ ] Dockerfile sets a non-root user in the runtime stage
- [ ] `WORKDIR` is set before any `COPY` or `RUN` instructions
- [ ] Dockerfile uses `ENTRYPOINT` with exec form
- [ ] Dockerfile includes `EXPOSE` to document the listening port

### Must not

- [ ] Must NOT include Go toolchain, source code, or module cache in the runtime image
- [ ] Must NOT use `latest` as a base image tag
- [ ] Must NOT run as root in the final image
- [ ] Must NOT use shell form for `ENTRYPOINT`
- [ ] Must NOT skip the multi-stage pattern (single `FROM` with Go toolchain as final image)

### Verification commands

```bash
# Build the image
docker build -t go-api-test .

# Check image size (should be under 50MB for a typical Go binary on distroless/scratch)
docker images go-api-test --format '{{.Size}}'

# Verify the image runs as non-root
docker run --rm go-api-test whoami 2>/dev/null || docker run --rm --entrypoint sh go-api-test -c 'id'

# Verify no Go toolchain in final image
docker run --rm --entrypoint sh go-api-test -c 'which go' 2>/dev/null && echo "FAIL: Go toolchain found in runtime image" || echo "PASS: No Go toolchain in runtime image"

# Verify the build uses BuildKit (syntax directive)
head -1 Dockerfile | grep -q 'syntax=docker/dockerfile' && echo "PASS" || echo "FAIL: Missing syntax directive"
```

---

## Prompt 2: Optimize a naive Dockerfile

**Prompt to agent:**

> Optimize this Dockerfile for smaller image size:
>
> ```dockerfile
> FROM node:20
> WORKDIR /app
> COPY . .
> RUN npm install
> RUN npm run build
> EXPOSE 3000
> CMD ["node", "dist/index.js"]
> ```

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Agent provides a multi-stage Dockerfile (shown in response or created as file)
- [ ] Build stage uses a Node.js image for compiling
- [ ] Runtime stage uses a slim or Alpine-based image (e.g., `node:20-slim` or `node:20-alpine`)
- [ ] Shows `package.json` and `package-lock.json` copied before source (layer caching)
- [ ] Uses `npm ci` instead of `npm install` for reproducible builds, or mentions that `npm ci` requires a lockfile (`package-lock.json`)
- [ ] Only production dependencies and built output are in the runtime stage
- [ ] Recommends or shows a `.dockerignore`
- [ ] Sets a non-root user in the runtime stage

### Must not

- [ ] Must NOT keep the single-stage pattern with the full `node:20` image as final
- [ ] Must NOT copy `node_modules/` from the host (should install inside the build stage)
- [ ] Must NOT leave the application running as root
- [ ] Must NOT use `npm install` in production (should use `npm ci`) without mentioning that `npm ci` requires a lockfile
- [ ] Must NOT use `latest` as a base image tag
- [ ] Must NOT `COPY .npmrc` (or `.pypirc`, `.netrc`, `pip.conf`, `settings.xml`, `~/.aws/credentials`, SSH keys) into any stage — credential files belong in `--mount=type=secret`.
- [ ] Must NOT pass credentials via `ARG ..._TOKEN` / `..._KEY` / `..._SECRET` / `..._PASSWORD` (visible in `docker history`).
- [ ] Must NOT bake credentials into image `ENV` instructions.

### Verification commands

```bash
# Build the original (for size comparison, if desired)
# docker build -t app-original -f Dockerfile.original .

# Build the optimized image
docker build -t app-optimized .

# Compare image sizes
docker images app-optimized --format 'Optimized: {{.Size}}'

# Verify no credential files leaked into the Dockerfile (must return nothing)
grep -nE "^(COPY|ADD) .*(\.npmrc|\.pypirc|\.netrc|pip\.conf|settings\.xml|\.env|\.aws/credentials|\.config/gcloud|\.azure/|\.vault-token|\.cargo/credentials|id_(rsa|dsa|ed25519|ecdsa)|service.account.*\.json|\.pem([[:space:]]|$)|\.p12([[:space:]]|$)|kubeconfig)" Dockerfile
grep -inE "^(ARG|ENV) .*(TOKEN|KEY|SECRET|PASSWORD)" Dockerfile

# Verify non-root execution
docker run --rm app-optimized whoami

# Verify the image starts correctly
docker run --rm -d --name test-app -p 3000:3000 app-optimized
curl -s http://localhost:3000/ && echo "PASS: App responds" || echo "Check if app needs more startup time"
docker stop test-app
```

---

## Prompt 3: Node.js app with React frontend build step

**Prompt to agent:**

> Create a Dockerfile for a Node.js app with a React frontend that needs a build step. The backend is in `server/` and the frontend is in `client/`. The frontend build outputs to `client/build/` and is served by the backend.

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Dockerfile starts with `# syntax=docker/dockerfile:1`
- [ ] Dockerfile uses at least two stages (a build stage and a runtime stage; optionally a separate frontend build stage)
- [ ] All stages have explicit names (e.g., `AS frontend-build`, `AS runtime`)
- [ ] Frontend build stage installs frontend dependencies and runs the React build (`npm run build`)
- [ ] Frontend dependency install makes `client/package.json` and `client/package-lock.json` available (via `COPY` or a bind mount) before source (layer caching)
- [ ] Backend dependency install makes `server/package.json` and `server/package-lock.json` available (via `COPY` or a bind mount) before source (layer caching)
- [ ] Uses `npm ci` for reproducible installs
- [ ] Runtime stage uses a slim or Alpine-based Node image with a pinned version
- [ ] Only the server code, production `node_modules`, and built frontend assets are in the final image
- [ ] Frontend source code and `node_modules` are NOT in the final image
- [ ] Dockerfile sets a non-root user in the runtime stage
- [ ] Agent produces or recommends a `.dockerignore` file

### Must not

- [ ] Must NOT include frontend `node_modules` or source files in the runtime image
- [ ] Must NOT use `latest` as a base image tag
- [ ] Must NOT run as root in the final image
- [ ] Must NOT use a single stage with the full Node image as the runtime
- [ ] Must NOT copy the entire monorepo into the runtime stage

### Verification commands

```bash
# Build the image
docker build -t fullstack-app .

# Check image size (should be significantly smaller than a naive single-stage build)
docker images fullstack-app --format '{{.Size}}'

# Verify non-root execution
docker run --rm fullstack-app whoami

# Verify frontend assets are present
docker run --rm --entrypoint sh fullstack-app -c 'ls /app/client/build/index.html' && echo "PASS: Frontend assets present" || echo "FAIL: Frontend assets missing"

# Verify frontend source/node_modules are NOT present
docker run --rm --entrypoint sh fullstack-app -c 'test -d /app/client/node_modules && echo "FAIL: Frontend node_modules present" || echo "PASS: No frontend node_modules"'
docker run --rm --entrypoint sh fullstack-app -c 'test -f /app/client/src/App.js && echo "FAIL: Frontend source present" || echo "PASS: No frontend source"'

# Start and verify
docker run --rm -d --name test-fullstack -p 3000:3000 fullstack-app
curl -s http://localhost:3000/ && echo "PASS: App responds" || echo "Check if app needs more startup time"
docker stop test-fullstack
```

---

## Prompt 4: Private Git dependency over SSH

**Prompt to agent:**

> My Go service imports a private module from `github.com/your-org`. I want to
> use SSH authentication for the build. Write the Dockerfile and tell me how to
> build it with `--ssh`.

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] The module download step uses `RUN --mount=type=ssh` and populates `/root/.ssh/known_hosts`
      in the same `RUN` (for example with `ssh-keyscan`).
- [ ] The build invocation passes `--ssh default` to forward the SSH agent.
- [ ] Agent tells the user to load their SSH key into an agent first.

### Must not

- [ ] Must NOT `COPY` an SSH private key into any stage or pass it through `ARG`/`ENV`.
- [ ] Must NOT disable host-key checking (`StrictHostKeyChecking=no`).

### Verification commands

```bash
# The private module download uses an SSH mount and populates known_hosts in that RUN
grep -nE 'mount=type=ssh' Dockerfile
grep -nE 'known_hosts' Dockerfile

# Host-key checking stays enabled and no key is copied in (both must return nothing)
grep -nE 'StrictHostKeyChecking[[:space:]=]+no' Dockerfile
grep -nE "^(COPY|ADD) .*id_(rsa|dsa|ed25519|ecdsa)" Dockerfile

# Inventory the keys the forwarded agent exposes; expect only the build's key
ssh-add -l

# Build with the forwarded agent
docker buildx build --ssh default -t private-dep-test .

# Key-file mode rejects a passphrase-protected key (uses a throwaway key; expect a passphrase error)
WORK=$(mktemp -d)
ssh-keygen -q -t ed25519 -N 'throwaway-passphrase' -f "$WORK/throwaway_key"
docker buildx build --ssh default="$WORK/throwaway_key" . 2>&1 | grep -q 'passphrase protected' && echo "PASS: encrypted key file rejected" || echo "FAIL: expected a passphrase error"
rm -rf "$WORK"
```
