# stripe-apps

Build, modify, or review Stripe Apps and extensions using the relevant documentation and reference guides. Use for custom Stripe Dashboard UI, stripe-app.yaml, @stripe/ui-extension-sdk, @stripe/extensibility-sdk, script extensions, extension interfaces, custom workflow actions, and apps that authenticate to Stripe or react to events. Also use when deciding whether a Stripe extension can support the user's billing or workflow requirements.

This plugin packages the [`stripe-apps`](skills/stripe-apps/SKILL.md) skill from
[stripe/ai](https://github.com/stripe/ai/tree/main/skills/stripe-apps) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/stripe-apps/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install stripe-apps@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dstripe-apps),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `stripe-apps`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[stripe/ai](https://github.com/stripe/ai).
