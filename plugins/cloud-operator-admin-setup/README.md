# cloud-operator-admin-setup

Sets up and manages the Cloud Operator Agent ("Gemini for Google Cloud operations" in the console) for a Google Cloud organization: turning it on or off, its organization-wide settings, and user access. Use when an organization administrator wants to set it up for the whole organization or change it, or when Cloud Operator is turned off for the organization or the user has no access there. Don't use when someone asks to set up Cloud Operator or their operator agent for themselves, even in a named organization (use `cloud-operator-setup`).

This plugin packages the [`cloud-operator-admin-setup`](skills/cloud-operator-admin-setup/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-operator-admin-setup) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-operator-admin-setup/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-operator-admin-setup@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-operator-admin-setup),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-operator-admin-setup`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
