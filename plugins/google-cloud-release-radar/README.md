# google-cloud-release-radar

Tracks, queries, and summarizes official Google Cloud release notes across 360+ products and curated product bundles using a customizable watchlist. Use when the user asks what shipped recently in Google Cloud, wants to check release notes, deprecations, security bulletins, or breaking changes for specific services or curated bundles, or wants to set up, add, remove, or view products on their release watchlist. Don't use when deploying infrastructure, troubleshooting runtime errors, or writing product release notes for internal codebases.

This plugin packages the [`google-cloud-release-radar`](skills/google-cloud-release-radar/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-release-radar) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-release-radar/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-release-radar@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-release-radar),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-release-radar`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
