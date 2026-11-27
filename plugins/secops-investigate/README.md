# secops-investigate

Expert guidance for deep security incident and entity investigations in Google SecOps. Use when investigating cases, analyzing entities (hosts, IPs, domains, hashes, users), extracting and searching UDM events, performing asset and user timeline analysis, and detecting lateral movement across enterprise networks. Don't use for detection rule authoring or YARA-L tuning (use secops-detection-engineering), proactive hypothesis-driven hunting (use secops-hunt), initial alert triage (use secops-triage), or basic case status updates (use secops-cases).

This plugin packages the [`secops-investigate`](skills/secops-investigate/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/secops-investigate) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/secops-investigate/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install secops-investigate@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsecops-investigate),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `secops-investigate`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
