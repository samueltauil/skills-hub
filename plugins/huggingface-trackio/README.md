# huggingface-trackio

Track and visualize ML training experiments with Trackio. Use when logging metrics during training (Python API), firing alerts for training diagnostics, or retrieving/analyzing logged metrics (CLI). Supports real-time dashboard visualization, alerts with webhooks, HF Space syncing, and JSON output for automation.

This plugin packages the [`huggingface-trackio`](skills/huggingface-trackio/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/huggingface-trackio) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/huggingface-trackio/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install huggingface-trackio@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dhuggingface-trackio),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `huggingface-trackio`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
