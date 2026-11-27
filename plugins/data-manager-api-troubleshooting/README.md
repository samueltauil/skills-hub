# data-manager-api-troubleshooting

Diagnoses and fixes errors, warnings, and missing data for Data Manager API event and audience ingestion requests. Use when an IngestEvents, IngestAudienceMembers, RemoveAudienceMembers, RemoveAllAudienceMembers, or RetrieveRequestStatus call fails (INVALID_ARGUMENT, REQUIRED_FIELD_MISSING, INVALID_HEX_ENCODING, PERMISSION_DENIED, UNAUTHENTICATED, RESOURCE_EXHAUSTED, INVALID_REQUEST_ID), when a response has fieldWarnings, when checking request status or diagnostics, when request status shows FAILED or PARTIAL_SUCCESS or processing errors, when finding which records failed, or when a request returned 200 but conversions or audience members are missing. Don't use for writing new ingestion code (use the data-manager-api-event-ingestion or data-manager-api-audience-ingestion skills) or first-time credential setup (use the data-manager-api-setup skill).

This plugin packages the [`data-manager-api-troubleshooting`](skills/data-manager-api-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/ads/data-manager-api-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/data-manager-api-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install data-manager-api-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddata-manager-api-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `data-manager-api-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
