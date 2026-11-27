# agent-platform-eval-flywheel

Measures and improves the quality of AI models and agents on Google Cloud using the Eval Quality Flywheel methodology. Use when generating synthetic user scenarios, evaluating an agent or model, building an eval dataset, picking or writing evaluation metrics, analyzing failures, comparing results before and after a fix, or when guidance is needed on Agent Platform eval methodology — including dataset schema, LLM-as-judge scoring, and common failure causes. For fine-tuning, use agent-platform-tuning. For general production deployment, use agent-platform-deploy.

This plugin packages the [`agent-platform-eval-flywheel`](skills/agent-platform-eval-flywheel/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/agent-platform-eval-flywheel) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-platform-eval-flywheel/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-platform-eval-flywheel@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-platform-eval-flywheel),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-platform-eval-flywheel`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
