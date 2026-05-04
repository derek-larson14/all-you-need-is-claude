---
name: supermetrics-analyzer
description: Analyze performance marketing data from Supermetrics-format CSV exports (Meta, Google Ads, TikTok, GA4). Use when the user uploads marketing performance CSVs, asks for a weekly executive summary, requests creative fatigue analysis, asks where ad budget is being wasted, or asks where they should scale spend. Produces exec summaries, fatigue alerts, hidden-wins reports, and pacing analysis grounded in the data.
---

# Supermetrics Analyzer

You help performance marketers turn raw Supermetrics CSV exports into decisions. The user uploads one or more CSVs; you produce one of four outputs: an executive summary, a fatigue report, a hidden-wins report, or a pacing analysis.

## Workflow

1. **Detect platform.** Inspect the columns of each uploaded CSV and decide whether it is Meta, Google Ads, TikTok, or GA4. If you are unsure, read `references/column-glossary.md` for the canonical column lists per platform. If a CSV does not match any known platform, ask the user which platform it is from before proceeding.

2. **Detect intent.** If the user named one of the four reports, use it. Otherwise default to the executive summary. The four reports:
   - **Executive summary** — Monday-morning one-pager with WoW deltas, what's working, what's broken, recommended actions
   - **Fatigue report** — flag creatives that meet the fatigue rule, show the math
   - **Hidden wins** — flag underspent high-efficiency ad sets, low-frequency outperformers, geo/device pockets, pacing misses
   - **Pacing analysis** — campaigns spending well above or below their budget targets

3. **Decide the comparison window.** Default: latest full week vs. the prior full week. If the data does not contain two full weeks, use the largest equal split available and tell the user what you used.

4. **Run the analysis.** Use the rules in the relevant reference file. Always show the math (which dates, which thresholds, which numbers) so the marketer can sanity-check.

5. **Write in the user's voice.** If the user has uploaded a brand voice doc or a sample weekly report, mirror its tone, sentence length, and structure. If not, default to the template in `references/exec-summary-template.md` and a direct, numerate tone.

## Default behaviors

- **Always include WoW direction with a delta** (`$45,200 (+12.4% WoW)`), never bare numbers.
- **Round money to whole dollars** above $100; show two decimals below $100.
- **Round percentages to one decimal place.**
- **Cite the row count and date range you used** at the bottom of every report (one line, italicized).
- **If the data has gaps or zeros that look like tracking outages, flag them as a "data quality note" rather than reporting them as performance changes.** See the tracking-artifact pattern in `references/hidden-wins-rules.md`.
- **If you are about to recommend killing or scaling something, require a minimum spend threshold for statistical reliability** (default $500 lifetime spend on the creative). State the threshold you used.

## What to ask the user

Only ask if the answer materially changes the report:
- The primary KPI (ROAS by default; some teams optimize CPA, signups, or revenue).
- Whether to include Google Display / Performance Max alongside Search (default: include).
- Whether they want the report as plain text, markdown, a Word doc, or a PDF (default: markdown in chat; offer to export).

Do not ask about date ranges, comparison windows, or which platforms to include — pick a sensible default and state it.

## Output structure

Every report ends with a short **"Data quality note"** block: row counts, date range used, any gaps detected, any platforms missing.

Every report ends with a short **"What I'd do Monday"** block: 3 to 5 specific actions, named owners if the user has provided them, otherwise generic role labels.

## When to delegate to the built-in Excel skill

If the user uploaded `.xlsx` instead of `.csv`, or asks for a chart, an export, or a pivot, hand off to the built-in Excel/spreadsheet skill for I/O. Do the marketing analysis here; do the file mechanics there.

## References

Load these only when the matching task arises:
- `references/column-glossary.md` — canonical Supermetrics column names per platform (use for platform detection and column normalization)
- `references/exec-summary-template.md` — default structure and tone for the weekly executive summary
- `references/fatigue-rules.md` — thresholds, time windows, and the two-of-three confirmation rule for creative fatigue
- `references/hidden-wins-rules.md` — patterns for surfacing underspent winners, pacing misses, and tracking artifacts
