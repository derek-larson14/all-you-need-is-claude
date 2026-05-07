# Weekly Summary Prompt

Run inside the marketing workspace (Claude can see the ad CSVs in `data/` automatically). Paste:

---

Using the Supermetrics Analyzer skill, produce my weekly executive summary from the ad data in `data/`.

Compare the most recent full week to the prior full week. Use ROAS as the primary KPI. Include all platforms.

Format the output:
- **TL;DR** at the very top — three bullets, one sentence each, leading with direction (up/down/flat).
- **Body in tables** — headline KPIs, channel breakdown, what's working, what's broken. No paragraph blurbs in the body.
- End with the "What I'd do Monday" block (3-5 specific actions with named campaigns or creatives).
- End with the "Data quality note."

Match this voice: direct, numerate, no hedging.
