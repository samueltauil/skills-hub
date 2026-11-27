# cloud-run-basics

Manages Cloud Run services, jobs, and worker pools. Use when you need to deploy applications responding to HTTP requests (services), run event-triggered or scheduled tasks (jobs), or handle always-on pull-based background processing (worker pools).

This plugin packages the [`cloud-run-basics`](skills/cloud-run-basics/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-run-basics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-run-basics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-run-basics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-run-basics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-run-basics`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
