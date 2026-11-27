# Eval: docker-sandboxes-lifecycle

Skill under test: `skills/docker-sandboxes-lifecycle/`

Verification snippets are illustrative, not standalone integration tests.
Run them only against disposable resources with a fresh `APP` suffix (at
most 20 characters) and an initialized isolated policy. Follow the skill's
`checks/verification.md` for prerequisites and cleanup. Never substitute
the default daemon or approve untrusted files just to execute an eval.

---

## Prompt 1: create vs. run and the omitted-path trap

**Prompt to agent:**

> I want to launch claude in a sandbox in the current directory, but I keep
> getting a sandbox with no files in it. What's going on?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Identifies that the issue might come from running `sbx create claude` with no path.
- [ ] Recommends a valid fix: `sbx run claude` (mounts cwd), `sbx run claude .`,
      or `sbx create claude .` (explicit path).
- [ ] Does not claim `sbx create` and `sbx run` behave identically when the
      path is omitted.

### Must not

- [ ] Must NOT recommend just `sbx run NAME` (without `--name` flag or a path) without mentioning `sbx run --name NAME` to reattach to an existing sandbox.

### Verification commands

```bash
# First prepare APP, WORK, and REPO with the lifecycle runbook's step 1.
# shell tests the same workspace semantics without provider authentication.
sbx --app-name "$APP" create --name eval-no-mount shell
(cd "$REPO" && sbx --app-name "$APP" run --name eval-cwd -d shell)
sbx --app-name "$APP" ls --json
sbx --app-name "$APP" rm --force eval-no-mount eval-cwd  # consented test cleanup
```

---

## Prompt 2: isolate an agent from the host working tree

**Prompt to agent:**

> I don't want the agent editing my actual working tree directly — can it
> work on a copy instead, and how do I get its commits back before I delete
> the sandbox?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Recommends `sbx create --clone` / `sbx run --clone` (creation-time
      only), with the four preconditions (explicit path, inside a git repo,
      not a worktree, `.git` a real directory) mentioned or implied.
- [ ] Explains the host repo is mounted read-only and the agent commits into
      an in-container clone.
- [ ] Explains commits must be fetched with `git fetch sandbox-<name>` (a
      concrete, shell-valid name, not a literal `<name>` placeholder in a
      runnable command) BEFORE removing the sandbox, or they are lost.

### Must not

- [ ] Must NOT claim `--clone` silently succeeds as a no-op when reattaching
      to an existing plain (bind-mounted) sandbox.
- [ ] Must NOT claim removing/pruning a clone-mode sandbox is safe by
      default without mentioning the fetch-first step.

### Verification commands

```bash
# REPO is the disposable Git repository from the lifecycle runbook's step 1.
sbx --app-name "$APP" create --clone --name eval-clone shell "$REPO"
git -C "$REPO" remote -v | grep sandbox-eval-clone
git -C "$REPO" fetch sandbox-eval-clone
sbx --app-name "$APP" rm --force eval-clone  # consented test cleanup after fetch
```

---

## Prompt 3: routine cleanup

**Prompt to agent:**

> I have a bunch of old stopped sandboxes taking up space. How do I clean
> them up without touching anything that's still running?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Recommends `sbx prune` with `--filter until=DURATION` (e.g. `until=168h`) for
      cleaning up old stopped sandboxes.
- [ ] States that `sbx prune` never removes a running sandbox, but IS
      destructive to matching stopped sandboxes (state, secrets, and any
      unfetched clone commits) and should be previewed with `--dry-run` first.

### Must not

- [ ] Must NOT recommend `sbx rm --all` as the routine/safe cleanup command.
- [ ] Must NOT describe `sbx prune` as generally "safe to run habitually"
      without qualifying that it destroys stopped sandboxes and unfetched
      clone commits and should be previewed first.
- [ ] Must NOT default to `--force` for routine cleanup.

### Verification commands

```bash
sbx --app-name "$APP" prune --dry-run --filter until=168h
```

---

## Prompt 4: run a diagnostic and copy its output

**Prompt to agent:**

