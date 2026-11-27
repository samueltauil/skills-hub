# java-diagnostics

Symptom-first runtime diagnostics for JVM applications using JDK tools: jcmd, jstack, jmap, jstat, JFR, GC logs, async-profiler, Native Memory Tracking, and Eclipse MAT. Use when a Java app has high CPU, memory leaks or OutOfMemoryError, slow startup, deadlocks or thread starvation, long GC pauses, native memory growth, or slow requests. Includes permission tiers for safe use.

This plugin packages the [`java-diagnostics`](skills/java-diagnostics/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/java-diagnostics) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/java-diagnostics/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install java-diagnostics@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Djava-diagnostics),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `java-diagnostics`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
