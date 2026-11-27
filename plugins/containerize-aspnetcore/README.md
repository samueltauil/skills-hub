# containerize-aspnetcore

Containerize an ASP.NET Core project by creating Dockerfile and .dockerfile files customized for the project.

This plugin packages the [`containerize-aspnetcore`](skills/containerize-aspnetcore/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/containerize-aspnetcore) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/containerize-aspnetcore/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install containerize-aspnetcore@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcontainerize-aspnetcore),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `containerize-aspnetcore`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
