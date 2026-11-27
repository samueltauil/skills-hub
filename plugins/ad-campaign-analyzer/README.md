# ad-campaign-analyzer

Use this skill when the user shares ad campaign performance data and asks what to cut, scale, or test. Trigger for prompts like "analyze my ad campaigns", "where am I wasting ad spend", "reallocate my ad budget", "which ads are actually working", or "ROAS analysis". Do not trigger for campaign planning or creative generation without performance data.

This plugin packages the [`ad-campaign-analyzer`](skills/ad-campaign-analyzer/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/ad-campaign-analyzer) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/ad-campaign-analyzer/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install ad-campaign-analyzer@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dad-campaign-analyzer),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `ad-campaign-analyzer`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
