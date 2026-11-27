# agent-platform-deploy

Deploy open models or custom weights from Model Garden to Agent Platform endpoints, check the status of an in-progress deployment operation, or clean up resources by undeploying models and deleting endpoints. Use when asked to actively deploy a model, list the Model Garden CATALOG of available models, check if a specific model is deployable (`gcloud ai model-garden models list-deployment-config`), query deployment cost, troubleshoot deployment errors (like quota limits), or undeploy/clean up endpoints. Also use when copying and deploying a 1P Tuned Model. Don't use for pure listing/discovery questions of the form "is X deployed?", "list my endpoints", or "which regions have models running?" — for those use `agent-platform-endpoint-management`. Don't use for running model evaluations (use `agent-platform-eval-flywheel` skill).

This plugin packages the [`agent-platform-deploy`](skills/agent-platform-deploy/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/agent-platform-deploy) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/agent-platform-deploy/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install agent-platform-deploy@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dagent-platform-deploy),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `agent-platform-deploy`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
