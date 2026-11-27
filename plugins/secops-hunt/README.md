# secops-hunt

Expert guidance for proactive threat hunting in Google SecOps. Use when proactively hunting for threats, retroactively analyzing indicators of compromise (IoCs), performing prevalence searches across enterprise events, hunting for MITRE ATT&CK techniques, or detecting behavioral and statistical outliers using UDM queries. Don't use for incoming alert triage (use secops-triage), active incident response and timeline deep-dives on a known breach (use secops-investigate), or detection rule authoring (use secops-detection-engineering).

This plugin packages the [`secops-hunt`](skills/secops-hunt/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/secops-hunt) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/secops-hunt/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install secops-hunt@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsecops-hunt),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `secops-hunt`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
