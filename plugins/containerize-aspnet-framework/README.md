# containerize-aspnet-framework

Containerize an ASP.NET .NET Framework project by creating Dockerfile and .dockerfile files customized for the project.

This plugin packages the [`containerize-aspnet-framework`](skills/containerize-aspnet-framework/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/containerize-aspnet-framework) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/containerize-aspnet-framework/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install containerize-aspnet-framework@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcontainerize-aspnet-framework),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `containerize-aspnet-framework`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
