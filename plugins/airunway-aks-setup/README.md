# airunway-aks-setup

Set up AI Runway on AKS — from bare cluster to running model. Covers cluster verification, controller install, GPU assessment, provider setup, and first deployment. WHEN: "setup AI Runway", "onboard AKS cluster", "install AI Runway", "airunway setup", "deploy model to AKS", "GPU inference on AKS", "KAITO setup on AKS", "run LLM on AKS", "vLLM on AKS", "set up model serving on AKS", "AI Runway controller".

This plugin packages the [`airunway-aks-setup`](skills/airunway-aks-setup/SKILL.md) skill from
[microsoft/azure-skills](https://github.com/microsoft/azure-skills/tree/main/.github/plugins/azure-skills/skills/airunway-aks-setup) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/airunway-aks-setup/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install airunway-aks-setup@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dairunway-aks-setup),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `airunway-aks-setup`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[microsoft/azure-skills](https://github.com/microsoft/azure-skills).
