# Usage Attribution

**MUST READ**: Before executing any `gcloud` command, REST API call, or Python
discovery-client call with this skill, follow these usage attribution
instructions. Tag every command you execute directly in the terminal so usage
can be attributed. The tag identifies only the skill and its version; it carries
no user data.

-   **`gcloud` CLI Commands**: Prefix every `gcloud` invocation, whatever the
    subcommand (in this skill, generic tasks such as enabling APIs, IAM, and
    `gcloud logging read`), with the metrics environment variable. Set it inline
    on each command because shell state may not persist between commands:

    ```bash
    CLOUDSDK_METRICS_REQUEST_ATTRIBUTION="agent-skills/1.0 (skill:application-integration-basics)" \
    gcloud <command> [flags]
    ```

    Do not use `gcloud config set` for this: it would persist beyond the current
    task and mislabel unrelated usage. `gcloud auth print-access-token` never
    needs the prefix, whether it runs on its own (for example to check
    credentials), inline as `$(gcloud auth print-access-token)`, or assigned
    first, as in `TOKEN="$(gcloud auth print-access-token)"`: it only fetches a
    credential, and the `curl` requests that use the token carry the attribution
    `User-Agent` header themselves. Every other `gcloud` command you run needs
    the prefix, including read-only and local ones such as
    `gcloud services list` or `gcloud config list`.

-   **Direct HTTP and REST Requests (`curl`)**: Application Integration has no
    Google-managed MCP server and no `gcloud integrations` command group; calls
    go to `https://integrations.googleapis.com/v1/...` (and
    `https://connectors.googleapis.com/...`). Add the header
    `-H "User-Agent: agent-skills/1.0 (skill:application-integration-basics)"`
    to every `curl` call you run directly. `curl` sends its own default
    `User-Agent` (`curl/<version>`) only when none is given, so an explicit
    `-H "User-Agent: ..."` replaces it; if a `User-Agent` header is already
    specified, append this string to the end of it rather than overwriting
    existing `User-Agent` data — the collection pipeline parses the
    `agent-skills/<version>` and `skill:<name>` tokens, so any rewording breaks
    attribution:

    ```bash
    curl -sS -H "Authorization: Bearer $(gcloud auth print-access-token)" \
      -H "User-Agent: agent-skills/1.0 (skill:application-integration-basics)" \
      "https://integrations.googleapis.com/v1/projects/PROJECT_ID/locations/LOCATION/integrations"
    ```

-   **Python discovery client run directly by you**: When you yourself run a
    one-off Python snippet in the terminal that uses
    `googleapiclient.discovery.build("integrations", "v1")` (or
    `build("connectors", "v1")`), wrap the authorized HTTP object with
    `googleapiclient.http.set_user_agent`, which adds the given string to the
    `User-Agent` header of every request made through that object (the client
    library's own `(gzip)` marker stays after it). Use this pattern
    (`google-auth-httplib2` is installed as a dependency of
    `google-api-python-client`):

    ```python
    import google.auth
    import google_auth_httplib2
    from googleapiclient import discovery
    from googleapiclient.http import set_user_agent

    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    http = set_user_agent(
        google_auth_httplib2.AuthorizedHttp(credentials),
        "agent-skills/1.0 (skill:application-integration-basics)",
    )
    service = discovery.build("integrations", "v1", http=http)
    ```

    Do not pass both `http=` and `credentials=` to `build`; because `http=`
    bypasses the scoping `build` normally applies, request the
    `https://www.googleapis.com/auth/cloud-platform` scope in
    `google.auth.default` as shown.

-   **Constraint for Generated Code**: The tracking prefix, `User-Agent` header,
    and `set_user_agent` wrapper are strictly for commands you execute directly
    in the terminal. Do NOT include them in code provided to the user for their
    own repositories, including generated scripts, CI/CD pipelines, Terraform
    configurations, ADK agents (including `ApplicationIntegrationToolset` code),
    Python modules, or integration version JSON.

-   **No host or credential changes**: The attribution is per command only. It
    is not a host change and does not need the approval required by the skill's
    "Host changes require approval" rule, because it never persists anything.
    Never persist it with `gcloud config set metrics/request_attribution`, by
    exporting the variable in a shell profile, or in `~/.curlrc`; those would be
    host changes (needing the user's approval under that rule) and would
    mislabel unrelated usage.

-   **User Opt-Out**: If the user asks to disable or remove tracking or
    attribution tags, omit the `CLOUDSDK_METRICS_REQUEST_ATTRIBUTION` variable,
    custom `User-Agent` suffix, and `set_user_agent` wrapper from all commands.
