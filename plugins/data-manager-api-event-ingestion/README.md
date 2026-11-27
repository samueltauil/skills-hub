# data-manager-api-event-ingestion

Guides developers through implementing event and conversion ingestion to Google products using the Data Manager API /v1/events:ingest endpoint and its associated client libraries. Use this skill when the user wants to upload offline conversions, enhanced conversions for leads, click conversions, call conversions, Google Analytics web or app events, or any other event ingestion use case supported by the Data Manager API. Don't use for uploading audience members (use the data-manager-api-audience-ingestion skill), or for debugging errors, checking request status, or investigating missing conversions (use the data-manager-api-troubleshooting skill).

This plugin packages the [`data-manager-api-event-ingestion`](skills/data-manager-api-event-ingestion/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/ads/data-manager-api-event-ingestion) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/data-manager-api-event-ingestion/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install data-manager-api-event-ingestion@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddata-manager-api-event-ingestion),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `data-manager-api-event-ingestion`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
