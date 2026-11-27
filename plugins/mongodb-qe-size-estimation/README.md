# mongodb-qe-size-estimation

Estimates the storage and memory impact of encrypting fields in collections with Queryable Encryption (QE) enabled. Do NOT use for collections that use Client-Side Field Level Encryption (CSFLE) instead of QE.

This plugin packages the [`mongodb-qe-size-estimation`](skills/mongodb-qe-size-estimation/SKILL.md) skill from
[mongodb/agent-skills](https://github.com/mongodb/agent-skills/tree/main/skills/mongodb-qe-size-estimation) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mongodb-qe-size-estimation/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mongodb-qe-size-estimation@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmongodb-qe-size-estimation),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mongodb-qe-size-estimation`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[mongodb/agent-skills](https://github.com/mongodb/agent-skills).
