# slang-shader-engineer

Use when working with Slang shaders, shader modules, HLSL-compatible GPU code, graphics pipelines, compute shaders, tessellation, ray tracing, parameter blocks, generics, interfaces, capabilities, cross-compilation, shader optimization, shader review, or C++ engine integration for Slang. Trigger on any mention of Slang, .slang files, slangc, SPIR-V from Slang, Slang modules, [shader("compute")], [shader("vertex")], or requests to write/review/refactor shader code with modern language features. Also trigger for Slang-to-HLSL/GLSL/Metal/CUDA cross-compile questions, or when the user says "shader" alongside "generics", "interfaces", "parameter blocks", "autodiff", or "capabilities".

This plugin packages the [`slang-shader-engineer`](skills/slang-shader-engineer/SKILL.md) skill from
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/slang-shader-engineer) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/slang-shader-engineer/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install slang-shader-engineer@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dslang-shader-engineer),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `slang-shader-engineer`.

## License

MIT. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[github/awesome-copilot](https://github.com/github/awesome-copilot).
