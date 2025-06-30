"""
Prime Price Pulse 2.0
=====================
Pulls 90-day price history for each Prime set, cleans the data,
and spits out a squeaky-clean CSV ready for Power BI.
"""

import requests
import pandas as pd
import pathlib
import time

# ✏️  Add or remove sets here
prime_sets = [
    "wisp_prime_set",
    "hildryn_prime_set",
    "saryn_prime_set",
    "mesa_prime_set",
    "octavia_prime_set",
]

# --- 1. grab the data -----------------------------------------
def get_history(url_name: str) -> pd.DataFrame:
    url = f"https://api.warframe.market/v1/items/{url_name}/statistics"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    days = r.json()["payload"]["statistics_closed"]["90days"]
    df = (
        pd.DataFrame(days)[
            ["datetime", "avg_price", "min_price", "max_price", "volume"]
        ]
        .assign(
            item=url_name.replace("_prime_set", "").title(),  # Wisp Prime -> Wisp
            datetime=lambda x: pd.to_datetime(x["datetime"]),
        )
    )
    return df


frames = []
for url_name in prime_sets:
    frames.append(get_history(url_name))
    time.sleep(0.6)  # be gentle to the API

raw = pd.concat(frames, ignore_index=True)

# --- 2. clean it up -------------------------------------------
clean = (
    raw.sort_values(["item", "datetime"])
    .drop_duplicates()
    .replace(0, pd.NA)  # zap API zeroes
    .astype(
        {
            "avg_price": "float",
            "min_price": "float",
            "max_price": "float",
            "volume": "Int64",
        }
    )
)

# split datetime for easier grouping
clean["date"] = clean["datetime"].dt.date
clean["time"] = clean["datetime"].dt.time

# 7-day rolling average 
clean["avg_price_7d"] = (
    clean.groupby("item")["avg_price"]
    .transform(lambda s: s.rolling(window=7, min_periods=1).mean())
)

# --- 3. save ---------------------------------------------------
out_path = pathlib.Path("prime_prices_clean.csv")
clean.to_csv(out_path, index=False)
print(f"Saved ➜ {out_path.resolve()}")