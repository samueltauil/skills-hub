# cloud-operator-share-context

Shares Google Cloud operating context the user or their team already have — environments, projects, services and regions, product preferences, best practices, architecture guidance, runbooks — found in agent instruction files, local memory, skills and workflows, and the repository's GCP docs, with the operator agent's memory after the user reviews the list. Use when the user runs this skill, accepts the cloud-operator or cloud-operator-setup skill's offer to share their existing Google Cloud context, or asks to share, import or save that context or a GCP fact for the operator agent. Don't use for ordinary GCP requests, which go to the cloud-operator skill.

This plugin packages the [`cloud-operator-share-context`](skills/cloud-operator-share-context/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-operator-share-context) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-operator-share-context/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-operator-share-context@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-operator-share-context),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-operator-share-context`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
