# google-agents-cli-onboarding

Onboarding entrypoint for agents-cli on Google Cloud (Gemini Enterprise Agent Platform). It should be used when the user wants to "create a new agent", "develop an agent", "build an agent using ADK", "build an agent using LangChain, LangGraph, or the Claude Agent SDK", "run the agent locally", "debug agent code", "test an agent", "evaluate an agent", "deploy an agent", "publish an agent", "monitor an agent", or needs the end-to-end production agent development lifecycle.

This plugin packages the [`google-agents-cli-onboarding`](skills/google-agents-cli-onboarding/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-agents-cli-onboarding) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-agents-cli-onboarding/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-agents-cli-onboarding@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-agents-cli-onboarding),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-agents-cli-onboarding`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
