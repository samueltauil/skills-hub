# cf-cli

Cloudflare's official cf CLI (beta) for the public Cloudflare API and Workers projects. Use for finding and running Cloudflare commands from the terminal — sign-in and profiles, cf cli search, cf schema, cf deploy/dev/build, resource commands for DNS, zones, D1, KV, and R2 — and for choosing between cf and Wrangler in a project.

This plugin packages the [`cf-cli`](skills/cf-cli/SKILL.md) skill from
[cloudflare/skills](https://github.com/cloudflare/skills/tree/main/skills/cf-cli) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cf-cli/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cf-cli@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcf-cli),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cf-cli`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[cloudflare/skills](https://github.com/cloudflare/skills).
