"""
Generate 90 days of synthetic Supermetrics-format CSV exports for the
"All You Need Is Claude" workshop.

Brand: Northwind Apparel (DTC apparel, mid-market, ~$2M annual ad spend)
Date range: 2026-01-30 -> 2026-04-29 (90 days, ending the day before workshop)
Platforms: Meta, Google Ads, TikTok

Seeded scenarios (the demo "wow moments"):
  1. Fatiguing creative on Meta: Spring-Prospecting-Q2 / Lookalike-1pct / Video-Hero-A
  2. Hidden winner (underspent): Meta Interest-Sustainability ad set, $40/day cap, ROAS 4.2x
  3. Hidden winner (placement): TikTok UGC-Customer-Review-3 strong CTR/ROAS at low spend
  4. Tracking artifact: Google branded campaign 3-day conversion gap (2026-04-19 to 2026-04-21)
  5. Pacing miss: Meta Retargeting-Cart-Abandoners spends only ~60% of $300/day budget
  6. Genuine loser: Meta Cold-Broad-Test-2 ROAS ~0.6x throughout

Output: marketing-workspace/data/{meta,google,tiktok}-ads-90d.csv
"""

from __future__ import annotations
import csv
import os
import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

random.seed(42)  # reproducible across regenerations

START = date(2026, 1, 30)
DAYS = 90
END = START + timedelta(days=DAYS - 1)

OUT = Path(__file__).resolve().parent.parent / "marketing-workspace" / "data"
OUT.mkdir(parents=True, exist_ok=True)


# ---------- helpers ----------
def jitter(value: float, pct: float = 0.15) -> float:
    return value * (1 + random.uniform(-pct, pct))


def weekend_factor(d: date) -> float:
    return 0.88 if d.weekday() >= 5 else 1.0


def cpm_drift(day_index: int) -> float:
    # ~10% rise across 90 days
    return 1.0 + 0.10 * (day_index / DAYS)


def round2(x: float) -> float:
    return round(x, 2)


def round_int(x: float) -> int:
    return max(0, int(round(x)))


# ---------- META ----------
@dataclass
class MetaAd:
    campaign: str
    objective: str
    adset: str
    ad: str
    daily_budget: float
    base_ctr: float       # decimal, e.g. 0.015
    base_cpm: float       # USD
    base_roas: float
    base_freq: float
    cap_factor: float = 1.0  # how much of daily_budget actually spends, 0..1

META_PORTFOLIO: list[MetaAd] = [
    # Campaign 1: Spring prospecting (contains the FATIGUING ad)
    MetaAd("Spring-Prospecting-Q2", "Conversions", "Lookalike-1pct", "Video-Hero-A",
           daily_budget=180, base_ctr=0.019, base_cpm=15.5, base_roas=3.1, base_freq=1.6),
    MetaAd("Spring-Prospecting-Q2", "Conversions", "Lookalike-1pct", "Static-Carousel-B",
           daily_budget=120, base_ctr=0.014, base_cpm=15.0, base_roas=2.4, base_freq=1.4),
    MetaAd("Spring-Prospecting-Q2", "Conversions", "Broad-25-54-F", "Video-UGC-C",
           daily_budget=140, base_ctr=0.013, base_cpm=14.8, base_roas=2.1, base_freq=1.7),

    # Campaign 2: Interest-based (contains HIDDEN WINNER #1)
    MetaAd("Interest-Targeting-Q2", "Conversions", "Interest-Sustainability", "Static-Brand-D",
           daily_budget=40, base_ctr=0.021, base_cpm=14.0, base_roas=4.2, base_freq=1.3, cap_factor=1.0),
    MetaAd("Interest-Targeting-Q2", "Conversions", "Interest-Outdoor-Active", "Video-Lifestyle-E",
           daily_budget=90, base_ctr=0.012, base_cpm=15.2, base_roas=1.8, base_freq=2.1),

    # Campaign 3: Retargeting (PACING MISS — only spends ~60% of budget)
    MetaAd("Retargeting-Cart-Abandoners", "Conversions", "Cart-Abandon-7d", "Dynamic-Product-F",
           daily_budget=300, base_ctr=0.028, base_cpm=16.0, base_roas=5.4, base_freq=2.4, cap_factor=0.60),
    MetaAd("Retargeting-Cart-Abandoners", "Conversions", "Site-Visitors-30d", "Static-Reminder-G",
           daily_budget=160, base_ctr=0.024, base_cpm=15.5, base_roas=4.1, base_freq=2.2, cap_factor=0.65),

    # Campaign 4: Cold testing (GENUINE LOSER)
    MetaAd("Cold-Broad-Test-2", "Conversions", "Broad-18-65", "Test-Creative-H",
           daily_budget=120, base_ctr=0.008, base_cpm=14.5, base_roas=0.6, base_freq=1.5),
    MetaAd("Cold-Broad-Test-2", "Conversions", "Broad-18-65", "Test-Creative-I",
           daily_budget=110, base_ctr=0.009, base_cpm=14.2, base_roas=0.7, base_freq=1.4),

    # Campaign 5: Brand awareness
    MetaAd("Brand-Awareness-Q2", "Reach", "Top-of-Funnel-Broad", "Brand-Anthem-J",
           daily_budget=100, base_ctr=0.011, base_cpm=12.5, base_roas=1.4, base_freq=1.9),
    MetaAd("Brand-Awareness-Q2", "Reach", "Top-of-Funnel-Broad", "Brand-Story-K",
           daily_budget=80, base_ctr=0.010, base_cpm=12.8, base_roas=1.3, base_freq=2.0),
]


