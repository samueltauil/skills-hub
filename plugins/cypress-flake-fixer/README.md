# cypress-flake-fixer

Find and fix flake-prone anti-patterns in an existing Cypress suite, and APIs removed in Cypress 12 to 16. Bundles a zero-dependency scanner for fixed cy.wait() delays, assigned command return values, async/await, force: true, chaining after actions, one-shot expect() inside .then(), conditional testing, and removed APIs such as Cypress.env(), cy.exec(), cy.server()/cy.route(). Use when asked to fix flaky Cypress tests, remove cy.wait, stabilize or harden a Cypress suite, audit Cypress specs, debug "detached from the DOM" errors, or prepare an upgrade to Cypress 15 or 16.

This plugin packages the [`cypress-flake-fixer`](skills/cypress-flake-fixer/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/cypress-flake-fixer) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/cypress-flake-fixer/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install cypress-flake-fixer@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dcypress-flake-fixer),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `cypress-flake-fixer`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
