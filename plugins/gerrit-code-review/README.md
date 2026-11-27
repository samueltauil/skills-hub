# gerrit-code-review

Reads and manages Gerrit code reviews over the HTTPS REST API: change metadata and diffs, inline comments and drafts, reviewers and CCs, labels and votes, checks, topics, hashtags, commit messages, cherry-picks, abandon, and submit. Use when working with Android (AOSP), Chromium, Fuchsia, or self-hosted Gerrit, when given a Gerrit change URL (https://*-review.googlesource.com/*, https://r.android.com/*, https://crrev.com/c/*, https://fxrev.dev/*, or https://*/c/*/+/*), or when git commands target a Gerrit host (refs/for/ pushes or branch cherry-picks). Don't use for local-only git operations or GitHub and GitLab pull requests.

This plugin packages the [`gerrit-code-review`](skills/gerrit-code-review/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/developers/gerrit-code-review) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gerrit-code-review/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gerrit-code-review@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgerrit-code-review),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gerrit-code-review`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
