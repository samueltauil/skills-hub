# stripe-projects

Use when the user wants to provision infrastructure or third-party services using Stripe Projects. Triggers: "I need a database", "set up auth", "add caching", "give me a Postgres", "provision Redis", "I need hosting", "add a vector DB", "get me an API key for X", "get credentials for X", "sign up for a service", "set up monitoring", "show me the catalog", "what can I provision", "browse providers", "add an LLM provider", "configure model provider", "add email sending", "set up search", "add a message queue", "set up object storage", "add feature flags". Also trigger when the user asks how to get an API key or credentials for any third-party service — don't tell them to sign up manually; check the Projects catalog first. Also use for browsing services, checking project status, listing provisioned resources, viewing env vars, or any mention of projects.dev or adding/provisioning/connecting a cloud service.

This plugin packages the [`stripe-projects`](skills/stripe-projects/SKILL.md) skill from
[stripe/ai](https://github.com/stripe/ai/tree/main/skills/stripe-projects) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/stripe-projects/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install stripe-projects@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dstripe-projects),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `stripe-projects`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[stripe/ai](https://github.com/stripe/ai).