> I have a stopped sandbox. How do I copy a test input into it, run a
> diagnostic with a working directory and an environment variable, and
> copy the output back? Can I copy directly into another sandbox?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Uses `sbx exec` for the diagnostic, with `-w` for the working directory
      and `-e` for a non-secret variable; may note that exec and cp can operate
      on stopped sandboxes.
- [ ] Uses `sbx cp` in both directions, with exactly one `SANDBOX:PATH`
      argument and one host path.
- [ ] Explains sandbox-to-sandbox copying is unsupported; uses a host
      staging file if a second sandbox needs the output.

### Must not

- [ ] Must NOT invent a direct sandbox-to-sandbox `sbx cp` command.
- [ ] Must NOT require deleting or recreating the stopped sandbox to exec.

### Verification commands

```bash
sbx --app-name "$APP" create --name eval-diagnostic shell
printf 'diagnostic-input\n' > "$WORK/diagnostic-input.txt"
sbx --app-name "$APP" cp "$WORK/diagnostic-input.txt" eval-diagnostic:/tmp/input.txt
sbx --app-name "$APP" stop eval-diagnostic
sbx --app-name "$APP" exec -w /tmp -e DIAGNOSTIC=ready eval-diagnostic sh -c \
  'test "$DIAGNOSTIC" = ready && cat input.txt > output.txt'
sbx --app-name "$APP" cp eval-diagnostic:/tmp/output.txt "$WORK/diagnostic-output.txt"
cmp "$WORK/diagnostic-input.txt" "$WORK/diagnostic-output.txt"
sbx --app-name "$APP" rm --force eval-diagnostic  # consented test cleanup
```

Pass: exec restarts the sandbox and the copied output matches the host input.

---

## Prompt 5: publish a port on an existing sandbox

**Prompt to agent:**

> My existing sandbox serves HTTP on port 8080, but reattaching with
> `sbx run --name web -p 18080:8080` didn't expose it. How do I publish it
> on localhost and remove the mapping when I'm done?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Explains `-p`/`--publish` on create/run applies only at creation;
      reattaching does not change port bindings.
- [ ] Uses `sbx ports` with `--publish` to add the port mapping and `--unpublish`
      to remove it.

### Must not

- [ ] Must NOT require recreating the sandbox just to publish a port.
- [ ] Must NOT claim `sbx run -p` changes bindings on reattach.

### Verification commands

```bash
# Choose a free host port if 18080 is already in use.
sbx --app-name "$APP" create --name eval-ports shell
sbx --app-name "$APP" ports eval-ports --publish 127.0.0.1:18080:8080/tcp4
sbx --app-name "$APP" ports eval-ports --json
sbx --app-name "$APP" ports eval-ports --unpublish 127.0.0.1:18080:8080/tcp4
sbx --app-name "$APP" ports eval-ports --json
sbx --app-name "$APP" rm --force eval-ports  # consented test cleanup
```

Pass: the mapping appears, then disappears. This checks binding management,
not HTTP reachability; no server is started by this fixture.

---

## Prompt 6: stop now, resume later without losing state

**Prompt to agent:**

> I want to stop a sandbox overnight without losing files stored inside
> it. How do I resume the same sandbox tomorrow?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Recommends `sbx stop NAME`, which retains state, followed later by
      `sbx run --name NAME` to restart and attach to the same sandbox.
- [ ] Uses `sbx ls` to inspect status and distinguishes stopping from
      destructive `rm`/`prune`.

### Must not

- [ ] Must NOT recommend removal or pruning to preserve the sandbox.
- [ ] Must NOT create a replacement sandbox as the normal resume path.

### Verification commands

```bash
sbx --app-name "$APP" run --name eval-resume -d shell "$REPO"
sbx --app-name "$APP" exec eval-resume sh -c 'printf retained > /tmp/retained.txt'
sbx --app-name "$APP" stop eval-resume
sbx --app-name "$APP" ls --json
sbx --app-name "$APP" run --name eval-resume -d
sbx --app-name "$APP" exec eval-resume sh -c 'test "$(cat /tmp/retained.txt)" = retained'
sbx --app-name "$APP" rm --force eval-resume  # consented test cleanup
```

Pass: listing shows the stopped sandbox; its file survives stop/restart.

---

