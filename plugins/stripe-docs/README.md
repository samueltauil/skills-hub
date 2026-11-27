# stripe-docs

Use when the user or agent needs to read, search, or look up Stripe documentation or API reference. Prefer this over curl or WebFetch for any docs.stripe.com content. Use to fetch gated documentation.

This plugin packages the [`stripe-docs`](skills/stripe-docs/SKILL.md) skill from
[stripe/ai](https://github.com/stripe/ai/tree/main/skills/stripe-docs) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/stripe-docs/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install stripe-docs@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dstripe-docs),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `stripe-docs`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[stripe/ai](https://github.com/stripe/ai).
