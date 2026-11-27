# gcloud

Provides safety-critical validation, guardrails, and data reduction for gcloud CLI operations across Google Cloud Platform (GCP) services and infrastructure. Use when planning, generating, constructing, proposing, describing, or executing any gcloud CLI commands - including when answering questions about gcloud syntax, or formatting flags. Don't use when writing Google Cloud client library code or raw REST/gRPC API requests.

This plugin packages the [`gcloud`](skills/gcloud/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gcloud) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gcloud/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gcloud@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgcloud),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gcloud`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
