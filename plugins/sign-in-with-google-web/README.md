# sign-in-with-google-web

Implement, configure, and secure Sign In With Google (SiwG) using Google Identity Services (GIS / `https://accounts.google.com/gsi/client`) across web architectures. Use when creating Google sign-in buttons, implementing Google One Tap with FedCM, integrating GIS in React/Next.js/Angular/HTML, verifying ID tokens on backend runtimes (Python/Node.js/Go/Java), enforcing Google Workspace domain restrictions (`hd`), securing client-side ID tokens via WebCrypto nonces or encrypted IndexedDB, embedding in cross-origin iframes via the Intermediate Iframe API (`https://accounts.google.com/gsi/intermediate`), configuring Content Security Policy (CSP), COOP, and Permissions Policy (`identity-credentials-get`) headers, or handling sign-out and revocation. Don't use for legacy Google Sign-In (`gapi.auth2`), Google Cloud IAM service accounts, or Android/iOS native Credential Manager.

This plugin packages the [`sign-in-with-google-web`](skills/sign-in-with-google-web/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/identity/sign-in-with-google-web) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/sign-in-with-google-web/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install sign-in-with-google-web@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dsign-in-with-google-web),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `sign-in-with-google-web`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
