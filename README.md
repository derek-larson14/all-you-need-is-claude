# All You Need Is Claude — Workshop Bundle

The plugin and dummy data for the **All You Need Is Claude** workshop. Three skills you'll install in Claude Co-Work, plus realistic fake data to run them against. Bring your own data once you've seen it work.

**Workshop:** May 8, 2026 · Google Meet · 3 hours

---

## What's in here

```
.
├── .claude-plugin/marketplace.json     The Co-Work plugin marketplace manifest
├── plugins/core-marketing/             The plugin
│   ├── .claude-plugin/plugin.json
│   └── skills/
│       ├── content-brief-generator/    Brand-aware briefs and outlines
│       ├── content-watcher/            Brand consistency checker
│       └── supermetrics-analyzer/      Ad performance reports
├── marketing-workspace/                The workshop workspace (downloaded by attendees)
│   ├── CLAUDE.md                       Tells Claude what's in the workspace
│   └── data/
│       ├── brand-book.docx             Northwind Apparel brand guidelines
│       ├── sample-posts/               On-brand and off-brand sample copy
│       ├── meta-ads-90d.csv            90 days of Meta ads
│       ├── google-ads-90d.csv          90 days of Google
│       └── tiktok-ads-90d.csv          90 days of TikTok
├── prompts/
│   ├── content-brand/                  Workshop prompts for the brief and watcher skills
│   └── performance/                    Workshop prompts for the supermetrics skill
└── scripts/generate_data.py            Regenerate the ad CSVs if you want to customize
```

## Install (under 2 minutes)

The workshop walks you through this live, but here's the path:

1. **Download the workspace** zip from the [setup page](https://all-you-need-is-claude.vercel.app) or the latest GitHub release. Unzip it.
2. **Open Co-Work** and point the workspace at the unzipped folder. Claude can now see every file in there.
3. **Install the plugin:** Customize → Browse Plugins → Personal → Add marketplace from GitHub → paste `derek-larson14/all-you-need-is-claude` → install **core-marketing**.

## What the skills do

### content-brief-generator
You attach a brand book and name a topic. It produces a content brief — angle, headlines, key points, sources, voice notes, and a meta description. Re-prompt it with "expand into an outline" and it gives the writer section-level word counts, link suggestions, and a CTA. Brand voice and compliance rules come straight from the brand book; the skill self-checks before returning.

### content-watcher
You attach a brand book and any piece of copy (ad, post, email, draft). It returns a verdict (Approve / Revise / Hold), a flat list of issues with the offending phrase quoted and a suggested rewrite, plus a "what's working" note. Designed for agencies running 50+ campaigns where brand drift is the silent killer.

### supermetrics-analyzer
You drop in a Supermetrics CSV (Meta / Google / TikTok / GA4). It detects the platform, runs one of four reports — exec summary, fatigue, hidden wins, pacing — and shows the math behind every claim. Built around the standard two-of-three fatigue rule and a tracking-artifact detector.

All three skills are markdown. Open `plugins/core-marketing/skills/<skill>/SKILL.md` to read them. Edit the `references/` files to match your team's voice or thresholds.

## The dummy data

**Northwind Apparel** is a fictional sustainable activewear brand. Realistic enough to test against; clearly fake so you can break it without consequence.

- `marketing-workspace/data/brand-book.docx` — full brand guidelines: voice principles with do/don't pairs, banned words list, compliance rules (sustainability claim substantiation, banned medical claims), two personas, four messaging pillars.
- `marketing-workspace/data/sample-posts/` — three on-brand pieces (product launch, Instagram caption, restock email) and four off-brand pieces that violate specific rules (banned superlatives, unsubstantiated sustainability claims, off-voice slang, persona mismatch). Use these to drive the watcher.
- The three CSVs — 90 days of seeded ad data with six known scenarios for the supermetrics skill (a fatiguing creative, an underspent winner, a tracking gap, etc.). Regenerate with `python3 scripts/generate_data.py` (writes to `marketing-workspace/data/`).

## After the workshop

30 days of async support. Email Jack at **jack@3plus1.ai** with questions.

## License

MIT. Fork it, customize it, ship it inside your team.
