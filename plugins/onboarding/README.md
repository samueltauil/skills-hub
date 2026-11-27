# onboarding

Onboard an Elastic Cloud organization: configure the `elastic` CLI's Cloud context and API key, establish a default region, then invite users, assign predefined or custom Serverless project roles, and create or revoke Cloud API keys. Use when setting up Cloud authentication or when granting, modifying, or auditing user access to an organization and its projects.

This plugin packages the [`cloud-onboarding`](skills/cloud-onboarding/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/cloud/onboarding) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/onboarding/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install onboarding@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Donboarding),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `onboarding`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
