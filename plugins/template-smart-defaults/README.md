# template-smart-defaults

Applies cross-parameter default rules when creating .NET projects with dotnet new, filling gaps consistently without overriding values the user set explicitly. USE FOR: choosing which target framework to pair with native AOT, deciding whether to keep HTTPS when authentication is enabled, recognizing that controllers and minimal-API flags are mutually exclusive, filling unset related parameters during project creation, explaining why a default was applied and ensuring an explicit user value is never overridden. DO NOT USE FOR: creating the project itself (use template-instantiation), finding or comparing templates (use template-discovery and template-comparison), authoring or validating custom templates (use template-authoring and template-validation).

This plugin packages the [`template-smart-defaults`](skills/template-smart-defaults/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-template-engine/skills/template-smart-defaults) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/template-smart-defaults/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install template-smart-defaults@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtemplate-smart-defaults),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `template-smart-defaults`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
