# Fatigue Check Prompt

Run inside the marketing workspace, in the same chat as the weekly summary. Paste:

---

Using the Supermetrics Analyzer skill, run a fatigue report on `data/meta-ads-90d.csv`.

Apply the standard rules in `references/fatigue-rules.md`: trailing 3-day vs trailing 14-day windows, minimum 7 days live, minimum $500 lifetime spend, two-of-three signal confirmation.

Group findings by **High confidence** (3 signals) and **Medium confidence** (2 signals). For each flagged creative, show:
- Campaign / Ad set / Ad name
- Days live, lifetime spend, lifetime ROAS
- The signals that tripped, with their numbers
- A specific recommended action

Then list one or two creatives in the **Watch list**: not yet fatigued but trending that way (one signal tripped).
