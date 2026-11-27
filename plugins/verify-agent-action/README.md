# verify-agent-action

Review a proposed AI-agent action or human-approval packet before execution. Use when an agent wants to run a consequential tool, command, deployment, message, purchase, credential operation, or data mutation; when checking whether approval still matches the exact action; or when auditing action evidence for forged results, parameter swaps, replay, correlated reviewers, missing evidence, expiry, or stale monitoring. Produce an evidence-based review only—never execute or authorize the action.

This plugin packages the [`verify-agent-action`](skills/verify-agent-action/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/verify-agent-action) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/verify-agent-action/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install verify-agent-action@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dverify-agent-action),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `verify-agent-action`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