def fatigue_curve(ad: MetaAd, day_index: int) -> tuple[float, float, float, float]:
    """Return (ctr_mult, cpm_mult, roas_mult, freq_mult) for ad on a given day."""
    if ad.ad == "Video-Hero-A":
        # Strong days 1-44, gradual decline 45-75, sharp collapse days 76-89.
        # Two-phase curve so trailing 3d vs 14d catches the acceleration.
        if day_index < 45:
            return (1.0, 1.0, 1.0, 1.0)
        if day_index < 76:
            progress = (day_index - 44) / 31  # 0 -> 1 over days 45-75
            return (
                1.0 - 0.30 * progress,   # CTR -> 0.70x by day 75
                1.0 + 0.08 * progress,   # CPM +8% by day 75
                1.0 - 0.35 * progress,   # ROAS -> 0.65x
                1.0 + 0.65 * progress,   # Freq -> 1.65x base = ~2.65
            )
        progress = (day_index - 75) / 14  # 0 -> 1 over days 76-89 (the collapse)
        return (
            0.70 * (1.0 - 0.50 * progress),   # CTR collapses to 0.35x base
            1.08 * (1.0 + 0.25 * progress),   # CPM +35% from baseline by end
            0.65 * (1.0 - 0.45 * progress),   # ROAS to ~0.36x
            1.65 * (1.0 + 0.45 * progress),   # Freq to ~2.4x base = ~3.85
        )
    return (1.0, 1.0, 1.0, 1.0)


def gen_meta() -> list[dict]:
    rows = []
    for i in range(DAYS):
        d = START + timedelta(days=i)
        wf = weekend_factor(d)
        drift = cpm_drift(i)
        for ad in META_PORTFOLIO:
            ctr_m, cpm_m, roas_m, freq_m = fatigue_curve(ad, i)
            spend = jitter(ad.daily_budget * ad.cap_factor * wf, 0.10)
            cpm = jitter(ad.base_cpm * drift * cpm_m, 0.08)
            impressions = (spend / cpm) * 1000
            ctr = max(0.001, jitter(ad.base_ctr * ctr_m, 0.12))
            link_clicks = impressions * ctr
            frequency = max(1.0, jitter(ad.base_freq * freq_m, 0.08))
            reach = impressions / frequency
            cplc = spend / max(link_clicks, 1)
            roas = max(0.0, jitter(ad.base_roas * roas_m, 0.10))
            revenue = spend * roas
            # purchases ~ revenue / AOV; AOV ~$65 for apparel, jittered
            aov = jitter(65, 0.15)
            purchases = revenue / aov
            rows.append({
                "Date": d.isoformat(),
                "Account name": "Northwind Apparel",
                "Campaign name": ad.campaign,
                "Campaign objective": ad.objective,
                "Ad set name": ad.adset,
                "Ad name": ad.ad,
                "Daily budget": round2(ad.daily_budget),
                "Cost": round2(spend),
                "Impressions": round_int(impressions),
                "Reach": round_int(reach),
                "Frequency": round(frequency, 2),
                "Link clicks": round_int(link_clicks),
                "Link CTR": round(ctr * 100, 3),  # as percent
                "CPM": round2(cpm),
                "Cost per link click": round2(cplc),
                "Purchases": round_int(purchases),
                "Purchase conversion value": round2(revenue),
                "ROAS": round(roas, 2),
            })
    return rows


