#!/usr/bin/env python3
"""Download Taiwan house-price index candidates.

Collected candidates:
- Sinyi quarterly metropolitan house-price index, including Taiwan aggregate.
- Taipei City monthly residential price index from data.taipei.

The baseline placeholder `tw_house_prices_raw.csv` uses Sinyi's Taiwan
aggregate expanded from quarterly to monthly by repeating the quarter value.
The final dataset builder can later choose another interpolation method or
another source without losing the raw quarterly candidate.
"""

from __future__ import annotations

from io import BytesIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import RAW_TW_FIN


SINYI_URL = "https://www.sinyinews.com.tw/quarterly"
TAIPEI_MONTHLY_URL = (
    "https://data.taipei/api/dataset/"
    "ce4ea2c6-6334-44f8-945a-5705492b187d/resource/"
    "02c7bb70-2113-4daf-81d3-5c14b9ae26df/download"
)

SINYI_REGION_MAP = {
    "台北": "taipei",
    "新北": "new_taipei",
    "桃園": "taoyuan",
    "新竹": "hsinchu",
    "台中": "taichung",
    "台南": "tainan",
    "高雄": "kaohsiung",
    "台灣": "taiwan",
}


def _num(value: str) -> float | None:
    value = value.strip().replace(",", "")
    if value in {"", "-", "—", "nan"}:
        return None
    return float(value)


def fetch_sinyi_quarterly() -> pd.DataFrame:
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(SINYI_URL, headers=headers, timeout=45)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    rows: list[dict[str, object]] = []
    for block in soup.select("div.all_year_block"):
        labels = [p.get_text(strip=True) for p in block.select("ul li p")]
        regions = labels[1:]
        if "台灣" not in regions:
            continue

        for dl in block.find_all("dl", recursive=False):
            period_tag = dl.find("dt")
            if period_tag is None:
                continue
            period = period_tag.get_text(strip=True)
            if "/Q" not in period:
                continue

            values = [p.get_text(strip=True) for p in dl.select("dd p")]
            if len(values) < len(regions):
                continue

            year, quarter = period.split("/Q")
            out = {
                "quarter": period,
                "date": f"{int(year)}Q{int(quarter)}",
                "source": "Sinyi News quarterly house price index",
                "source_url": SINYI_URL,
            }
            for region, value in zip(regions, values):
                key = SINYI_REGION_MAP.get(region, region)
                out[f"sinyi_{key}"] = _num(value)
            rows.append(out)

    if not rows:
        raise RuntimeError("No Sinyi quarterly rows parsed.")

    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    return df


def expand_sinyi_taiwan_to_monthly(quarterly: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for _, row in quarterly.iterrows():
        period = pd.Period(row["date"], freq="Q")
        for month in pd.period_range(period.start_time, period.end_time, freq="M"):
            rows.append(
                {
                    "date": str(month),
                    "tw_house_prices": row["sinyi_taiwan"],
                    "tw_house_sinyi_taiwan": row["sinyi_taiwan"],
                    "source_quarter": row["quarter"],
                    "source": "Sinyi quarterly Taiwan aggregate, repeated within quarter",
                    "source_url": SINYI_URL,
                }
            )
    return pd.DataFrame(rows)


def fetch_taipei_monthly() -> pd.DataFrame:
    resp = requests.get(TAIPEI_MONTHLY_URL, timeout=30)
    resp.raise_for_status()

    raw = pd.read_csv(BytesIO(resp.content), encoding="big5")
    raw = raw.rename(
        columns={
            "住宅價格月指數類別": "category",
            "期別": "roc_month",
            "月指數": "monthly_index",
            "季移動平均數": "quarter_moving_avg",
            "半年移動平均數": "half_year_moving_avg",
            "月指數變動率": "monthly_change",
            "季移動平均數變動率": "quarter_moving_avg_change",
            "半年移動平均數變動率": "half_year_moving_avg_change",
            "標準住宅總價（新台幣萬元）": "standard_total_price_10k_ntd",
            "標準住宅單價（新台幣萬元每坪）": "standard_unit_price_10k_ntd_per_ping",
        }
    )
    year_month = raw["roc_month"].astype(str).str.extract(r"(\d+)/(\d+)")
    raw["date"] = (
        (year_month[0].astype(int) + 1911).astype(str)
        + "-"
        + year_month[1].astype(int).astype(str).str.zfill(2)
    )
    numeric_cols = [
        "monthly_index",
        "quarter_moving_avg",
        "half_year_moving_avg",
        "standard_total_price_10k_ntd",
        "standard_unit_price_10k_ntd_per_ping",
    ]
    for col in numeric_cols:
        raw[col] = pd.to_numeric(raw[col].replace("-", pd.NA), errors="coerce")
    raw["source"] = "Taipei City Government open data"
    raw["source_url"] = TAIPEI_MONTHLY_URL
    return raw[
        [
            "date",
            "category",
            "monthly_index",
            "quarter_moving_avg",
            "half_year_moving_avg",
            "monthly_change",
            "quarter_moving_avg_change",
            "half_year_moving_avg_change",
            "standard_total_price_10k_ntd",
            "standard_unit_price_10k_ntd_per_ping",
            "source",
            "source_url",
        ]
    ].sort_values(["category", "date"])


def main() -> None:
    RAW_TW_FIN.mkdir(parents=True, exist_ok=True)

    sinyi_q = fetch_sinyi_quarterly()
    sinyi_q_out = RAW_TW_FIN / "tw_house_sinyi_quarterly_raw.csv"
    sinyi_q.to_csv(sinyi_q_out, index=False)

    sinyi_m = expand_sinyi_taiwan_to_monthly(sinyi_q)
    house_out = RAW_TW_FIN / "tw_house_prices_raw.csv"
    sinyi_m.to_csv(house_out, index=False)

    taipei = fetch_taipei_monthly()
    taipei_out = RAW_TW_FIN / "tw_house_taipei_monthly_raw.csv"
    taipei.to_csv(taipei_out, index=False)

    print(f"Saved {sinyi_q_out} ({len(sinyi_q)} quarterly rows)")
    print(f"Saved {house_out} ({len(sinyi_m)} monthly rows)")
    print(f"Saved {taipei_out} ({len(taipei)} monthly/category rows)")


if __name__ == "__main__":
    main()
