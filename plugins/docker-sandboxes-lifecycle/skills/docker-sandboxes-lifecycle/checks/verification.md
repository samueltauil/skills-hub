# Verification Runbook for local sandbox lifecycle commands

User-run integration checks; not executed during skill generation. Prerequisites:
standalone `sbx`, Git, a supported local runtime, and an existing Docker login.
`sbx login` changes shared authentication, not just the isolated test app.
Run from the skill directory in one shell; negative checks intentionally fail.
Never use a real repository or production credentials for these checks.

## 1. Create an isolated test session and disposable Git repository

```bash
APP="l-$(date +%s)-$$"  # unique suffix, at most 20 characters
WORK=$(mktemp -d)
REPO="$WORK/repo"
git init -q -b main "$REPO"
git -C "$REPO" -c user.name=Test -c user.email=test@example.invalid commit -q --allow-empty -m initial
sbx --app-name "$APP" version
sbx --app-name "$APP" policy init balanced
```
Pass: standalone version is displayed and policy is initialized for this fresh
app. Every following `sbx` command must retain this same `--app-name`.
If inherited `DOCKER_CLI_PLUGIN_ORIGINAL_CLI_COMMAND` causes plugin-wrapper
output, unset it before invoking standalone `sbx`.

## 2. Compare create-without-path and run-with-a-workspace

```bash
sbx --app-name "$APP" create --name no-mount-check shell
sbx --app-name "$APP" run --name mount-check -d shell "$REPO"
sbx --app-name "$APP" ls --json
sbx --app-name "$APP" run --name mount-check -d
sbx --app-name "$APP" ls --json
```
Pass: `no-mount-check` has no workspace; `mount-check` has `$REPO`. Reusing
`--name mount-check` does not create a third sandbox. Detached run does not
open an interactive agent session.

## 3. Check clone-mode creation and reattachment

```bash
sbx --app-name "$APP" create --clone --name clone-check shell "$REPO"
git -C "$REPO" remote -v
sbx --app-name "$APP" run --clone --name clone-check -d
sbx --app-name "$APP" run --clone --name no-mount-check -d
```
Pass: the remote `sandbox-clone-check` exists; reattaching to `clone-check`
succeeds; the last command fails because `no-mount-check` was not created in
clone mode. The disposable repository has a real `.git` directory and is
neither a linked worktree nor a submodule.

## 4. Preserve fetched clone commits before removal

```bash
sbx --app-name "$APP" exec clone-check git -c user.name=Test -c user.email=test@example.invalid commit --allow-empty -m clone-check-commit
git -C "$REPO" fetch sandbox-clone-check
git -C "$REPO" log --oneline -1 refs/remotes/sandbox-clone-check/main
sbx --app-name "$APP" rm --force clone-check
git -C "$REPO" rev-parse --verify refs/remotes/sandbox-clone-check/main
git -C "$REPO" log --oneline -1 refs/sandboxes/clone-check/main
```
Pass: the first log shows `clone-check-commit`. After this consented removal,
`rev-parse` fails (the ordinary remote ref was removed) but the survivor ref
still shows that commit. Exec uses the sandbox's recorded workspace, not an
assumed `/workspace`. Unfetched commits would be lost on removal.

## 5. Confirm read-only mounts remain readable

```bash
mkdir "$WORK/docs"
printf 'readable-content\n' > "$WORK/docs/notes.txt"
sbx --app-name "$APP" run --name ro-check -d shell "$REPO" "$WORK/docs:ro"
sbx --app-name "$APP" exec ro-check cat "$WORK/docs/notes.txt"
sbx --app-name "$APP" exec ro-check sh -c 'echo x >> "$1"' sh "$WORK/docs/notes.txt"
```
Pass: reading succeeds; writing fails with a read-only/permission error.
Use harmless test content, never a real secrets file.

## 6. Preview prune candidates and its age filter

```bash
sbx --app-name "$APP" run --name prune-keep -d shell "$REPO"
sbx --app-name "$APP" create --name prune-drop shell "$REPO"
sbx --app-name "$APP" stop prune-drop
sbx --app-name "$APP" prune --dry-run --json
sbx --app-name "$APP" prune --dry-run --json --filter until=168h
```
Pass: the unfiltered preview includes `prune-drop` and excludes running
`prune-keep`; other stopped test sandboxes may also appear. The age-filtered
preview is empty because this app's sandboxes were created moments ago,
not stopped more than a week ago. Neither preview removes anything.

## 7. Clean up only this disposable session

```bash
sbx --app-name "$APP" rm --force no-mount-check mount-check ro-check prune-keep prune-drop
sbx --app-name "$APP" daemon stop
rm -rf "$WORK"
```
Pass: these test sandboxes are removed and their isolated daemon stops. The
forced removals above are explicitly consented test cleanup, not defaults
for normal work. If a check stopped early, inspect this app with `sbx
--app-name "$APP" ls` and remove only its remaining test sandboxes first.
