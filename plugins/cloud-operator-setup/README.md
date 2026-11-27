# cloud-operator-setup

Sets up the user's personal operator agent in a Google Cloud organization via the `autocloud` MCP server: finds the organization, checks or creates the agent, saves the project and organization, and offers to share the user's existing Google Cloud operating context with the operator agent's memory. Use when the user runs this skill, asks to set up Cloud Operator or their operator agent (also in a named organization, but not for the whole organization as its administrator), asks to create their agent, or chooses setup when the cloud-operator skill asks. Don't use for ordinary GCP requests or installing gcloud.

This plugin packages the [`cloud-operator-setup`](skills/cloud-operator-setup/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-operator-setup) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-operator-setup/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-operator-setup@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-operator-setup),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-operator-setup`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
