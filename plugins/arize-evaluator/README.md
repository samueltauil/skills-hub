# arize-evaluator

Handles LLM-as-judge evaluation workflows on Arize including creating/updating evaluators, running evaluations on spans or experiments, managing tasks, trigger-run operations, column mapping, and continuous monitoring. Use when the user mentions create evaluator, LLM judge, hallucination, faithfulness, correctness, relevance, run eval, score spans, score experiment, trigger-run, column mapping, continuous monitoring, or improve evaluator prompt.

This plugin packages the [`arize-evaluator`](skills/arize-evaluator/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/arize-evaluator) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/arize-evaluator/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install arize-evaluator@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Darize-evaluator),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `arize-evaluator`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
