# blog-writing-guide

Write, review, and improve blog posts for the Sentry engineering blog following Sentry's specific writing standards, voice, and quality bar. Use this skill whenever someone asks to write a blog post, draft a technical article, review blog content, improve a draft, write a product announcement, create an engineering deep-dive, or produce any written content destined for the Sentry blog or developer audience. Also trigger when the user mentions "blog post," "blog draft," "write-up," "announcement post," "engineering post," "deep dive," "postmortem," or asks for help with technical writing for Sentry. Even if the user just says "help me write about [feature/topic]" — if it sounds like it could become a Sentry blog post, use this skill.

This plugin packages the [`blog-writing-guide`](skills/blog-writing-guide/SKILL.md) skill from
[getsentry/skills](https://github.com/getsentry/skills/tree/main/skills/blog-writing-guide) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/blog-writing-guide/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install blog-writing-guide@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dblog-writing-guide),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `blog-writing-guide`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[getsentry/skills](https://github.com/getsentry/skills).
