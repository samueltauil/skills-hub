# server-side-conversion-tracking

Set up server-side conversion tracking so purchases are reported accurately to Facebook, TikTok, Google and Bing despite iOS restrictions, ad blockers and cookie loss. Use when conversions are under-reported, when platform-reported purchases do not match real orders, when asked about Conversions API / Events API / offline conversions / CAPI, click id passthrough (fbclid, ttclid, gclid, msclkid), or when ad optimization has degraded after tracking changes.

This plugin packages the [`server-side-conversion-tracking`](skills/server-side-conversion-tracking/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/server-side-conversion-tracking) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/server-side-conversion-tracking/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install server-side-conversion-tracking@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dserver-side-conversion-tracking),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `server-side-conversion-tracking`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
