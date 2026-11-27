# npm-trusted-publishing

Set up or fix npm trusted publishing (OIDC) in GitHub Actions and remove NPM_TOKEN. Use for ENEEDAUTH, E404 on PUT, E422 repository.url, or migrating off 2FA-bypass tokens before January 2027.

This plugin packages the [`npm-trusted-publishing`](skills/npm-trusted-publishing/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/npm-trusted-publishing) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/npm-trusted-publishing/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install npm-trusted-publishing@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dnpm-trusted-publishing),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `npm-trusted-publishing`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
