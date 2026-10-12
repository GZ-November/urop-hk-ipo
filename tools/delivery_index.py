# ==============================================================================
# Delivery Index and Visual Entry Point Generator
# ==============================================================================
"""Generate self-contained HTML entry page, machine-readable index, and delivery README."""
from __future__ import annotations

import datetime as dt
import html
from pathlib import Path
from typing import Any


def _escape(val: Any) -> str:
    """Safely escape text for HTML embedding and neutralize formula execution."""
    if val is None:
        return ""
    text = str(val).strip()
    return html.escape(text, quote=True)


def _safe_rel(target: Path | str | None, base: Path | None = None) -> str:
    """Format a relative link safely using forward slashes and HTML attribute escaping."""
    if not target:
        return "#"
    raw_str = str(target).strip()
    if raw_str.lower().startswith(("javascript:", "data:", "vbscript:")):
        return "#"
    path_obj = Path(raw_str)
    if base and path_obj.is_absolute():
        try:
            rel = path_obj.relative_to(base)
            res_str = str(rel).replace("\\", "/")
        except ValueError:
            try:
                import os
                rel_str = os.path.relpath(str(path_obj), str(base))
                res_str = rel_str.replace("\\", "/")
            except ValueError:
                res_str = str(path_obj.name)
    else:
        res_str = str(path_obj).replace("\\", "/")
    return html.escape(res_str, quote=True)


