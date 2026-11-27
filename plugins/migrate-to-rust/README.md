# migrate-to-rust

Clones, analyzes, plans, and migrates legacy codebases (C++, Fortran, Java, Python, C, Shell) from a GitHub URL or local directory to a modern, high-performance, deterministic, 100% Safe Rust architecture, tracking live telemetry across every task bucket, test failure/fix cycle, and Profile-Guided Optimization (PGO) stage, and producing a first-person AI storytelling report and interactive HTML infographic. Use when migrating a GitHub repository or local codebase to Rust, porting legacy C++, Fortran, Python, or Java workloads to memory-safe Rust, designing Struct-of-Arrays (SoA) or SIMD Rust architectures, or optimizing Rust ports with LLVM PGO. Don't use for unrelated non-Rust refactoring or single-line syntax questions.

This plugin packages the [`migrate-to-rust`](skills/migrate-to-rust/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/developers/migrate-to-rust) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/migrate-to-rust/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install migrate-to-rust@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dmigrate-to-rust),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `migrate-to-rust`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
