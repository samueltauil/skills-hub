# google-ads-api-quickstart

Guides developers through Google Ads API quickstart: credential setup, choosing from 6 client libraries/REST, configuring environments, and running a "retrieve campaigns" script. Troubleshoots common setup errors: USER_PERMISSION_DENIED, login_customer_id issues, and CLOUD_PROJECT_NOT_APPROVED_FOR_PRODUCTION (a Google Cloud project with Test access calling a production account). Use this skill when: - The user asks how to get started with the Google Ads API. - The user needs to set up Google Ads API access in a Google Cloud project or OAuth credentials. - The user wants to write a quickstart/example script for Google Ads. - The user encounters errors like USER_PERMISSION_DENIED, CLOUD_PROJECT_NOT_APPROVED_FOR_PRODUCTION, or the legacy DEVELOPER_TOKEN_NOT_APPROVED.

This plugin packages the [`google-ads-api-quickstart`](skills/google-ads-api-quickstart/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/ads/google-ads-api-quickstart) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-ads-api-quickstart/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-ads-api-quickstart@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-ads-api-quickstart),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-ads-api-quickstart`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
