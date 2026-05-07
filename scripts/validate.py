"""
Phase 1 validation: deterministically apply every rule from the skill's
references files against the generated CSVs. Confirms each seeded scenario
trips before the workshop. If anything misses, retune the data or the rule.

Usage: python3 scripts/validate.py
"""

from __future__ import annotations
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path
from statistics import mean

DATA = Path(__file__).resolve().parent.parent / "marketing-workspace" / "data"
META = DATA / "meta-ads-90d.csv"
GOOGLE = DATA / "google-ads-90d.csv"
TIKTOK = DATA / "tiktok-ads-90d.csv"


def load(path: Path) -> list[dict]:
    with path.open() as f:
        return list(csv.DictReader(f))


def f(x) -> float:
    return float(x) if x not in ("", None) else 0.0


def i(x) -> int:
    return int(x) if x not in ("", None) else 0


def section(title: str) -> None:
    print(f"\n{'=' * 70}\n {title}\n{'=' * 70}")


def check(label: str, ok: bool, detail: str = "") -> None:
    icon = "PASS" if ok else "FAIL"
    print(f"  [{icon}] {label}" + (f" :: {detail}" if detail else ""))


# ---------- META ANALYSIS ----------
def analyze_meta() -> None:
    section("META — fatigue rule (two-of-three confirmation)")
    rows = load(META)
    by_ad: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_ad[r["Ad name"]].append(r)

    # Sort each ad's rows by date
    for ad_name in by_ad:
        by_ad[ad_name].sort(key=lambda r: r["Date"])

    print("\n  Per-ad lifetime + recent vs baseline windows (3d vs 14d):\n")
    print(f"  {'Ad':<28} {'Days':>5} {'Spend':>9} {'ROAS':>5} {'Freq':>5} "
          f"{'CTRr':>5} {'CTRb':>5} {'CTRrat':>7} {'Flag':>10}")

    for ad_name, ad_rows in by_ad.items():
        days_live = len(ad_rows)
        lifetime_spend = sum(f(r["Cost"]) for r in ad_rows)
        if lifetime_spend < 500 or days_live < 7:
            continue
        recent = ad_rows[-3:]
        baseline = ad_rows[-14:-3] if len(ad_rows) >= 14 else ad_rows[:-3]
        ctr_r = mean(f(r["Link CTR"]) for r in recent)
        ctr_b = mean(f(r["Link CTR"]) for r in baseline) or 1e-9
        cpm_r = mean(f(r["CPM"]) for r in recent)
        cpm_b = mean(f(r["CPM"]) for r in baseline) or 1e-9
        freq_r = mean(f(r["Frequency"]) for r in recent)
        ctr_ratio = ctr_r / ctr_b
        cpm_ratio = cpm_r / cpm_b
        roas_lifetime = sum(f(r["Purchase conversion value"]) for r in ad_rows) / lifetime_spend

        signals = {
            "freq>=3": freq_r >= 3.0,
            "ctr<=.75": ctr_ratio <= 0.75,
            "cpm>=1.20": cpm_ratio >= 1.20,
        }
        n = sum(signals.values())
        flag = "HIGH" if n == 3 else ("MED" if n == 2 else ("WATCH" if n == 1 else ""))
        print(f"  {ad_name:<28} {days_live:>5} {lifetime_spend:>9.0f} "
              f"{roas_lifetime:>5.2f} {freq_r:>5.2f} "
              f"{ctr_r:>5.2f} {ctr_b:>5.2f} {ctr_ratio:>7.2f} {flag:>10}")

    section("META — seeded scenario checks")
    hero = sorted([r for r in rows if r["Ad name"] == "Video-Hero-A"], key=lambda r: r["Date"])
    recent = hero[-3:]
    baseline = hero[-14:-3]
    ctr_ratio = mean(f(r["Link CTR"]) for r in recent) / mean(f(r["Link CTR"]) for r in baseline)
    freq_r = mean(f(r["Frequency"]) for r in recent)
    cpm_ratio = mean(f(r["CPM"]) for r in recent) / mean(f(r["CPM"]) for r in baseline)
    sig = sum([freq_r >= 3.0, ctr_ratio <= 0.75, cpm_ratio >= 1.20])
    check("Video-Hero-A flagged with at least 2 signals", sig >= 2,
          f"freq={freq_r:.2f} ctr_ratio={ctr_ratio:.2f} cpm_ratio={cpm_ratio:.2f} "
          f"({sig}/3 signals)")

    sus = [r for r in rows if r["Ad set name"] == "Interest-Sustainability"]
    avg_roas = mean(f(r["ROAS"]) for r in sus)
    avg_spend = mean(f(r["Cost"]) for r in sus)
    check("Hidden winner Interest-Sustainability ROAS >= 1.25x account avg",
          avg_roas >= 1.25 * mean(f(r["ROAS"]) for r in rows),
          f"ad_set ROAS={avg_roas:.2f} vs account avg "
          f"{mean(f(r['ROAS']) for r in rows):.2f}, daily spend ~${avg_spend:.0f}")

    ret = [r for r in rows if r["Campaign name"] == "Retargeting-Cart-Abandoners"]
    by_campaign_day = defaultdict(float)
    for r in ret:
        by_campaign_day[r["Date"]] += f(r["Cost"])
    avg_daily_total = mean(by_campaign_day.values())
    target_total = 300 + 160  # two ad sets' budgets
    pct = avg_daily_total / target_total
    check("Pacing miss — Retargeting-Cart-Abandoners spends < 80% of budget",
          pct < 0.8,
          f"actual avg daily = ${avg_daily_total:.0f}, target = ${target_total}, "
          f"pct = {pct:.0%}")

    loser = [r for r in rows if r["Campaign name"] == "Cold-Broad-Test-2"]
    loser_roas = sum(f(r["Purchase conversion value"]) for r in loser) / sum(f(r["Cost"]) for r in loser)
    check("Genuine loser — Cold-Broad-Test-2 ROAS < 0.8x", loser_roas < 0.8,
          f"lifetime ROAS = {loser_roas:.2f}")


