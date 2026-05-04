# Column Glossary

Canonical Supermetrics CSV column names per platform. Real exports may differ slightly in casing, spacing, or pluralization depending on the user's report template. Match by intent, not exact string.

## Meta Ads

**Dimensions:**
`Date`, `Account name`, `Campaign name`, `Campaign objective`, `Ad set name`, `Ad name`

**Metrics:**
`Cost`, `Impressions`, `Reach`, `Frequency`, `Link clicks`, `Link CTR`, `CPM`, `Cost per link click`, `Purchases`, `Purchase conversion value`, `ROAS`

**Notes:**
- `Frequency = Impressions / Reach` — if missing, compute it.
- `Link CTR` is given as a percent (e.g. `1.85` means 1.85%, not 0.0185).
- `Purchase conversion value` is revenue.
- Fields may also appear with their API IDs (`adcampaign_name`, `cost`, `action_link_click`, `action_value_app_custom_event.fb_mobile_purchase`). Same meaning.

## Google Ads

**Dimensions:**
`Date`, `Account name`, `Campaign name`, `Ad group name`, `Network`, `Device`

**Metrics:**
`Cost`, `Impressions`, `Clicks`, `CTR`, `CPC`, `Conversions`, `Conversion value`, `Cost per conversion`, `Search impression share`, `ROAS`

**Notes:**
- `Search impression share` is on a 0..1 scale (e.g. `0.42`).
- `Network` values: `Search Network`, `Search Partners`, `Display Network`, `YouTube`, `Cross-network` (PMax).
- For PMax campaigns, asset-level breakdowns are not in standard exports.

## TikTok Ads

**Dimensions:**
`Date`, `Advertiser name`, `Campaign name`, `Ad group name`, `Ad name`

**Metrics:**
`Cost`, `Impressions`, `Clicks`, `CTR`, `CPM`, `CPC`, `Conversions`, `Video views`, `Video views at 75%`, `Video views at 100%`, `ROAS`

**Notes:**
- `CTR` given as a percent.
- Video completion rate = `Video views at 100%` / `Video views`. Use as a creative-quality signal.
- TikTok ROAS is consistently lower than Meta on the same brand. Don't compare cross-platform on raw ROAS — normalize against each platform's account average.

## GA4 (via Supermetrics)

**Dimensions:**
`date`, `sessionSource`, `sessionMedium`, `sessionSourceMedium`, `sessionCampaignName`, `deviceCategory`, `country`, `eventName`

**Metrics:**
`sessions`, `activeUsers`, `conversions`, `purchaseRevenue`, `engagementRate`, `bounceRate`

**Notes:**
- GA4 columns are camelCase, not human-label.
- Use to triangulate ad-platform conversions against site-side conversions when the two disagree.

## Platform detection rules

If the CSV contains:
- `Frequency` AND `Link CTR` → Meta
- `Search impression share` OR (`Network` AND `Ad group name`) → Google Ads
- `Video views at 100%` OR `Advertiser name` → TikTok
- `sessionSourceMedium` OR `engagementRate` → GA4

If multiple match or none match, ask the user.
