# iap-agent-platform-troubleshooting

Diagnoses Identity-Aware Proxy (IAP) denials of outbound requests from Gemini Enterprise Agent Platform agents that run on Agent Runtime and send traffic through Agent Gateway. Use when an agent request fails with "Egress request is not authorized", when Cloud Audit Logs show an IAP egressViaIAP decision with granted false, when IAP audit entries are missing while debugging agent egress, or when Access policies, IAP allow policies, policy bindings, or Agent Registry entries might block agent egress. Don't use for Gemini model IAM permission errors (such as aiplatform.endpoints.predict), Agent Platform API errors, or Agent Runtime deployment or 500 errors (use agent-platform-troubleshooting instead). Don't use for setting up, creating, or connecting an Agent Gateway, or for IAP web apps, IAP TCP forwarding, or SSH.

This plugin packages the [`iap-agent-platform-troubleshooting`](skills/iap-agent-platform-troubleshooting/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/iap-agent-platform-troubleshooting) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/iap-agent-platform-troubleshooting/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install iap-agent-platform-troubleshooting@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Diap-agent-platform-troubleshooting),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `iap-agent-platform-troubleshooting`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
