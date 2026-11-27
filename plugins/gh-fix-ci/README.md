# gh-fix-ci

Use when a user asks to debug or fix failing GitHub PR checks that run in GitHub Actions; use `gh` to inspect checks and logs, summarize failure context, draft a fix plan, and implement only after explicit approval. Treat external providers (for example Buildkite) as out of scope and report only the details URL.

This plugin packages the [`gh-fix-ci`](skills/gh-fix-ci/SKILL.md) skill from
[openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/gh-fix-ci) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gh-fix-ci/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gh-fix-ci@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgh-fix-ci),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gh-fix-ci`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[openai/skills](https://github.com/openai/skills).
