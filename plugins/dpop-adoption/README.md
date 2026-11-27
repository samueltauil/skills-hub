# dpop-adoption

Implement and debug OAuth 2.0 DPoP (RFC 9449) refresh token sender-constraining for WebCrypto, Node.js ES6, and browser runtimes integrating with Google's OAuth platform. Use when configuring non-extractable asymmetric key pairs (P-256), generating DPoP Proof JWTs for authorization code exchange and token refresh, or handling 400 use_dpop_nonce challenge retry loops at oauth2.googleapis.com/token. Don't use for unconstrained OAuth 2.0 flows (where refresh tokens are not bound to a client key pair), or for Google Cloud IAM / service account authentication.

This plugin packages the [`dpop-adoption`](skills/dpop-adoption/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/identity/dpop-adoption) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/dpop-adoption/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install dpop-adoption@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddpop-adoption),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `dpop-adoption`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