def generate_start_here_html(
    *,
    title: str,
    status: str,
    is_analysis_ready: bool,
    cohorts: list[dict[str, Any]],
    resume_command: str | None = None,
    work_orders_path: str | Path | None = None,
    bundle_zip_path: str | Path | None = None,
    error_message: str | None = None,
    is_bundle: bool = False,
    base_dir: Path | None = None,
) -> str:
    """Generate self-contained English START_HERE.html report."""
    now_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Status badges and banners
    if status == "ANALYSIS-READY":
        status_badge = '<span class="badge badge-success">ANALYSIS-READY</span>'
        banner_class = "banner-success"
        banner_title = "Reviewed Disclosures & Reconciliation Passed"
        banner_text = (
            "All configured disclosure fields, deterministic extractions, and independent review "
            "gates have passed. Clean CSV, Excel workbook, and Codebook are reconciled with original source hashes. "
            "Note: Passing disclosure gates does not certify uncollected optional market/event horizons or arbitrary econometric specifications."
        )
    elif status == "WORK_PENDING":
        status_badge = (
            '<span class="badge badge-warning">WORK PENDING</span> '
            '<span class="badge badge-danger">NOT ANALYSIS-READY</span>'
        )
        banner_class = "banner-warning"
        banner_title = "Work Pending: Extraction & Independent Review Required"
        banner_text = (
            "Official listing reports and document packets have been prepared, but formal "
            "extractions or independent review credentials remain required. "
            "<strong>Do NOT treat this dataset as completed data.</strong> "
            "Follow the actionable work orders below and resume collection."
        )
    elif status == "FAILED":
        status_badge = (
            '<span class="badge badge-danger">FAILED</span> '
            '<span class="badge badge-danger">NOT ANALYSIS-READY</span>'
        )
        banner_class = "banner-danger"
        banner_title = "Collection Run Failed"
        banner_text = (
            "The collection run encountered an error or official report coverage gap. "
            "Review diagnostic output below. Stale or fabricated success is strictly forbidden."
        )
    else:  # LEGACY_GAPS
        status_badge = (
            '<span class="badge badge-info">LEGACY / GAPS DETECTED</span> '
            '<span class="badge badge-warning">NOT ANALYSIS-READY</span>'
        )
        banner_class = "banner-info"
        banner_title = "Legacy Snapshot Notice"
        banner_text = (
            "This snapshot contains legacy unreviewed columns or documented evidence gaps. "
            "Passing code checks is not semantic certification. Review audit reports before analysis."
        )

    # Deliverables table rows
    cohort_rows = []
    total_issuers = sum(c.get("issuers", 0) for c in cohorts)
    for c in cohorts:
        cid = _escape(c.get("id", ""))
        cboard = _escape(c.get("board", "Main Board"))
        period = c.get("requested_period") or c.get("period") or ["Unknown", "Unknown"]
        period_str = f"{_escape(period[0])} to {_escape(period[1])}"
        n_issuers = c.get("issuers", 0)
        c_ready = c.get("is_analysis_ready", c.get("fully_reviewed_and_aligned", False))
        c_badge = (
            '<span class="badge badge-success">ANALYSIS-READY</span>'
            if c_ready
            else '<span class="badge badge-warning">PENDING GATES</span>'
        )

        wb_link = _safe_rel(c.get("workbook"), base_dir)
        csv_link = _safe_rel(c.get("csv"), base_dir)
        cb_md_link = _safe_rel(c.get("codebook_md"), base_dir)
        cb_json_link = _safe_rel(c.get("codebook_json"), base_dir)
        audit_md_link = _safe_rel(c.get("audit_md"), base_dir)
        status_link = _safe_rel(c.get("status_json"), base_dir)
        evidence_link = _safe_rel(c.get("evidence_dir"), base_dir)

        # Audit stats
        audit_stats = c.get("audit_stats", {})
        stat_summary_parts = []
        for target_name, tstats in audit_stats.items():
            if isinstance(tstats, dict):
                matches = tstats.get("matches_with_value", 0)
                missing = tstats.get("both_missing", 0)
                disc = (
                    tstats.get("value_mismatch", 0)
                    + tstats.get("excel_missing", 0)
                    + tstats.get("json_missing", 0)
                )
                stat_summary_parts.append(
                    f"<strong>{_escape(target_name)}</strong>: {matches} matched, {missing} both missing, {disc} discrepancies"
                )
        stat_str = "<br>".join(stat_summary_parts) if stat_summary_parts else "Pending audit execution"

        cohort_rows.append(f"""
        <tr>
          <td><strong>{cid}</strong><br><small>{cboard}</small></td>
          <td>{period_str}</td>
          <td style="text-align:center;">{n_issuers}</td>
          <td style="text-align:center;">{c_badge}</td>
          <td>
            <a class="file-link" href="{wb_link}">Excel (.xlsx)</a> |
            <a class="file-link" href="{csv_link}">Clean CSV</a><br>
            <a class="file-link" href="{cb_md_link}">Codebook (MD)</a> |
            <a class="file-link" href="{cb_json_link}">JSON</a><br>
            <a class="file-link" href="{audit_md_link}">Audit Report</a> |
            <a class="file-link" href="{status_link}">Status</a> |
            <a class="file-link" href="{evidence_link}">Evidence</a>
          </td>
          <td><small>{stat_str}</small></td>
        </tr>
        """)
    cohorts_tbody = "".join(cohort_rows)

    # Work orders / resume section
    work_order_html = ""
    if status == "WORK_PENDING" or resume_command:
        wo_link = _safe_rel(work_orders_path, base_dir) if work_orders_path else "#"
        cmd_escaped = _escape(resume_command or "python3 run.py start --resume")
        work_order_html = f"""
        <div class="section-card">
          <h2>Actionable Agent Work Orders & Resume Operation</h2>
          <p>
            Extraction or review is pending. Review work orders and source packets below,
            complete supported extractions and independent reviews, then run the exact resume command:
          </p>
          <div style="margin: 12px 0;">
            <a class="action-btn" href="{wo_link}">Open Work Orders (JSON)</a>
          </div>
          <h3>Exact Resume Command</h3>
          <div class="code-box"><code>{cmd_escaped}</code></div>
          <p><small>Note: Reruns safely reuse the preserved cohort configuration and will not overwrite unrelated runs or fabricate approvals.</small></p>
        </div>
        """

    # Error message section
    error_html = ""
    if error_message:
        error_html = f"""
        <div class="section-card" style="border-left: 4px solid #dc2626;">
          <h2 style="color: #dc2626;">Failure Diagnostics</h2>
          <pre class="code-box" style="white-space: pre-wrap; color: #fecaca;">{_escape(error_message)}</pre>
        </div>
        """

    # Company inventory table (if provided in cohorts)
    company_rows = []
    for c in cohorts:
        cid = _escape(c.get("id", ""))
        for comp in c.get("companies", []):
            code = _escape(comp.get("code", ""))
            name = _escape(comp.get("name", ""))
            ldate = _escape(comp.get("listing_date", "Pending"))
            p_stat = _escape(comp.get("prospectus_status", "Pending"))
            a_stat = _escape(comp.get("allot_status", "Pending"))
            company_rows.append(f"""
            <tr>
              <td><code>{code}</code></td>
              <td>{name}</td>
              <td>{cid}</td>
              <td>{ldate}</td>
              <td>{p_stat}</td>
              <td>{a_stat}</td>
            </tr>
            """)
    companies_table_html = ""
    if company_rows:
        companies_tbody = "".join(company_rows)
        companies_table_html = f"""
        <div class="section-card">
          <h2>Issuer Inventory & Gate Verification ({len(company_rows)} issuers)</h2>
          <div style="overflow-x: auto;">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Code</th>
                  <th>Company Name</th>
                  <th>Cohort</th>
                  <th>Listing Date</th>
                  <th>Prospectus Gate</th>
                  <th>Allotment Gate</th>
                </tr>
              </thead>
              <tbody>
                {companies_tbody}
              </tbody>
            </table>
          </div>
        </div>
        """

    # Primary deliverable files table (for bundle / run directory)
    readme_link = "README.md"
    index_link = "index.json"
    quality_link = "quality_summary.json" if is_bundle else "run_state.json"
    manifest_link = "manifest.json" if is_bundle else "#"
    manifest_row = (
        f'<tr><td><a class="file-link" href="{manifest_link}">manifest.json</a></td>'
        f"<td>SHA-256 evidence integrity manifest of all archive contents</td></tr>"
        if is_bundle
        else ""
    )

    bundle_download_html = ""
    if bundle_zip_path:
        zip_rel = _safe_rel(bundle_zip_path, base_dir)
        bundle_download_html = f"""
        <div style="margin: 16px 0;">
          <a class="action-btn" href="{zip_rel}">Download Complete Delivery ZIP ({_escape(Path(bundle_zip_path).name)})</a>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{_escape(title)}</title>
  <style>
    :root {{
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #334155;
      --heading: #0f172a;
      --border: #e2e8f0;
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --success-bg: #ecfdf5;
      --success-border: #a7f3d0;
      --success-text: #065f46;
      --warning-bg: #fffbeb;
      --warning-border: #fde68a;
      --warning-text: #92400e;
      --danger-bg: #fef2f2;
      --danger-border: #fecaca;
      --danger-text: #991b1b;
      --info-bg: #eef2ff;
      --info-border: #c7d2fe;
      --info-text: #3730a3;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.5;
      color: var(--text);
      background-color: var(--bg);
      margin: 0;
      padding: 24px 16px;
    }}
    .container {{
      max-width: 1080px;
      margin: 0 auto;
    }}
    header {{
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border);
    }}
    h1 {{
      font-size: 1.75rem;
      color: var(--heading);
      margin: 0 0 8px 0;
    }}
    .meta-bar {{
      font-size: 0.875rem;
      color: #64748b;
    }}
    .badge {{
      display: inline-block;
      padding: 3px 8px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      border-radius: 4px;
      letter-spacing: 0.5px;
    }}
    .badge-success {{ background: var(--success-bg); color: var(--success-text); border: 1px solid var(--success-border); }}
    .badge-warning {{ background: var(--warning-bg); color: var(--warning-text); border: 1px solid var(--warning-border); }}
    .badge-danger  {{ background: var(--danger-bg);  color: var(--danger-text);  border: 1px solid var(--danger-border); }}
    .badge-info    {{ background: var(--info-bg);    color: var(--info-text);    border: 1px solid var(--info-border); }}
    .banner {{
      padding: 16px;
      border-radius: 6px;
      margin-bottom: 24px;
      font-size: 0.95rem;
    }}
    .banner-success {{ background: var(--success-bg); border-left: 4px solid #10b981; color: var(--success-text); }}
    .banner-warning {{ background: var(--warning-bg); border-left: 4px solid #f59e0b; color: var(--warning-text); }}
    .banner-danger  {{ background: var(--danger-bg);  border-left: 4px solid #ef4444; color: var(--danger-text); }}
    .banner-info    {{ background: var(--info-bg);    border-left: 4px solid #6366f1; color: var(--info-text); }}
    .section-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 24px;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }}
    .section-card h2 {{
      font-size: 1.2rem;
      color: var(--heading);
      margin-top: 0;
      margin-bottom: 12px;
      border-bottom: 1px solid #f1f5f9;
      padding-bottom: 8px;
    }}
    .section-card h3 {{
      font-size: 1rem;
      color: var(--heading);
      margin-top: 16px;
      margin-bottom: 8px;
    }}
    .policy-box {{
      background: #f0fdf4;
      border-left: 4px solid #059669;
      padding: 14px;
      border-radius: 4px;
      margin: 16px 0;
      font-size: 0.9rem;
    }}
    .policy-box h3 {{ color: #065f46; margin: 0 0 6px 0; font-size: 0.95rem; }}
    .policy-box ul {{ margin: 0; padding-left: 20px; }}
    .boundary-box {{
      background: #f8fafc;
      border-left: 4px solid #475569;
      padding: 12px;
      border-radius: 4px;
      margin: 16px 0;
      font-size: 0.875rem;
    }}
    .boundary-box h3 {{ color: #1e293b; margin: 0 0 4px 0; font-size: 0.9rem; }}
    .code-box {{
      background: #0f172a;
      color: #f8fafc;
      padding: 12px 16px;
      border-radius: 6px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.875rem;
      overflow-x: auto;
    }}
    .action-btn {{
      display: inline-block;
      background: var(--primary);
      color: #ffffff;
      padding: 8px 16px;
      text-decoration: none;
      border-radius: 4px;
      font-weight: 600;
      font-size: 0.875rem;
    }}
    .action-btn:hover {{ background: var(--primary-hover); }}
    .data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.875rem;
      margin: 12px 0;
    }}
    .data-table th, .data-table td {{
      padding: 10px 12px;
      text-align: left;
      border-bottom: 1px solid var(--border);
    }}
    .data-table th {{
      background: #f8fafc;
      color: #475569;
      font-weight: 600;
    }}
    .data-table tr:hover {{ background: #f8fafc; }}
    .file-link {{
      color: var(--primary);
      text-decoration: none;
      font-weight: 500;
    }}
    .file-link:hover {{ text-decoration: underline; }}
    footer {{
      margin-top: 32px;
      padding-top: 16px;
      border-top: 1px solid var(--border);
      font-size: 0.8rem;
      color: #94a3b8;
      text-align: center;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>{_escape(title)}</h1>
      <div class="meta-bar">
        Generated: {now_utc} &bull; Total Issuers: {total_issuers} &bull; Status: {status_badge}
      </div>
    </header>

    <div class="banner {banner_class}">
      <h3 style="margin: 0 0 4px 0;">{banner_title}</h3>
      <div>{banner_text}</div>
    </div>

    {bundle_download_html}
    {error_html}
    {work_order_html}

    <div class="section-card">
      <h2>Deliverables & Cohort Summary</h2>
      <div style="overflow-x: auto;">
        <table class="data-table">
          <thead>
            <tr>
              <th>Cohort & Board</th>
              <th>Listing Range</th>
              <th style="text-align:center;">Issuers</th>
              <th style="text-align:center;">Readiness</th>
              <th>Files & Documentation</th>
              <th>Audit & Coverage Metrics</th>
            </tr>
          </thead>
          <tbody>
            {cohorts_tbody}
          </tbody>
        </table>
      </div>

      <div class="policy-box">
        <h3>Missing Data Policy vs. Observed Zero</h3>
        <p>Econometric integrity requires strict distinction between unobserved data and empirical zeros:</p>
        <ul>
          <li><strong>NaN / NA (Missing / Unobserved):</strong> Indicates unobserved disclosures, omitted reporting items, or unmatured post-IPO event windows (e.g. 180-day lockup when the observation cutoff precedes maturity). Missing values are strictly preserved and <em>never substituted with zero</em>.</li>
          <li><strong>0 / 0.0 (Empirically Observed Zero):</strong> Indicates a measured, source-verified zero value (e.g. zero clawback shares reallocated, zero cornerstone investors disclosed, zero greenshoe exercise).</li>
        </ul>
      </div>

      <div class="boundary-box">
        <h3>Sample Boundaries & Coverage Rules</h3>
        <p>
          Includes ordinary IPOs listed on the Hong Kong Stock Exchange within the specified interval.
          Explicitly excluded: transfers from GEM to Main Board, SPAC listings, De-SPAC transactions, and listings by introduction.
        </p>
      </div>
    </div>

    <div class="section-card">
      <h2>Package Navigation Index</h2>
      <table class="data-table">
        <thead>
          <tr>
            <th>File</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><a class="file-link" href="START_HERE.html">START_HERE.html</a></td>
            <td>Interactive visual entry point, quality reports, and gate status (this page)</td>
          </tr>
          <tr>
            <td><a class="file-link" href="{readme_link}">README.md</a></td>
            <td>Concise English overview, folder layout, and dataset usage instructions</td>
          </tr>
          <tr>
            <td><a class="file-link" href="{index_link}">index.json</a></td>
            <td>Machine-readable deliverables index and cohort metadata</td>
          </tr>
          <tr>
            <td><a class="file-link" href="{quality_link}">{quality_link}</a></td>
            <td>Quality summary, audit statistics, and gate reconciliation details</td>
          </tr>
          {manifest_row}
        </tbody>
      </table>
    </div>

    {companies_table_html}

    <footer>
      Hong Kong IPO Pipeline Toolkit &bull; Deterministic Extraction & Econometric Evidence &bull; Preserves Source Truth
    </footer>
  </div>
</body>
</html>
"""


