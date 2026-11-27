# audit-and-reduce-dependencies

Reduces JavaScript dependency footprint with pnpm while preserving lockfile, workspace layout, and dependency range style. Runs /check-npm first, then removes unused deps, dedupes versions, ranks transitive closure, and reports Keep/Replace/Remove triage. Use when cleaning up pnpm dependencies, reducing lockfile size, or shrinking node_modules in Grafana plugins; not for Go modules or full GitHub Actions workflow audits.

This plugin packages the [`audit-and-reduce-dependencies`](skills/audit-and-reduce-dependencies/SKILL.md) skill from
[grafana/skills](https://github.com/grafana/skills/tree/main/skills/grafana-plugins/audit-and-reduce-dependencies) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/audit-and-reduce-dependencies/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install audit-and-reduce-dependencies@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Daudit-and-reduce-dependencies),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `audit-and-reduce-dependencies`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[grafana/skills](https://github.com/grafana/skills).
