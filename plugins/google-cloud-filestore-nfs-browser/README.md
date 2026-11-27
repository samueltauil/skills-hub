# google-cloud-filestore-nfs-browser

Inspects, searches, and reads files and POSIX metadata on Filestore (NFS) instances on Google Cloud without local NFS client packages or root privileges. Use when browsing Filestore shares, searching files, reading remote logs, or inspecting file attributes; don't use for Cloud Storage buckets, Cloud NetApp Volumes, Persistent Disks, or modifying/deleting files.

This plugin packages the [`google-cloud-filestore-nfs-browser`](skills/google-cloud-filestore-nfs-browser/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-filestore-nfs-browser) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-filestore-nfs-browser/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-filestore-nfs-browser@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-filestore-nfs-browser),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-filestore-nfs-browser`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
