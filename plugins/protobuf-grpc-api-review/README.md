# protobuf-grpc-api-review

Review Protocol Buffer (.proto) and gRPC API changes for wire and JSON compatibility, safe schema evolution, rollout hazards, and RPC contract quality. Use when reviewing proto diffs, adding or changing messages and services, planning migrations, or diagnosing cross-version failures.

This plugin packages the [`protobuf-grpc-api-review`](skills/protobuf-grpc-api-review/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/protobuf-grpc-api-review) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/protobuf-grpc-api-review/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install protobuf-grpc-api-review@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dprotobuf-grpc-api-review),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `protobuf-grpc-api-review`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
