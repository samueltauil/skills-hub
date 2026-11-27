# sentry-prompt-optimizer

Creates, optimizes, and iteratively refines agent prompts, system prompts, developer prompts, and reusable prompt templates. Use when asked to improve a prompt, optimize a system prompt, rewrite an agent prompt, tune prompt wording, make a prompt more reliable, port prompts between OpenAI, Claude, or Gemini, or build prompt evals.

This plugin packages the [`prompt-optimizer`](skills/prompt-optimizer/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/prompt-optimizer) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/sentry-prompt-optimizer/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install sentry-prompt-optimizer@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsentry-prompt-optimizer),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `sentry-prompt-optimizer`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
