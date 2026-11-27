# trl-training

Post-train LLMs with TRL (Transformers Reinforcement Learning) — SFT, DPO, GRPO, KTO, and reward-model training. Use when writing or debugging training code with the TRL Python API or the trl CLI.

This plugin packages the [`trl-training`](skills/trl-training/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/trl-training) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/trl-training/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install trl-training@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtrl-training),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `trl-training`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