def analyze_google() -> None:
    section("GOOGLE — tracking gap detection")
    rows = load(GOOGLE)
    by_date_camp = defaultdict(lambda: {"spend": 0.0, "conv": 0})
    for r in rows:
        if r["Campaign name"] == "Brand-Search":
            by_date_camp[r["Date"]]["spend"] += f(r["Cost"])
            by_date_camp[r["Date"]]["conv"] += i(r["Conversions"])

    gap_dates = ["2026-04-19", "2026-04-20", "2026-04-21"]
    gap_zero = all(by_date_camp[d]["conv"] == 0 for d in gap_dates)
    gap_spend = all(by_date_camp[d]["spend"] > 0 for d in gap_dates)
    check("Brand-Search shows tracking artifact (zero conv but spend continued)",
          gap_zero and gap_spend,
          f"dates {gap_dates}: zero conv={gap_zero}, spend continued={gap_spend}")


def analyze_tiktok() -> None:
    section("TIKTOK — hidden winner")
    rows = load(TIKTOK)
    ugc3 = [r for r in rows if r["Ad name"] == "UGC-Customer-Review-3"]
    avg_ctr = mean(f(r["CTR"]) for r in ugc3)
    avg_roas = mean(f(r["ROAS"]) for r in ugc3)
    account_avg_roas = mean(f(r["ROAS"]) for r in rows)
    check("UGC-Customer-Review-3 outperforms TikTok account avg by 50%+",
          avg_roas >= 1.5 * account_avg_roas,
          f"ad ROAS={avg_roas:.2f} vs account avg={account_avg_roas:.2f}, "
          f"CTR={avg_ctr:.2f}%")


def headline_kpis() -> None:
    section("HEADLINE KPIs (last full week vs prior, blended)")
    meta_rows = load(META)
    google_rows = load(GOOGLE)
    tiktok_rows = load(TIKTOK)

    def to_d(s):
        y, m, dd = s.split("-")
        return date(int(y), int(m), int(dd))

    all_dates = sorted({r["Date"] for r in meta_rows + google_rows + tiktok_rows})
    last_date = to_d(all_dates[-1])
    days_back_to_sun = (last_date.weekday() + 1) % 7  # Sunday = 6 in py weekday
    # Actually: align to last full Mon-Sun week
    end_recent = last_date
    start_recent = end_recent.fromordinal(end_recent.toordinal() - 6)
    end_prior = start_recent.fromordinal(start_recent.toordinal() - 1)
    start_prior = end_prior.fromordinal(end_prior.toordinal() - 6)

    def in_range(d, a, b):
        dd = to_d(d)
        return a <= dd <= b

    def totals(rows, a, b, spend_k="Cost", rev_k=None):
        s = sum(f(r[spend_k]) for r in rows if in_range(r["Date"], a, b))
        rev = 0.0
        for r in rows:
            if not in_range(r["Date"], a, b):
                continue
            if rev_k:
                rev += f(r[rev_k])
            else:
                rev += f(r["Cost"]) * f(r["ROAS"])
        return s, rev

    def block(label, a, b):
        ms, mr = totals(meta_rows, a, b, rev_k="Purchase conversion value")
        gs, gr = totals(google_rows, a, b, rev_k="Conversion value")
        ts, tr = totals(tiktok_rows, a, b)  # tiktok rev = spend*ROAS
        spend = ms + gs + ts
        rev = mr + gr + tr
        roas = rev / spend if spend else 0
        print(f"  {label} ({a} to {b}): spend ${spend:>8,.0f}  rev ${rev:>9,.0f}  ROAS {roas:.2f}x")
        return spend, rev, roas

    rs, rr, rro = block("This week  ", start_recent, end_recent)
    ps, pr, pro = block("Prior week ", start_prior, end_prior)
    print(f"\n  Δ Spend:   {(rs - ps) / ps * 100:+.1f}%")
    print(f"  Δ Revenue: {(rr - pr) / pr * 100:+.1f}%")
    print(f"  Δ ROAS:    {(rro - pro):+.2f}x")


def main() -> None:
    headline_kpis()
    analyze_meta()
    analyze_google()
    analyze_tiktok()
    print()


if __name__ == "__main__":
    main()
