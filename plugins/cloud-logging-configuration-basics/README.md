# cloud-logging-configuration-basics

Configure single-project Cloud Logging on Google Cloud: regional log buckets, log sinks, log views, restricting or hiding sensitive logs in the default view (_Default) filter, IAM permissions for views (Logs View Accessor, IAM conditions), logs-based metrics, log exclusions, and sampling. Don't use for cross-project logging or multi-project setups.

This plugin packages the [`cloud-logging-configuration-basics`](skills/cloud-logging-configuration-basics/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/cloud-logging-configuration-basics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cloud-logging-configuration-basics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cloud-logging-configuration-basics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcloud-logging-configuration-basics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cloud-logging-configuration-basics`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
