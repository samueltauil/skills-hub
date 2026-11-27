# mongodb-connection

Optimize MongoDB client connection configuration (pools, timeouts, patterns) for any supported driver language. Use this skill when working/updating/reviewing on functions that instantiate or configure a MongoDB client (eg, when calling `connect()`), configuring connection pools, troubleshooting connection errors (ECONNREFUSED, timeouts, pool exhaustion), optimizing performance issues related to connections. This includes scenarios like building serverless functions with MongoDB, creating API endpoints that use MongoDB, optimizing high-traffic MongoDB applications, creating long-running tasks and concurrency, or debugging connection-related failures.

This plugin packages the [`mongodb-connection`](skills/mongodb-connection/SKILL.md) skill from
[mongodb/agent-skills](https://github.com/mongodb/agent-skills/tree/main/skills/mongodb-connection) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/mongodb-connection/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install mongodb-connection@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmongodb-connection),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `mongodb-connection`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[mongodb/agent-skills](https://github.com/mongodb/agent-skills).
