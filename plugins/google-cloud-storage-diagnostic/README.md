# google-cloud-storage-diagnostic

Troubleshoots and diagnoses Cloud Storage on Google Cloud (also known colloquially as GCS) access and permission denials (403 Permission Denied or Insufficient Permission) and access control conflicts. Use whenever a user encounters or asks to analyze a 403 error on a bucket or object - including analysis-only questions where no commands are run - or needs help with IAM bindings, fine-grained ACLs, Uniform Bucket-Level Access (UBLA), getIamPolicy inspection denials and least-privilege inspection roles, browser storage.cloud.google.com Cookieauth and Data Access Audit Logging conflicts, Signed URL SignatureDoesNotMatch errors, VPC Service Controls (VPC-SC) perimeters, explicit IAM Deny policies, Bucket IP Filtering, Requester Pays, Retention Policy locks, Compute Engine VM access scopes, Application Default Credentials (ADC) mismatches, recursive delete permissions, or recreated service accounts. Don't use for creating buckets, routine uploads/downloads, proactive security audits, or Cloud Storage FUSE mounts.

This plugin packages the [`google-cloud-storage-diagnostic`](skills/google-cloud-storage-diagnostic/SKILL.md) skill from
[google/skills](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-storage-diagnostic) so it can be installed on its own. It is generated
by [Skills Hub](https://skillshub.space/skills/google-cloud-storage-diagnostic/) and follows the
[Agent Plugins](https://agent-plugins.org) specification.

## Install

GitHub Copilot CLI:

```sh
copilot plugin marketplace add samueltauil/skills-hub
copilot plugin install google-cloud-storage-diagnostic@skills-hub
```

VS Code (with `chat.plugins.enabled` turned on): [install with one click](https://vscode.dev/redirect?url=vscode%3A%2F%2Fchat-plugin%2Finstall%3Fsource%3Dsamueltauil%252Fskills-hub%26plugin%3Dgoogle-cloud-storage-diagnostic),
or add the `samueltauil/skills-hub` marketplace from the Agent Customizations editor and
search for `google-cloud-storage-diagnostic`.

## License

Apache-2.0. See [LICENSE](LICENSE). The skill content belongs to its original authors at
[google/skills](https://github.com/google/skills).
