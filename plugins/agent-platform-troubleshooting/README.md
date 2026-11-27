# agent-platform-troubleshooting

Troubleshoots Google Cloud Gemini Enterprise Agent Platform issues across Agent Gateway, Agent Connectivity Templates (ACT), Agent Registry, Agent Identity, Identity-Aware Proxy (IAP), Unified Access Policies (UAP), Model Armor, Semantic Governance Policies (SGP), Cloud DNS peering, Private CA TrustConfig, Next-Hop Secure Web Proxy (SWP), Explicit HTTPS Proxy (L4 AuthzPolicy), and Cloud Trace. Use when agent requests fail with 401/403/404/498/500/503 or Code 13, Egress request is not authorized, HTTP CONNECT fails with 404, Agent Runtime crashes on startup, or gateway/ACT/IAP/Model Armor/SGP configs fail validation. Don't use for general Google Cloud Identity and Access Management (IAM) debugging or networking issues unrelated to the Agent Platform stack.

This plugin packages the [`agent-platform-troubleshooting`](skills/agent-platform-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/agent-platform-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-platform-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-platform-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-platform-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-platform-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
