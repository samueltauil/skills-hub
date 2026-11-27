# litert-google-tensor

Compiles LiteRT (.tflite) models ahead-of-time for Google Tensor TPUs (Tensor G5 on Pixel 10, Tensor G6 on Pixel 11) locally on Linux x86_64 or on Google Colab (--colab on macOS, Windows, or ARM hosts), benchmarks them on a USB-attached Pixel with LiteRT's benchmark_model (NPU latency, peak memory, TPU tile time, TPU energy, optional CPU baseline), and packages compiled models for an Android Gradle app as a Google Play AI pack with the Tensor NPU runtime module and a Kotlin loader, applies it to the app and verifies it on a Pixel. Use when the user asks to compile, AOT-compile, or prepare a .tflite model for the Pixel TPU/NPU, check whether a .tflite is already Tensor-compiled, measure on-device NPU performance of a compiled model, or package or deploy a compiled model into their Android app (or replace the one it ships). Don't use for Qualcomm, MediaTek, or Samsung NPUs, GPU-only benchmarking, LiteRT-LM or LLM (.litertlm) models, on-device JIT compilation, non-Gradle builds, or publishing to Google Play.

This plugin packages the [`litert-google-tensor`](skills/litert-google-tensor/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/platform-devices/litert-google-tensor) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/litert-google-tensor/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install litert-google-tensor@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dlitert-google-tensor),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `litert-google-tensor`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
