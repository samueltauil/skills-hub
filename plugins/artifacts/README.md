# artifacts

Build, debug, or review code that uses Cloudflare Artifacts, Git-compatible versioned storage, from Workers, the REST API, or Git clients. Use for the env.ARTIFACTS binding, creating, forking, or importing repositories, repo-scoped tokens, and pushing commits from a Worker.

This plugin packages the [`artifacts`](skills/artifacts/SKILL.md) skill from
[cloudflare/skills](https://github.com/cloudflare/skills/tree/main/skills/artifacts) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/artifacts/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install artifacts@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dartifacts),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `artifacts`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[cloudflare/skills](https://github.com/cloudflare/skills).
