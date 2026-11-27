# test-gap-audit

Run a read-only audit for missing, weak, stale, or mis-scoped test coverage. If the user does not name a scope, audit the full repository and identify important code paths, routes, features, services, workflows, and contracts that lack proper tests. If the user names a feature, PR, branch, route, workflow, service, bug fix, API, security-sensitive path, or risky code change, focus only on that specific scope. Use when the user asks what tests are missing, whether coverage is enough, what regression tests to add, or how to prove a change is safe. This is not a general bug audit and not a security review; it evaluates whether behavior is covered by tests.

This plugin packages the [`test-gap-audit`](skills/test-gap-audit/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/test-gap-audit) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/test-gap-audit/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install test-gap-audit@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dtest-gap-audit),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `test-gap-audit`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
