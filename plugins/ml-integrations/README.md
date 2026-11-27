# ml-integrations

Install and manage Elastic security ML integration packages (beaconing, ded, dga, lmd, pad, problemchild, security_ai). Handles the full lifecycle: pre-flight checks, Fleet package install, component templates, ingest pipelines, transforms, data views, ML anomaly detection jobs, and detection rules. Use when a user asks to install, set up, check the status of, or troubleshoot a security ML integration package, including the technical preview Security for AI package.

This plugin packages the [`security-ml-integrations`](skills/security-ml-integrations/SKILL.md) skill from
[elastic/agent-skills](https://github.com/elastic/agent-skills/tree/main/skills/security/ml-integrations) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/ml-integrations/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install ml-integrations@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dml-integrations),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `ml-integrations`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[elastic/agent-skills](https://github.com/elastic/agent-skills).
