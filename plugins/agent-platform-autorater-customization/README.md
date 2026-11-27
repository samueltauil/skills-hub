# agent-platform-autorater-customization

Customizes an autorater (evaluation metric) for an AI agent so its grades match the user's own judgment, starting from the agent's real trajectories. Use when a user wants a metric tailored to their agent, wants to turn failing trajectories into rubrics, says an existing autorater grades their agent wrong, or wants an autorater to agree with human labels (autorater hillclimbing, judge calibration). Don't use for quick evals with built-in metrics or for improving the agent itself (use agent-platform-eval-flywheel).

This plugin packages the [`agent-platform-autorater-customization`](skills/agent-platform-autorater-customization/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/agent-platform-autorater-customization) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-platform-autorater-customization/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-platform-autorater-customization@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-platform-autorater-customization),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-platform-autorater-customization`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
