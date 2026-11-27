# azure-container-registry-cli

Manage Azure Container Registry via the az acr CLI including registries, images, cloud builds, ACR Tasks, authentication, tokens, geo-replication, and networking. Use when working with ACR, az acr commands, pushing/importing/purging container images in Azure, or when the user mentions Azure Container Registry.

This plugin packages the [`azure-container-registry-cli`](skills/azure-container-registry-cli/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/azure-container-registry-cli) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/azure-container-registry-cli/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install azure-container-registry-cli@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dazure-container-registry-cli),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `azure-container-registry-cli`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
