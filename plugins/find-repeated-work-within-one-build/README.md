# find-repeated-work-within-one-build

Use ONLY for auditing executed-task counts or batching/hoisting costs within ONE MSBuild invocation: per-project Exec, duplicate dependency builds, per-item generators, run-once races. NEVER load for evaluation-only global-property variants with once-only target/task execution, idle-node/serial-chain investigations, second/unchanged builds, restores across commands, required-variant bin/obj collisions or unranked slowness. Do not load to check scope or replace an unavailable specialist; answer directly.

This plugin packages the [`find-repeated-work-within-one-build`](skills/find-repeated-work-within-one-build/SKILL.md) skill from
[dotnet/skills](https://github.com/dotnet/skills/tree/main/plugins/dotnet-msbuild/skills/find-repeated-work-within-one-build) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/find-repeated-work-within-one-build/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install find-repeated-work-within-one-build@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dfind-repeated-work-within-one-build),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `find-repeated-work-within-one-build`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[dotnet/skills](https://github.com/dotnet/skills).
