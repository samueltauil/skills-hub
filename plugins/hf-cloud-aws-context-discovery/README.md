# hf-cloud-aws-context-discovery

Discover the user's local AWS context (active profile, region, account ID, caller identity) at the start of any AWS task. Use this skill before any other AWS work — deploying to SageMaker, creating resources, calling AWS APIs, or anything that touches an AWS account. Use it especially when the user has not specified a region or profile explicitly, when they say things like "use my AWS account", "deploy to AWS", "use my profile", or when about to make any AWS CLI or SDK call. Never guess the region or account ID — always use this skill to read it from the local configuration first.

This plugin packages the [`hf-cloud-aws-context-discovery`](skills/hf-cloud-aws-context-discovery/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/hf-cloud-aws-context-discovery) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/hf-cloud-aws-context-discovery/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install hf-cloud-aws-context-discovery@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dhf-cloud-aws-context-discovery),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `hf-cloud-aws-context-discovery`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
