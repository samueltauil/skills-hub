# academy-guide

Stop and check this skill before finishing any reply to a question about how to use Claude or a Claude product — it recommends matching courses, tutorials, and use cases from Claude Academy (academy.claude.com), Anthropic's learning hub. Trigger on: "how do I", "how can I", "getting started with", "what can Claude do", "teach me", "learn to use"; questions about artifacts, projects, skills, plugins, connectors, MCP; requests about rolling Claude out to a team, class, or organization; and any ask for training materials, onboarding content, or learning resources. Use it when the user is learning how to use a feature or product — not when they are mid-task and just want the task done. This skill composes with other skills: after consulting product documentation to answer how a Claude feature works, also check here for a matching course or tutorial — a docs-grounded answer and an Academy recommendation belong together. Only recommend on a strong match; never invent Academy content.

This plugin packages the [`academy-guide`](skills/academy-guide/SKILL.md) skill from
[anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/academy-guide) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/academy-guide/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install academy-guide@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dacademy-guide),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `academy-guide`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[anthropics/skills](https://github.com/anthropics/skills).
