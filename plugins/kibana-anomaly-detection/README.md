# kibana-anomaly-detection

Elastic ML anomaly detection — investigation/RCA, score explanation, job lifecycle troubleshooting, and job operations. Use when answering "what broke?"/"which entity?"/RCA, "why is score high/low?"/renormalization, "datafeed stopped"/"memory limit"/hard_limit, or configuring ML anomaly detection jobs. Reads results from `.ml-anomalies-*` and job state from ML REST APIs.

This plugin packages the [`kibana-anomaly-detection`](skills/kibana-anomaly-detection/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/kibana/kibana-anomaly-detection) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/kibana-anomaly-detection/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install kibana-anomaly-detection@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dkibana-anomaly-detection),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `kibana-anomaly-detection`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
