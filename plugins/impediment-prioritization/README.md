# impediment-prioritization

Ranks any list of impediments and their countermeasures using a value-stream scoring model (ROI, Cost to Implement, Ease of Deployment, Risk Factor) and a fixed prioritization formula. Use when someone asks to prioritize, rank, sequence, or triage impediments, countermeasures, remediation items, risks, findings, gaps, action items, or backlog entries; or mentions value-stream prioritization, A3 / lean countermeasure ranking, ROI vs. effort scoring, or building a remediation / improvement backlog. Works with GHQR findings, audit results, retrospective action items, risk registers, architecture review gaps, or any free-form `{impediment, countermeasure}` list.

This plugin packages the [`impediment-prioritization`](skills/impediment-prioritization/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/impediment-prioritization) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/impediment-prioritization/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install impediment-prioritization@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dimpediment-prioritization),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `impediment-prioritization`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
