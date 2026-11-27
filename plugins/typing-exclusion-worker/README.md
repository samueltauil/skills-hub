# typing-exclusion-worker

Python typing exclusion worker: remove assigned mypy exclusion modules in small scoped batches, fix typing issues, run validation, and produce a structured completion summary. Use when running parallel typing-debt workers or when asked to remove modules from pyproject mypy exclusion overrides.

This plugin packages the [`typing-exclusion-worker`](skills/typing-exclusion-worker/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/typing-exclusion-worker) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/typing-exclusion-worker/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install typing-exclusion-worker@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtyping-exclusion-worker),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `typing-exclusion-worker`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
