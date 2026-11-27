# make-blog-post

Turn code from the current session into a blog post written in the voice of its author. Covers one function, script, class, or tool as a focused walkthrough with a generalized sample and a usage example, learns tone and structure from existing posts or writing samples by the same author, takes the destination from what the user names or the blog repository in use instead of assumed folders, and saves no file until the draft is approved. Use when asked to write, draft, or turn code into a blog post, article, tutorial, or gist, or when invoked as /make-blog-post at the end of a turn.

This plugin packages the [`make-blog-post`](skills/make-blog-post/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/make-blog-post) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/make-blog-post/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install make-blog-post@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmake-blog-post),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `make-blog-post`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
