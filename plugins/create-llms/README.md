# create-llms

Create an llms.txt file from scratch based on repository structure following the llms.txt specification at https://llmstxt.org/

This plugin packages the [`create-llms`](skills/create-llms/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/create-llms) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/create-llms/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install create-llms@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcreate-llms),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `create-llms`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
