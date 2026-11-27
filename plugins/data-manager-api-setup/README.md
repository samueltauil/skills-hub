# data-manager-api-setup

Guides developers through client library installation and authentication setup steps for the Data Manager API. Use this skill when a user is getting started with the Data Manager API and needs to setup their local environment, install the client library, or setup access to the API. Don't use for implementing audience or event ingestion logic (use the data-manager-api-audience-ingestion or data-manager-api-event-ingestion skills instead), or for debugging UNAUTHENTICATED, PERMISSION_DENIED, or other errors from requests after setup (use the data-manager-api-troubleshooting skill).

This plugin packages the [`data-manager-api-setup`](skills/data-manager-api-setup/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/ads/data-manager-api-setup) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/data-manager-api-setup/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install data-manager-api-setup@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddata-manager-api-setup),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `data-manager-api-setup`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
