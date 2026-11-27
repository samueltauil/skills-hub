# item-management

Own concrete MSBuild ItemGroup and item-expression questions. USE FOR: Include, Remove, Update, item identity and metadata, transforms, filtering, batching, duplicate or overlapping items, and reviews that verify whether those operations are correct. Generated items stay in scope when the central defect is item identity, metadata, batching, duplicate declarations, or glob/Remove/Update semantics. For a generated artifact missing from compilation or output, wrong target timing/path, or FileWrites clean tracking without a broader item-semantics defect, use including-generated-files. The item operation may be broken, suspected, or already correct. Exclude property-only issues, general incrementality with no item question, broad reviews with no concrete item concern, and non-MSBuild systems.

This plugin packages the [`item-management`](skills/item-management/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/item-management) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/item-management/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install item-management@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ditem-management),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `item-management`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
