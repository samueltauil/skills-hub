# Authoring `insights/executive_summary.html`

Optional. `build_report.py` synthesizes a data-driven Executive Summary when
this file is absent or empty. Write it only to add analysis the default lacks
(for example, what the Step 2.5 interview asked for).

Keep text brief and anchored on specific numbers from
`logging_usage_summary.json`. Follow SKILL.md Step 3: say what the cost figures
rest on, and state recoverable spend as a floor (`at least X%`), never "up to".
Quote unit prices and the free tier from `pricing.skus`, never from memory.

## Styling

The template uses its own CSS classes and variables (not Tailwind):

*   **Card Container**: `<div class="card" style="gap: 16px;">`
*   **Card Header**: `<div style="display: flex; justify-content: space-between;
    align-items: center; border-bottom: 1px solid var(--border); padding-bottom:
    12px;"><h2 class="section-title">Title</h2><span class="badge
    badge-primary">Label</span></div>`
*   **Structured Item Rows**: `<div style="display: flex; gap: 14px;
    align-items: flex-start; background: var(--bg); border: 1px solid
    var(--border); border-radius: 8px; padding: 14px;">`
*   **Badges**: `<span class="badge badge-warning">SPEND TREND</span>`, `<span
    class="badge badge-primary">PRIMARY DRIVERS</span>`, `<span class="badge
    badge-success">OPPORTUNITY</span>`
*   **Inline Code / Resource Names**: `<code
    class="code-pill">k8s_cluster</code>`
*   **Typography & Colors**:
    *   Primary text: `color: var(--text)`
    *   Muted notes: `<div style="font-size: 12px; color: var(--text-muted);
        margin-top: 4px;">`
    *   Accents: `#60a5fa` (blue), `#34d399` (emerald), `#fbbf24` (amber),
        `#ef4444` (red)

## Example

```html
<div class="card" style="gap: 16px;">
  <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 12px;">
    <h2 class="section-title">Executive Summary & Key Findings</h2>
    <span class="badge badge-primary">FinOps Assessment</span>
  </div>

  <div style="display: flex; flex-direction: column; gap: 12px;">
    <div style="display: flex; gap: 14px; align-items: flex-start; background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 14px;">
      <span class="badge badge-warning" style="flex-shrink: 0; margin-top: 1px;">SPEND TREND</span>
      <div style="font-size: 13px; line-height: 1.5; color: var(--text);">
        Project spend expanded from <strong style="color: var(--text);">$X.XX (Y GB)</strong> to peak at <strong style="color: #fbbf24;">$A.AA (B GB)</strong>, stabilizing at <strong>~$C/mo</strong>.
        <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">Note: Estimated at list prices (Log Storage $P/GiB after F GiB/month free; Vended Logs Storage $V/GiB).</div>
      </div>
    </div>

    <div style="display: flex; gap: 14px; align-items: flex-start; background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 14px;">
      <span class="badge badge-primary" style="flex-shrink: 0; margin-top: 1px;">PRIMARY DRIVERS</span>
      <div style="font-size: 13px; line-height: 1.5; color: var(--text);">
        <code class="code-pill">k8s_cluster</code> accounts for <strong style="color: #60a5fa;">50.3% ($X MTD)</strong> of ingestion.
      </div>
    </div>

    <div style="display: flex; gap: 14px; align-items: flex-start; background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 14px;">
      <span class="badge badge-success" style="flex-shrink: 0; margin-top: 1px;">OPPORTUNITY</span>
      <div style="font-size: 13px; line-height: 1.5; color: var(--text);">
        At least <strong style="color: #34d399;">X% (~$Y/mo)</strong> of spend is recoverable without losing signal; see the Cost Optimizer tab for each action and its filter.
      </div>
    </div>
  </div>
</div>
```
