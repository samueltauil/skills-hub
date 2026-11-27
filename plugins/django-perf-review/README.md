# django-perf-review

Django performance code review. Use when asked to "review Django performance", "find N+1 queries", "optimize Django", "check queryset performance", "database performance", "Django ORM issues", or audit Django code for performance problems.

This plugin packages the [`django-perf-review`](skills/django-perf-review/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/django-perf-review) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/django-perf-review/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install django-perf-review@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Ddjango-perf-review),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `django-perf-review`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
