# hf-cloud-python-env-setup

Set up an isolated Python environment for SageMaker / AWS work, with the right Python version and current boto3. Use this skill whenever Python code will be executed for a SageMaker deployment, training job, or any AWS automation — including when about to run `pip install`, when about to invoke `boto3`, when creating or activating a virtualenv, or when the user asks to "set up the environment". Never use system Python and never `pip install` into it. Always isolate. This skill prevents the most common failure modes: wrong Python version, dependency conflicts, and stale SDKs.

This plugin packages the [`hf-cloud-python-env-setup`](skills/hf-cloud-python-env-setup/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/hf-cloud-python-env-setup) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/hf-cloud-python-env-setup/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install hf-cloud-python-env-setup@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dhf-cloud-python-env-setup),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `hf-cloud-python-env-setup`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