# ---------- GOOGLE ADS ----------
@dataclass
class GoogleCampaign:
    campaign: str
    adgroup: str
    network: str
    device: str
    daily_budget: float
    base_ctr: float
    base_cpc: float
    base_cvr: float
    base_aov: float
    impression_share: float

GOOGLE_PORTFOLIO: list[GoogleCampaign] = [
    GoogleCampaign("Brand-Search", "Brand-Exact", "Search Network", "Mobile",
                   daily_budget=120, base_ctr=0.18, base_cpc=0.85, base_cvr=0.14, base_aov=72,
                   impression_share=0.92),
    GoogleCampaign("Brand-Search", "Brand-Phrase", "Search Network", "Desktop",
                   daily_budget=80, base_ctr=0.16, base_cpc=0.95, base_cvr=0.12, base_aov=78,
                   impression_share=0.88),
    GoogleCampaign("Non-Brand-Search", "Apparel-Generic", "Search Network", "Mobile",
                   daily_budget=200, base_ctr=0.045, base_cpc=2.10, base_cvr=0.028, base_aov=68,
                   impression_share=0.42),
    GoogleCampaign("Non-Brand-Search", "Sustainable-Apparel", "Search Network", "Mobile",
                   daily_budget=140, base_ctr=0.052, base_cpc=2.40, base_cvr=0.034, base_aov=74,
                   impression_share=0.38),
    GoogleCampaign("PMax-Shopping", "All-Products", "Search Partners", "Mobile",
                   daily_budget=300, base_ctr=0.028, base_cpc=1.20, base_cvr=0.022, base_aov=66,
                   impression_share=0.55),
    GoogleCampaign("Display-Remarketing", "Cart-Abandoners-90d", "Display Network", "Mobile",
                   daily_budget=90, base_ctr=0.008, base_cpc=0.55, base_cvr=0.018, base_aov=64,
                   impression_share=0.65),
]

GOOGLE_TRACKING_GAP = {date(2026, 4, 19), date(2026, 4, 20), date(2026, 4, 21)}


def gen_google() -> list[dict]:
    rows = []
    for i in range(DAYS):
        d = START + timedelta(days=i)
        wf = weekend_factor(d)
        drift = cpm_drift(i)
        is_gap = d in GOOGLE_TRACKING_GAP
        for c in GOOGLE_PORTFOLIO:
            spend = jitter(c.daily_budget * wf, 0.10)
            cpc = jitter(c.base_cpc * drift, 0.08)
            clicks = spend / cpc
            ctr = max(0.001, jitter(c.base_ctr, 0.10))
            impressions = clicks / ctr
            cvr = jitter(c.base_cvr, 0.15)
            # Tracking gap: only the brand campaigns are affected (label them as such)
            if is_gap and c.campaign == "Brand-Search":
                conversions_actual = clicks * cvr
                conversions = 0  # tracking outage records zero
                conv_value = 0.0
            else:
                conversions = clicks * cvr
                aov = jitter(c.base_aov, 0.15)
                conv_value = conversions * aov
            cost_per_conv = spend / max(conversions, 0.001) if conversions else 0
            roas = (conv_value / spend) if spend else 0
            rows.append({
                "Date": d.isoformat(),
                "Account name": "Northwind Apparel",
                "Campaign name": c.campaign,
                "Ad group name": c.adgroup,
                "Network": c.network,
                "Device": c.device,
                "Daily budget": round2(c.daily_budget),
                "Cost": round2(spend),
                "Impressions": round_int(impressions),
                "Clicks": round_int(clicks),
                "CTR": round(ctr * 100, 3),
                "CPC": round2(cpc),
                "Conversions": round_int(conversions),
                "Conversion value": round2(conv_value),
                "Cost per conversion": round2(cost_per_conv) if conversions else 0,
                "Search impression share": round(c.impression_share, 3),
                "ROAS": round(roas, 2),
            })
    return rows


# ---------- TIKTOK ----------
@dataclass
class TikTokAd:
    campaign: str
    adgroup: str
    ad: str
    daily_budget: float
    base_ctr: float
    base_cpm: float
    base_roas: float
    video_complete_rate: float

