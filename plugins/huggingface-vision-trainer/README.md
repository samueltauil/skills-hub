# huggingface-vision-trainer

Trains and fine-tunes vision models for object detection (D-FINE, RT-DETR v2, DETR, YOLOS), image classification (timm models — MobileNetV3, MobileViT, ResNet, ViT/DINOv3 — plus any Transformers classifier), and SAM/SAM2 segmentation using Hugging Face Transformers on Hugging Face Jobs cloud GPUs. Covers COCO-format dataset preparation, Albumentations augmentation, mAP/mAR evaluation, accuracy metrics, SAM segmentation with bbox/point prompts, DiceCE loss, hardware selection, cost estimation, Trackio monitoring, and Hub persistence. Use when users mention training object detection, image classification, SAM, SAM2, segmentation, image matting, DETR, D-FINE, RT-DETR, ViT, timm, MobileNet, ResNet, bounding box models, or fine-tuning vision models on Hugging Face Jobs.

This plugin packages the [`huggingface-vision-trainer`](skills/huggingface-vision-trainer/SKILL.md) skill from
[huggingface/skills](https://github.com/huggingface/skills/tree/main/skills/huggingface-vision-trainer) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/huggingface-vision-trainer/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install huggingface-vision-trainer@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dhuggingface-vision-trainer),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `huggingface-vision-trainer`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[huggingface/skills](https://github.com/huggingface/skills).
