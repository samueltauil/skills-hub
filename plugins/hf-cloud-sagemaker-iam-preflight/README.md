# hf-cloud-sagemaker-iam-preflight

Ensure a usable SageMaker execution role exists before deploying or training. Use this skill whenever about to create a SageMaker endpoint, model, training job, or any resource that requires an execution role. Use it especially when the user has not provided a role ARN explicitly, when scripts are about to call `iam:CreateRole`, or when an AccessDenied error mentions an IAM action. Never blindly call `iam:CreateRole` — always check for existing roles first. This skill prevents the most common SageMaker deployment failure: trying to create IAM resources from an SSO principal that has no IAM write permissions.

This plugin packages the [`hf-cloud-sagemaker-iam-preflight`](skills/hf-cloud-sagemaker-iam-preflight/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/hf-cloud-sagemaker-iam-preflight) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/hf-cloud-sagemaker-iam-preflight/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install hf-cloud-sagemaker-iam-preflight@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dhf-cloud-sagemaker-iam-preflight),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `hf-cloud-sagemaker-iam-preflight`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
