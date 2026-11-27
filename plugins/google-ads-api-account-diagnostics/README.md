# google-ads-api-account-diagnostics

Diagnoses Google Ads account performance issues such as conversion loss (value or volume), low lead flow/volume, and lost impression share (opportunities) due to ad rank, bids, or budgets. Use when troubleshooting sudden performance drops, analyzing campaign impression share metrics, investigating low lead flow, or searching for bidding and budget constraints. Don't use for setting up new campaigns, uploading conversion events directly, or general Google Mobile Ads SDK integration issues (use gma-android-integrate instead).

This plugin packages the [`google-ads-api-account-diagnostics`](skills/google-ads-api-account-diagnostics/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/ads/google-ads-api-account-diagnostics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-ads-api-account-diagnostics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-ads-api-account-diagnostics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-ads-api-account-diagnostics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-ads-api-account-diagnostics`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
