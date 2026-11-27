# hf-cloud-sagemaker-deployment-planner

Plan and coordinate the deployment of a model to Amazon SageMaker AI. Use this skill whenever the user wants to deploy, host, serve, or expose a model on SageMaker or AWS — including phrases like "deploy a model", "host this LLM on AWS", "serve this embedding model", "deploy a reranker", "deploy a text-to-image / diffusion model", "host this for async inference", "create an endpoint", "serve my fine-tuned model", or any request that involves making a model available for inference on AWS. Use this even when the user is vague (e.g. "I just want to get this running on AWS, you figure it out"). Works for text-generation LLMs, embedding models, rerankers, classifiers, text-to-image / diffusion models — picks the right serving stack and chooses between real-time and async inference. This is the entry-point skill for SageMaker deployment work — it asks clarifying questions, picks a deployment pathway, and coordinates the other deployment skills.

This plugin packages the [`hf-cloud-sagemaker-deployment-planner`](skills/hf-cloud-sagemaker-deployment-planner/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/hf-cloud-sagemaker-deployment-planner) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/hf-cloud-sagemaker-deployment-planner/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install hf-cloud-sagemaker-deployment-planner@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dhf-cloud-sagemaker-deployment-planner),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `hf-cloud-sagemaker-deployment-planner`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