def generate_index_json(
    *,
    title: str,
    status: str,
    is_analysis_ready: bool,
    cohorts: list[dict[str, Any]],
    base_dir: Path | None = None,
) -> dict[str, Any]:
    """Generate structured machine-readable index dictionary."""
    clean_cohorts = []
    for c in cohorts:
        cid = c.get("id", "")
        period = c.get("requested_period") or c.get("period") or []
        files = {
            "workbook": _safe_rel(c.get("workbook"), base_dir),
            "csv": _safe_rel(c.get("csv"), base_dir),
            "codebook_md": _safe_rel(c.get("codebook_md"), base_dir),
            "codebook_json": _safe_rel(c.get("codebook_json"), base_dir),
            "audit_md": _safe_rel(c.get("audit_md"), base_dir),
            "status_json": _safe_rel(c.get("status_json"), base_dir),
            "evidence_dir": _safe_rel(c.get("evidence_dir"), base_dir),
        }
        clean_cohorts.append({
            "id": cid,
            "board": c.get("board", "Main Board"),
            "period": period,
            "issuers": c.get("issuers", 0),
            "is_analysis_ready": c.get("is_analysis_ready", c.get("fully_reviewed_and_aligned", False)),
            "files": files,
            "audit_stats": c.get("audit_stats", {}),
        })

    return {
        "title": title,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "overall_status": status,
        "is_analysis_ready": is_analysis_ready,
        "folder_layout": {
            "START_HERE.html": "Self-contained interactive visual entry point & quality report",
            "README.md": "Concise delivery documentation and relative links",
            "index.json": "Machine-readable data/output index",
            "quality_summary.json": "Audit stats, gate checks, and coverage summary",
            "manifest.json": "SHA-256 evidence integrity manifest",
            "instructions/": "Agent instructions and board documentation",
            "cohorts/": "Per-cohort research workbooks, clean CSVs, codebooks, audit reports, and evidence",
        },
        "cohorts": clean_cohorts,
    }


