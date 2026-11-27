# BigQuery Migration Service (BQMS) remote MCP server configuration reference

This guide helps you troubleshoot and validate connections, permissions, and
request headers for the remote BigQuery Migration Service (BQMS) MCP server.

## Table of Contents

-   [Connection Troubleshooting & Permissions](#connection-troubleshooting-permissions)
    (lines 23–43)
-   [Connection Parameters](#connection-parameters) (lines 45–59)
-   [Verifying Endpoint Connectivity](#verifying-endpoint-connectivity) (lines
    61–76)
-   [Option A: Quick Automatic Install via `add-mcp`](#option-a-quick-automatic-install-via-add-mcp)
    (lines 78–121)
-   [Option B: Manual JSON Configuration](#option-b-manual-json-configuration)
    (lines 123–144)
-   [Example Configuration Blocks](#example-configuration-blocks) (lines
    146–218)
-   [Initiating the Connection](#initiating-the-connection) (lines 220–241)
-   [Sample Prompts for MCP Clients](#sample-prompts-for-mcp-clients) (lines
    243–256)

## Connection Troubleshooting & Permissions

If tool calls return authorization, billing, or quota errors, verify that:

1.  **API Enabled**: The BigQuery Migration Service API
    (`bigquerymigration.googleapis.com`) is enabled in the target project.
2.  **IAM Roles**: The agent or user identity has:
    -   `roles/mcp.toolUser` (MCP Tool User)
    -   `roles/bigquerymigration.editor` (Migration Workflow Editor)
    -   `roles/storage.objectViewer` and `roles/storage.objectCreator` (or
        `roles/storage.objectAdmin`) on the staging and output Cloud Storage
        buckets when running Batch Translation workflows.
3.  **OAuth Scopes**: The client token includes:
    -   `https://www.googleapis.com/auth/bigquerymigration` (or
        `https://www.googleapis.com/auth/cloud-platform`)
    -   `https://www.googleapis.com/auth/devstorage.read_write` (or
        `https://www.googleapis.com/auth/devstorage.read_only` for read-only
        Cloud Storage access)
4.  **Billing Header**: All requests must include the `x-goog-user-project`
    header set to your Google Cloud Project ID (**must be the string ID, not the
    numeric project number**).

## Connection Parameters

When configuring an MCP client (such as Claude Code, Cursor, Gemini CLI, or VS
Code) to connect to the remote BigQuery Migration Service MCP server, use the
following parameters:

Parameter                 | Value / Description
:------------------------ | :------------------
**Server Name**           | Any name, e.g. `bigquery-migration-service`
**Server URL / Endpoint** | `https://bigquerymigration.googleapis.com/mcp`
**Transport**             | Streamable HTTP (`httpUrl`)
**Authentication**        | Google Cloud Credentials (`google_credentials`) or Application Default Credentials (ADC)
**OAuth Scopes**          | `https://www.googleapis.com/auth/bigquerymigration`<br>`https://www.googleapis.com/auth/devstorage.read_write`
**Headers**               | `x-goog-user-project: {project_id}` (Cloud Project ID string)
**Timeout**               | `30000` (30 seconds)

## Verifying Endpoint Connectivity

Before configuring an AI client, you can test connectivity to the remote
BigQuery Migration Service (BQMS) MCP endpoint without authentication by sending
an unauthenticated `tools/list` JSON-RPC request:

```bash
curl -s -X POST https://bigquerymigration.googleapis.com/mcp \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' \
    -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}'
```

A successful response returns a JSON-RPC envelope listing all available BigQuery
Migration Service (BQMS) MCP tools (`translate_query`, `get_translation`,
`explain_translation`, `generate_ddl_suggestion`, `fetch_ddl_suggestion`, etc.).

## Option A: Quick Automatic Install via `add-mcp`

You do **not** need to manually locate or edit configuration files when using
[`add-mcp`](https://github.com/neondatabase/add-mcp). The `add-mcp` tool
automatically detects your installed AI clients (Claude Code, Cursor, Gemini
CLI, VS Code, etc.) and registers the remote Streamable HTTP BigQuery Migration
Service (BQMS) MCP server into their configuration paths:

-   **All Auto-Detected Clients**:

    ```bash
    npx -y add-mcp@latest https://bigquerymigration.googleapis.com/mcp --name bqms --header "x-goog-user-project: {project_id}"
    ```

-   **Claude Code**:

    ```bash
    npx -y add-mcp@latest https://bigquerymigration.googleapis.com/mcp --name bqms --header "x-goog-user-project: {project_id}" -a claude-code
    ```

-   **Cursor**:

    ```bash
    npx -y add-mcp@latest https://bigquerymigration.googleapis.com/mcp --name bqms --header "x-goog-user-project: {project_id}" -a cursor
    ```

-   **Gemini CLI**:

    ```bash
    npx -y add-mcp@latest https://bigquerymigration.googleapis.com/mcp --name bqms --header "x-goog-user-project: {project_id}" -a gemini-cli
    ```

-   **VS Code**:

    ```bash
    npx -y add-mcp@latest https://bigquerymigration.googleapis.com/mcp --name bqms --header "x-goog-user-project: {project_id}" -a vscode
    ```

> **Note on Google Cloud Authentication (`google_credentials`)**: `add-mcp`
> emits standard MCP fields and does not automatically add Google Cloud
> credential settings. After running `add-mcp`, add your Google Cloud
> authentication settings (`"authProviderType": "google_credentials"` in Gemini
> CLI, or an `"Authorization": "Bearer {access_token}"` header in other clients)
> as shown in [Example Configuration Blocks](#example-configuration-blocks).

## Option B: Manual JSON Configuration

If you prefer to edit configuration files manually, locate the file for your
tool or IDE below and add the corresponding configuration from
[Example Configuration Blocks](#example-configuration-blocks):

-   **Gemini CLI**:
    -   Global: `~/.gemini/settings.json`
    -   Project level: `.gemini/settings.json`
-   **Claude Code**:
    -   Global: `~/.claude.json`
    -   Project level: `.mcp.json`
-   **Claude Desktop**:
    -   macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
    -   Windows: `%APPDATA%\Claude\claude_desktop_config.json`
-   **Cursor**:
    -   Global: `~/.cursor/mcp.json` (or Project level: `.cursor/mcp.json`), or
        managed via **Settings > Features > MCP**
-   **VS Code**:
    -   Project level: `.vscode/mcp.json`
    -   Global (via settings): Open Command Palette (`Cmd/Ctrl+Shift+P`), choose
        "MCP: Open User Configuration", and add the server under `"servers"`.

## Example Configuration Blocks

Replace `{project_id}` with your actual Google Cloud Project ID (must be the
string ID, not the numeric project number).

### 1. Gemini CLI (`~/.gemini/settings.json` or `.gemini/settings.json`)

Gemini CLI natively supports Google Application Default Credentials via
`"authProviderType": "google_credentials"` and `"httpUrl"`:

```json
{
  "mcpServers": {
    "bqms": {
      "httpUrl": "https://bigquerymigration.googleapis.com/mcp",
      "authProviderType": "google_credentials",
      "oauth": {
        "scopes": [
          "https://www.googleapis.com/auth/bigquerymigration",
          "https://www.googleapis.com/auth/devstorage.read_write"
        ]
      },
      "timeout": 30000,
      "headers": {
        "x-goog-user-project": "{project_id}"
      }
    }
  }
}
```

### 2. Cursor / Claude Code (`~/.cursor/mcp.json` or `.mcp.json`)

Standard Streamable HTTP MCP clients use `"url"` and pass an OAuth bearer token
(e.g., from `gcloud auth print-access-token`) in `"headers"`:

```json
{
  "mcpServers": {
    "bqms": {
      "type": "http",
      "url": "https://bigquerymigration.googleapis.com/mcp",
      "headers": {
        "Authorization": "Bearer {access_token}",
        "x-goog-user-project": "{project_id}"
      }
    }
  }
}
```

### 3. VS Code (`.vscode/mcp.json`)

VS Code uses the top-level `"servers"` key with `"type": "http"` and `"url"`:

```json
{
  "servers": {
    "bqms": {
      "type": "http",
      "url": "https://bigquerymigration.googleapis.com/mcp",
      "headers": {
        "Authorization": "Bearer {access_token}",
        "x-goog-user-project": "{project_id}"
      }
    }
  }
}
```

*Note: The `"bqms"` JSON key dictates the server name. If you rename it (e.g.,
to `"BigQueryMigration"`), use that new name when configuring permissions and
invoking tools.*

## Initiating the Connection

Once the configuration file is in place, initiate the connection so the BigQuery
Migration Service (BQMS) MCP tools (like `translate_query`) become available to
the agent:

-   **Gemini CLI**:
    -   **Automatic**: The CLI reads `~/.gemini/settings.json` (and project
        `.gemini/settings.json`) during startup and connects to the Streamable
        HTTP endpoint automatically. Run `/mcp` inside Gemini CLI to verify the
        server status.
-   **Claude Desktop / Claude Code**:
    -   **Restart or Reload**: Restart the application or session so it reads
        the updated config and connects to the Streamable HTTP endpoint.
-   **Cursor**:
    -   **Settings UI**: Navigate to **Settings > Features > MCP**. If using
        `.cursor/mcp.json`, click the **Refresh** icon next to the server to
        establish the Streamable HTTP connection.
-   **VS Code**:
    -   **Auto-Reload**: VS Code watches `.vscode/mcp.json` and connects on
        save, or you can run `MCP: List Servers` from the Command Palette
        (`Cmd/Ctrl+Shift+P`) to start or restart the server.

## Sample Prompts for MCP Clients

The following natural language prompts demonstrate standard workflows when
interacting with the BigQuery Migration Service (BQMS) MCP server:

-   **Ad-hoc Query Translation**: "Translate this query from `{dialect}`:
    `{query}`. Use `{project_id}` and `{location}`."
-   **Quality & Error Assessment**: "Assess the translation quality and
    summarize compiler errors."
-   **Translation Explanation**: "Explain the translation and behavioral
    differences between the source query and BigQuery GoogleSQL."
-   **DDL Suggestion for Missing Schemas**: "Generate DDL for this input query."
-   **Prepend Schema and Retranslate**: "Prepend the generated DDL statements to
    the input query and retranslate."