## Prompt 7: read-only reference files are not secret

**Prompt to agent:**

> I want the agent to read reference docs without editing them. Can I
> mount an extra directory with `:ro`? Would that also hide my API-key file?

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Shows how to add an extra directory as read-only (e.g., `:ro` suffix, `readOnly: true`, or equivalent).
- [ ] Explains read-only restricts writes but not reads, so it won't hide sensitive files;
      directs secrets to `sbx secret set` instead.

### Must not

- [ ] Must NOT claim a read-only mount hides sensitive content.
- [ ] Must NOT use an actual secret to demonstrate read-only behavior.

### Verification commands

```bash
mkdir "$WORK/eval-docs"
printf 'public reference\n' > "$WORK/eval-docs/notes.txt"
sbx --app-name "$APP" run --name eval-readonly -d shell "$REPO" "$WORK/eval-docs:ro"
sbx --app-name "$APP" exec eval-readonly cat "$WORK/eval-docs/notes.txt"
sbx --app-name "$APP" exec eval-readonly sh -c 'printf changed >> "$1"' sh "$WORK/eval-docs/notes.txt"
# The write above must fail; reading must succeed.
sbx --app-name "$APP" rm --force eval-readonly  # consented test cleanup
```

---

## Prompt 8: mount a directory, inspect it, and tear down

**Prompt to agent:**

> First, create a ./notes folder with a file called hello.md containing
> "hello from the host". Then, using Docker Sandboxes, spin up a sandbox
> with just the shell agent (no AI agent inside) that has that folder mounted.
> After creating it, list all sandboxes to confirm it exists. Then show me
> which files the sandbox can see in the mounted folder, and also show me the
> content of hello.md from inside the sandbox. When that's done, tear the
> sandbox down and double-check it's really gone by listing sandboxes again.
> Don't ask me questions, just do it.

> (AUTOMATED EVAL: You MUST NOT ask questions or request clarification. Proceed immediately with best-practice defaults. Create all necessary files even if the workspace appears empty.)

### Expected behaviors

- [ ] Creates a ./notes folder with hello.md containing "hello from the host".
- [ ] Creates a sandbox with `sbx run` or `sbx create` mounting the `./notes`
      folder as a workspace.
- [ ] Uses `sbx ls` to confirm the sandbox exists after creation.
- [ ] Uses `sbx exec` with `ls`, `find`, or `tree` to list files in the
      mounted directory from inside the sandbox.
- [ ] Uses `sbx exec` with `cat` to read the content of `hello.md` from
      inside the sandbox.
- [ ] Removes the sandbox with `sbx rm` (not `sbx prune` or `sbx rm --all`).
- [ ] Uses `sbx ls` again to verify the sandbox is gone.
- [ ] Shows "hello from the host" in the output from reading the file inside
      the sandbox.

### Must not

- [ ] Must NOT use `sbx rm --all` to remove the sandbox (too broad).
- [ ] Must NOT use `sbx prune` which could remove unrelated stopped sandboxes.
- [ ] Must NOT use `sbx reset` which would destroy all sandbox state.

### Verification commands

```bash
# Create test fixtures
mkdir -p "$WORK/notes"
printf 'hello from the host\n' > "$WORK/notes/hello.md"
printf '- write live skill evals\n' > "$WORK/notes/todo.md"

# Run the scenario
sbx --app-name "$APP" run --name eval-mount -d shell "$WORK/notes"
sbx --app-name "$APP" ls --json
sbx --app-name "$APP" exec eval-mount ls /workspace
sbx --app-name "$APP" exec eval-mount cat /workspace/hello.md
sbx --app-name "$APP" rm --force eval-mount
sbx --app-name "$APP" ls --json  # should not show eval-mount
```

---

## Should not trigger

- "Run my Docker Agent config with docker agent run --sandbox." → `docker-agent-run`

- "How do I stop an agent from reaching an internal API?" → `docker-sandboxes-network-credentials`
- "How do I write a checked-in config so my whole team gets the same sandbox setup?" → `docker-docs` (no catalog skill owns `sbxenv.yaml`)
- "How do I package a reusable mixin that adds a Postgres MCP server?" → `docker-sandboxes-kits`
