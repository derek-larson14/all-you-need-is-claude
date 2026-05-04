# Creative Fatigue Rules

## Definition

A creative is fatigued when the audience has seen it enough that performance is declining. Detect early; the cost of running fatigued creatives compounds.

## Time windows

- **Baseline window:** trailing 14 days of the creative's life
- **Recent window:** trailing 3 days
- **Minimum age:** 7 days (don't flag creatives that haven't had time to stabilize)
- **Minimum spend:** $500 lifetime on the creative (don't flag noise)

## Signals

| Signal | Warning | Fatigue |
|---|---|---|
| Frequency (prospecting) | ≥ 2.5 | ≥ 3.0 |
| Frequency (retargeting) | ≥ 5.0 | ≥ 6.0 |
| CTR ratio (recent / baseline) | ≤ 0.85 | ≤ 0.75 |
| CPM ratio (recent / baseline) | ≥ 1.10 | ≥ 1.20 |
| ROAS ratio (recent / baseline) | ≤ 0.80 | ≤ 0.65 |

## Confirmation rule

Flag a creative as **fatigued** when **at least two** of the following are simultaneously true:
1. Frequency at or above the fatigue threshold
2. CTR ratio at or below 0.75
3. CPM ratio at or above 1.20

Single-signal triggers produce too many false positives. Two of three is the practitioner standard.

## Output format

For each fatigued creative, present:
- Campaign / Ad set / Ad name
- Days live, lifetime spend, lifetime ROAS
- The two or three signals that confirmed fatigue, with their numbers
- Recommended action (pause, refresh creative, narrow audience, move to retargeting)

Group by **confidence**:
- **High confidence** — three signals tripped
- **Medium confidence** — two signals tripped

## What this rule will NOT catch

- Sudden ad-account-wide drops (those are platform issues, not creative fatigue — flag separately)
- Seasonal effects (Black Friday, post-holiday lulls — note the date range)
- Audience saturation at the ad-set level (the creative may be fine; the audience is exhausted)

If the user asks about an ad set or campaign with multiple creatives all showing decline, escalate to "audience saturation" rather than per-creative fatigue.
