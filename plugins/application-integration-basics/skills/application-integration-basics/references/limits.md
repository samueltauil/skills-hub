# Quotas, Limits, and Pricing

This reference summarizes Application Integration execution timeouts, payload and variable size caps, concurrency quotas, task and loop limits, Integration Connectors limits, and billing and pricing rules.

- [Execution Timeouts and Lifetimes](#execution-timeouts-and-lifetimes): Lines 12-22
- [Payload and Variable Size Limits](#payload-and-variable-size-limits): Lines 23-39
- [Concurrency and Request Rate Quotas](#concurrency-and-request-rate-quotas): Lines 40-50
- [Resource, Task, and Loop Limits](#resource-task-and-loop-limits): Lines 51-67
- [Integration Connectors Limits](#integration-connectors-limits): Lines 68-75
- [Pricing Summary](#pricing-summary): Lines 76-80

## Execution Timeouts and Lifetimes

| Limit | Value | Notes |
| :--- | :--- | :--- |
| Synchronous (`SYNC`) execution timeout | 2 minutes | Timed-out runs become `CANCELLED`. |
| Asynchronous (`ASYNC`) execution timeout | 10 minutes | Applies to Schedule, Cloud Scheduler, Cloud Pub/Sub, Salesforce triggers, `:schedule`, and executions resumed from a suspension or approval. |
| Default `:execute` HTTP timeout | 120 seconds | Controlled by the `X-Server-Timeout` request header. |
| Maximum execution lifetime | 31 days | Maximum total duration (44,640 minutes) an execution can last, including time paused in `Approval` or `Suspend` tasks. |
| Replay execution deadline | 10 minutes | Default deadline for replayed executions before they become `CANCELLED`. |
| Publish propagation window | Up to 10 minutes | Eventual consistency: an older version can keep serving traffic for up to 10 minutes after a new version is published. |

## Payload and Variable Size Limits

| Limit | Value | Notes |
| :--- | :--- | :--- |
| Cumulative integration data size | 30 MB | Total size across all integration input, output, and runtime variables (shared with private-trigger sub-integrations). |
| Local logging cutoff | 10 MB | Above 10 MB of integration data, the run continues but **local logging is disabled**, retry strategies do not run, and the execution does not appear in Cloud Monitoring dashboards. |
| API trigger cumulative input size | 8 MB | Larger requests fail immediately without starting an execution. |
| Cumulative data sent to and received from connections | 8 MB | Across integration input and output variables (Application Integration quotas). |
| Connectors task payload / response | 10 MB payload / 20 MB response | Maximum `Connectors` task payload (Integration Connectors quotas) and connector response size (Application Integration quotas). |
| Data Mapping variable limits | 20 MB (JSON/string); 100,000 elements (array) | Maximum size per variable in a `Data Mapping` task. |
| Data Transformer Script (Jsonnet) memory | 300 MB | Maximum evaluation memory for a `Data Transformer Script` task. |
| JavaScript task request size | 25 MB | Maximum payload passed into the V8 JavaScript task runtime. |
| Call REST Endpoint payload | 20 MB request / 34 MB response | Maximum HTTP request body and response size. |
| Loop data processed / collected output | 20 MB processed; 50 MB collected | `While Loop`, `For Each Loop`, and `For Each Parallel` process up to 20 MB; `While Loop` and `For Each Loop` collect up to 50 MB across sub-integration calls. |
| Cloud Logging entry size | 256 KiB | Above 256 KiB, request and response parameters are omitted from the Cloud Logging entry. |
| Console Execution Logs response | 300 MB | Above 300 MB, the console shows `Response size too large` (use the `executions.list` REST API instead). Event parameters in log messages truncate at 2,000 characters. |

## Concurrency and Request Rate Quotas

| Quota | Default value | Notes |
| :--- | :--- | :--- |
| Concurrent executions per project per region | 50 | Adjustable quota per project in each region. Backoff retries also default to 50 concurrent executions per project and region (up to 10 retries at 10, 20, 40... minutes). |
| Concurrent executions per integration | 10 | Separate adjustable per-integration concurrency cap. A burst on a single integration hits 10 concurrent executions, not 50. |
| Integration execution request rate | Shown on Cloud Quotas page | The execution request rate quota is shown on the Cloud Quotas page for the project and can be adjusted there. |
| Execution-log read requests per minute | 18,000 | Per project. |
| Call REST Endpoint concurrent calls | 100 | Maximum concurrent outbound calls from `Call REST Endpoint` tasks. |
| For Each Parallel concurrency | 50 | Default parallel sub-integration executions. |

## Resource, Task, and Loop Limits

| Limit | Value |
| :--- | :--- |
| Integrations per project | 1,000 |
| Tasks per integration | 100 |
| Versions per integration | 100 |
| Integration name length | 64 characters |
| API trigger name length | 64 characters |
| For Each Loop / While Loop iterations | 8,000 |
| For Each Parallel iterations | 10,000 |
| Call Integration sub-integrations | 10,000 |
| Send Email recipients | 30 |
| Connectors task timeout | 3 minutes |
| Connectors task pagination | Default page size 25; max 50,000 pages |
| Connectors Execute Custom Query | Max 180 seconds; max 50,000 rows |

## Integration Connectors Limits

| Limit | Value | Notes |
| :--- | :--- | :--- |
| Connections per region | 50 | Per Google Cloud project and region. |
| Nodes per connection | 100 | Exceeding allocated node capacity returns HTTP `429` throttling errors; raise min/max nodes or configure a task retry strategy. |
| Maximum unique regions | 20 | Maximum regions in which connections can be created in a project. |

## Pricing Summary

- **Billing account requirement**: An active billing account must be attached to the Google Cloud project even when usage stays within the monthly free tier.
- **Billable dimensions and free tier**: Application Integration provides a monthly free tier covering integration executions, data processed, and Google service connector nodes. Usage beyond the free tier is billed based on integration executions, data processed, and active Integration Connectors nodes (for Google service and third-party connectors).
- **Current rates and cost estimation**: Review current free-tier thresholds and pay-as-you-go rates on the [Application Integration pricing page](https://cloud.google.com/application-integration/pricing), and use the Google Cloud Pricing Calculator to estimate monthly costs.
