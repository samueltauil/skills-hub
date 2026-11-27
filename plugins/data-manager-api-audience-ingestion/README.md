# data-manager-api-audience-ingestion

Guides developers through managing (adding, removing, and clearing) audience members for Google products using the Data Manager API and its associated client libraries. Use this skill when the user wants to upload audience members, remove specific users, or clear/replace an entire audience for Customer Match, mobile device ID audiences, or any other audience use case supported by the Data Manager API. Don't use for uploading events or conversions (use the data-manager-api-event-ingestion skill), or for debugging errors, checking request status, or investigating low match rates (use the data-manager-api-troubleshooting skill).

This plugin packages the [`data-manager-api-audience-ingestion`](skills/data-manager-api-audience-ingestion/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/ads/data-manager-api-audience-ingestion) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/data-manager-api-audience-ingestion/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install data-manager-api-audience-ingestion@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddata-manager-api-audience-ingestion),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `data-manager-api-audience-ingestion`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
