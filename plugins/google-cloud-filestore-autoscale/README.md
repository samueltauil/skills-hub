# google-cloud-filestore-autoscale

Inspects Filestore capacity and utilization on Google Cloud, evaluates storage scaling rules, and performs capacity autoscaling (scale UP for low free space or scale DOWN for cost optimization). Use when monitoring Filestore instance headroom, resizing instance shares, configuring automated growth/shrink thresholds (custom thresholds apply globally across projects in session memory), or preventing out-of-space outages. Don't use for Cloud Storage (GCS) buckets, Persistent Disk block storage, or NetApp Volumes.

This plugin packages the [`google-cloud-filestore-autoscale`](skills/google-cloud-filestore-autoscale/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-filestore-autoscale) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-filestore-autoscale/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-filestore-autoscale@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-filestore-autoscale),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-filestore-autoscale`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
