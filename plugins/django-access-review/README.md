# django-access-review

Django access control and IDOR security review. Use when reviewing Django views, DRF viewsets, ORM queries, or any Python/Django code handling user authorization. Trigger keywords: "IDOR", "access control", "authorization", "Django permissions", "object permissions", "tenant isolation", "broken access".

This plugin packages the [`django-access-review`](skills/django-access-review/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/django-access-review) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/django-access-review/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install django-access-review@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddjango-access-review),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `django-access-review`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
