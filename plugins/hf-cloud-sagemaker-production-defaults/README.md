# hf-cloud-sagemaker-production-defaults

Create a SageMaker endpoint (real-time, real-time scale-to-zero, or async) with autoscaling, CloudWatch alarms, and tagging enabled by default. Use this skill whenever about to create a SageMaker endpoint, write deployment code that calls `create_endpoint`, or finalize a deployment after the image URI and IAM role are known. Provides deploy.py for real-time endpoints, deploy_ic.py for real-time endpoints that scale to zero instances via inference components, and deploy_async.py for async endpoints (also scale-to-zero). This is the last step in the SageMaker deployment workflow. Never generate a bare `create_endpoint` call without these defaults — endpoints without autoscaling or alarms are demos, not deployments.

This plugin packages the [`hf-cloud-sagemaker-production-defaults`](skills/hf-cloud-sagemaker-production-defaults/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/hf-cloud-sagemaker-production-defaults) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/hf-cloud-sagemaker-production-defaults/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install hf-cloud-sagemaker-production-defaults@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dhf-cloud-sagemaker-production-defaults),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `hf-cloud-sagemaker-production-defaults`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