TIKTOK_PORTFOLIO: list[TikTokAd] = [
    TikTokAd("TT-Prospecting-Q2", "Lookalike-Purchasers", "UGC-Customer-Review-1",
             daily_budget=120, base_ctr=0.018, base_cpm=7.5, base_roas=1.4, video_complete_rate=0.22),
    TikTokAd("TT-Prospecting-Q2", "Lookalike-Purchasers", "UGC-Customer-Review-2",
             daily_budget=100, base_ctr=0.016, base_cpm=8.0, base_roas=1.2, video_complete_rate=0.19),
    TikTokAd("TT-Prospecting-Q2", "Interest-Fashion", "Founder-Story-1",
             daily_budget=110, base_ctr=0.014, base_cpm=8.2, base_roas=1.1, video_complete_rate=0.18),
    # HIDDEN WINNER on TikTok
    TikTokAd("TT-Creator-Tests", "Creator-Audience-A", "UGC-Customer-Review-3",
             daily_budget=80, base_ctr=0.034, base_cpm=6.5, base_roas=2.9, video_complete_rate=0.34),
    TikTokAd("TT-Creator-Tests", "Creator-Audience-A", "Creator-Demo-Video",
             daily_budget=70, base_ctr=0.020, base_cpm=7.2, base_roas=1.5, video_complete_rate=0.24),
    TikTokAd("TT-Retargeting", "Site-Visitors-30d", "Dynamic-Product-Tile",
             daily_budget=90, base_ctr=0.025, base_cpm=8.5, base_roas=2.0, video_complete_rate=0.20),
]


def gen_tiktok() -> list[dict]:
    rows = []
    for i in range(DAYS):
        d = START + timedelta(days=i)
        wf = weekend_factor(d)
        drift = cpm_drift(i)
        for ad in TIKTOK_PORTFOLIO:
            spend = jitter(ad.daily_budget * wf, 0.10)
            cpm = jitter(ad.base_cpm * drift, 0.10)
            impressions = (spend / cpm) * 1000
            ctr = max(0.001, jitter(ad.base_ctr, 0.12))
            clicks = impressions * ctr
            cpc = spend / max(clicks, 1)
            roas = max(0.0, jitter(ad.base_roas, 0.12))
            revenue = spend * roas
            aov = jitter(60, 0.15)
            conversions = revenue / aov
            video_views = impressions * jitter(0.62, 0.10)
            video_p75 = video_views * jitter(ad.video_complete_rate * 1.4, 0.10)
            video_p100 = video_views * jitter(ad.video_complete_rate, 0.10)
            rows.append({
                "Date": d.isoformat(),
                "Advertiser name": "Northwind Apparel",
                "Campaign name": ad.campaign,
                "Ad group name": ad.adgroup,
                "Ad name": ad.ad,
                "Daily budget": round2(ad.daily_budget),
                "Cost": round2(spend),
                "Impressions": round_int(impressions),
                "Clicks": round_int(clicks),
                "CTR": round(ctr * 100, 3),
                "CPM": round2(cpm),
                "CPC": round2(cpc),
                "Conversions": round_int(conversions),
                "Video views": round_int(video_views),
                "Video views at 75%": round_int(video_p75),
                "Video views at 100%": round_int(video_p100),
                "ROAS": round(roas, 2),
            })
    return rows


# ---------- write ----------
def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    meta = gen_meta()
    google = gen_google()
    tiktok = gen_tiktok()
    write_csv(OUT / "meta-ads-90d.csv", meta)
    write_csv(OUT / "google-ads-90d.csv", google)
    write_csv(OUT / "tiktok-ads-90d.csv", tiktok)

    # quick sanity print
    def total_spend(rows, key="Cost"):
        return sum(r[key] for r in rows)

    print(f"Meta:   {len(meta):>5} rows, ${total_spend(meta):>10,.0f} total spend")
    print(f"Google: {len(google):>5} rows, ${total_spend(google):>10,.0f} total spend")
    print(f"TikTok: {len(tiktok):>5} rows, ${total_spend(tiktok):>10,.0f} total spend")
    annualized = (total_spend(meta) + total_spend(google) + total_spend(tiktok)) * (365 / DAYS)
    print(f"Annualized total: ${annualized:,.0f}")


if __name__ == "__main__":
    main()
