# polytype-middleware

Design or review the public API of a PolyType middleware library so it stays complete on net472 and netstandard2.0 while modern .NET callers use where T : IShapeable<T> with no witness. Use when adding generic methods, witness or TProvider overloads, extension members, or a #if NET / #if !NET split.

This plugin packages the [`polytype-middleware`](skills/polytype-middleware/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/polytype-middleware) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/polytype-middleware/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install polytype-middleware@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dpolytype-middleware),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `polytype-middleware`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
