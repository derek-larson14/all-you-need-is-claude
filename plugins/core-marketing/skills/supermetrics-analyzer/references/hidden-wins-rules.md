# Hidden Wins & Negative Space

The most common failure mode in performance marketing is overspending on losers and underspending on winners. The exec summary surfaces both.

## Pattern 1: Underspent high-efficiency ad sets

**Rule:** ROAS at least 25% above account average AND average daily spend below 70% of the daily budget cap, sustained over the trailing 14 days.

**Why it matters:** the platform isn't spending the budget you allocated, meaning headroom exists. Either the audience is too narrow, the bid cap is too tight, or the creative isn't winning enough auctions despite high efficiency.

**Recommended action:** raise daily budget by 50%, broaden audience by one expansion (lookalike 1% → 2-3%), or remove the bid cap.

## Pattern 2: Low-frequency outperformers

**Rule:** Frequency below 1.5 AND ROAS at or above account median, with at least $500 lifetime spend.

**Why it matters:** the creative hasn't saturated its audience yet. Likely safe to scale.

**Recommended action:** duplicate the ad set with 2x budget, keep the original running for control.

## Pattern 3: Geo / device / placement pockets

**Rule:** A slice (country, device, placement) with ROAS at least 1.5x the account average AND spend share below 10% of total.

**Why it matters:** there's a pocket the algorithm hasn't pushed budget into.

**Recommended action:** carve a dedicated campaign for that slice.

## Pattern 4: Pacing misses

**Rule:** Campaign spending below 80% of its daily budget for at least 5 of the last 7 days, while CPA is at or below target.

**Why it matters:** efficient spend the platform isn't fully delivering. Audience is too narrow or the bid is losing auctions.

**Recommended action:** expand audience or raise the bid cap. Don't increase budget — that won't help if delivery is the bottleneck.

## Pattern 5: Tracking artifacts (the head-fake)

**Rule:** Sudden zero or near-zero conversions on a campaign for 1-3 consecutive days, while spend, impressions, and clicks remain normal.

**Why it matters:** this is almost always a tracking outage, a pixel/SDK issue, or a CAPI hiccup — not a real performance drop. If you treat it as performance, you'll pause a working campaign.

**Recommended action:** flag as a **data quality note**, not a performance change. Recommend the user verify with their analytics or platform-side conversions.

## Pattern 6: Genuine losers

**Rule:** ROAS below 0.8x for at least 14 days with at least $1,000 lifetime spend.

**Why it matters:** these don't fix themselves. The longer they run, the more budget gets diverted from winners.

**Recommended action:** pause. If the user is testing for learnings, set a hard kill threshold ($500 more spend or 7 more days, whichever first).

## Output format

Group hidden wins under four headers:
- **Scale these** (patterns 1, 2, 3)
- **Fix delivery** (pattern 4)
- **Data quality** (pattern 5)
- **Cut these** (pattern 6)

For each item, show the rule that triggered, the numbers, and a one-line recommended action.
