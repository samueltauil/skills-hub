# gke-custom-golden-image-discovery

Discovers golden base images for creating GKE custom node images based on technical specifications or context clues. Use when finding the golden base image for custom GKE node creation, mapping cluster configuration parameters (GKE version, OS, architecture, accelerators, gVisor, cgroups) to image names, or querying GKE base image maps. Don't use for general GKE cluster creation (use gke-cluster-creation) or standard node pool management (use gke-basics).

This plugin packages the [`gke-custom-golden-image-discovery`](skills/gke-custom-golden-image-discovery/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/gke-custom-golden-image-discovery) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/gke-custom-golden-image-discovery/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install gke-custom-golden-image-discovery@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgke-custom-golden-image-discovery),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `gke-custom-golden-image-discovery`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
