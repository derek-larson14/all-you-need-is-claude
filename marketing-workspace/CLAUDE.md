# Marketing Workspace

This is your workspace for the **All You Need Is Claude** workshop. Co-Work treats this folder as a project — Claude can see every file in it without you having to attach anything.

## What's here

- **`data/brand-book.docx`** — Brand guidelines for "Northwind Apparel," a fictional sustainable activewear brand. Both the brief generator and the content watcher read this as their reference. Edit it freely; the skills follow whatever's in it.
- **`data/sample-posts/`** — Seven pieces of marketing copy. Three on-brand, four off-brand (superlatives, greenwashing, off-voice slang, persona mismatch). Used by the content watcher.
- **`data/meta-ads-90d.csv`**, **`data/google-ads-90d.csv`**, **`data/tiktok-ads-90d.csv`** — Fake ad performance data, 90 days each. Used by the supermetrics analyzer.

## What you have access to

Three skills, loaded by the `core-marketing` plugin:

- **content-brief-generator** — turns a topic into a brand-aware content brief, then expands the brief into a writer-ready outline.
- **content-watcher** — checks marketing copy against the brand book and flags violations.
- **supermetrics-analyzer** — runs weekly summaries, fatigue checks, and hidden-wins reports against the ad data.

## How this file works

This file (`CLAUDE.md`) is read by Claude every time you start a chat in this workspace. It's how the workspace tells Claude what's here, what the skills do, and how you want to work. You can edit it — change the brand name from Northwind to your real brand, swap in your own data, add your team's conventions. The skills will pick up the changes automatically.

## After the workshop

Replace `data/brand-book.docx` with your real brand book. Drop your real ad exports into `data/`. Edit this file to match your team. The workspace becomes yours.