def generate_delivery_readme(
    *,
    title: str,
    status: str,
    is_analysis_ready: bool,
    cohorts: list[dict[str, Any]],
    is_bundle: bool = True,
    base_dir: Path | None = None,
) -> str:
    """Generate concise delivery README.md."""
    status_label = "ANALYSIS-READY" if is_analysis_ready else f"NOT ANALYSIS-READY ({status})"
    lines = [
        f"# {title}",
        "",
        f"**Status: {status_label}**",
        "",
        "Open **[START_HERE.html](START_HERE.html)** for the interactive guide, complete file index,",
        "reconciliation statistics, and gate verification badges.",
        "",
        "## Standard Folder Layout",
        "",
        "```text",
        "├── START_HERE.html           # Interactive visual entry point & quality report",
        "├── README.md                 # Concise guide & folder layout (this file)",
        "├── index.json                # Machine-readable deliverable index",
        "├── quality_summary.json      # Audit metrics, gate status & maturity summary",
        "├── manifest.json             # SHA-256 evidence integrity manifest (in ZIP releases)",
        "├── instructions/             # Agent & research instructions",
        "└── cohorts/",
        "    └── <cohort_id>/          # Per-cohort data, evidence & codebooks",
        "        ├── <stem>.xlsx       # Research Excel workbook",
        "        ├── <stem>.csv        # Analysis-ready clean CSV",
        "        ├── codebook.md/json  # Academic variable dictionary",
        "        ├── audit.md/json     # Reconciliation & discrepancy report",
        "        ├── status.json       # Field gate alignment status",
        "        └── evidence/         # Extraction payloads & independent review records",
        "```",
        "",
        "## Missing Data Policy vs. Observed Zero",
        "",
        "- **`NaN` / `NA` / Blank (Missing / Unobserved):** Indicates unobserved disclosures, omitted",
        "  reporting items, or unmatured post-IPO event windows (e.g. 180-day lockup before cutoff).",
        "  Missing values are strictly preserved and **never substituted with zero**.",
        "- **`0` / `0.0` (Empirically Observed Zero):** Indicates an empirically verified, disclosed zero value",
        "  (e.g., zero clawback shares reallocated, zero cornerstone investors, zero greenshoe exercise).",
        "",
        "## Cohort Deliverables",
        "",
    ]

    for c in cohorts:
        cid = c.get("id", "")
        cboard = c.get("board", "Main Board")
        period = c.get("requested_period") or c.get("period") or ["Unknown", "Unknown"]
        n_iss = c.get("issuers", 0)
        c_ready = c.get("is_analysis_ready", c.get("fully_reviewed_and_aligned", False))
        label = "ANALYSIS-READY" if c_ready else "PENDING GATES"
        csv_link = _safe_rel(c.get("csv"), base_dir)
        wb_link = _safe_rel(c.get("workbook"), base_dir)
        cb_link = _safe_rel(c.get("codebook_md"), base_dir)

        lines.append(f"### {cid} ({cboard}) - [{label}]")
        lines.append(f"- **Listing interval:** {period[0]} to {period[1]}")
        lines.append(f"- **Issuers:** {n_iss}")
        lines.append(f"- **Clean CSV:** [{Path(csv_link).name}]({csv_link})")
        lines.append(f"- **Excel Workbook:** [{Path(wb_link).name}]({wb_link})")
        lines.append(f"- **Codebook:** [{Path(cb_link).name}]({cb_link})")
        lines.append("")

    lines.extend([
        "## Sample Boundaries & Coverage Rules",
        "",
        "Includes ordinary IPOs listed on the Hong Kong Stock Exchange within the specified interval.",
        "Excludes GEM transfers to Main Board, SPAC listings, De-SPAC transactions, and listings by introduction.",
        "",
        "---",
        "Hong Kong IPO Research Toolkit &bull; Deterministic Extraction & Econometric Evidence",
    ])
    return "\n".join(lines) + "\n"
