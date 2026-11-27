# upstream-patches

Create, amend, remove, and rebase patches for Terraform provider submodules using `./scripts/upstream.sh`. Use when `upgrade-provider` or manual patch work needs owning-patch lookup, patch conflict fixes, patch/hunk removal, or upstream rebase.

This plugin packages the [`upstream-patches`](skills/upstream-patches/SKILL.md) skill from
[pulumi/agent-skills](https://github.com/pulumi/agent-skills/tree/main/package-maintenance/skills/upstream-patches) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/upstream-patches/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install upstream-patches@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dupstream-patches),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `upstream-patches`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[pulumi/agent-skills](https://github.com/pulumi/agent-skills).
