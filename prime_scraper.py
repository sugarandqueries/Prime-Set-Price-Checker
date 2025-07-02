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

# --- 0. setup -------------------------------------------------    
prime_sets = [
    # S-tier & A-tier Primes from Overframe
    "wisp_prime_set", "saryn_prime_set", "dante_prime_set",
    "octavia_prime_set", "mesa_prime_set", "revenant_prime_set",
    "khora_prime_set", "gauss_prime_set", "volt_prime_set",
    "protean_prime_set", "mirage_prime_set", "nova_prime_set",
    "xaku_prime_set", "wukong_prime_set", "nidus_prime_set",
    "baruuk_prime_set", "rhino_prime_set", "harrow_prime_set",
    "gara_prime_set", "nezha_prime_set", "titania_prime_set",
    "nekros_prime_set", "sevagoth_prime_set", "mag_prime_set",
    "trinity_prime_set", "garuda_prime_set", "ember_prime_set",
    "hildryn_prime_set", "lavos_prime_set", "ivara_prime_set",
    "vauban_prime_set",
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

def safe_history(url):
    try:
        return get_history(url) 
    except Exception as e:
        print(f"⚠️  {url}: {e}")
        return pd.DataFrame() # return empty DataFrame on error



frames = []
for url_name in prime_sets:
    frames.append(get_history(url_name))
    time.sleep(1)  # to avoid hitting API rate limits

raw = pd.concat(frames, ignore_index=True)

# --- 2. clean it up -------------------------------------------
clean = (
    raw.sort_values(["item"])
    .drop_duplicates()
    .replace(0, pd.NA)  # removes API zeroes
    .astype(
        {
            "avg_price": "float",
            "min_price": "float",
            "max_price": "float",
            "volume": "Int64",
        }
    )
)

# remove duplicates in case of API errors
raw.sort_values(["item", "datetime"], inplace=True)
clean = raw.drop_duplicates(subset=["item", "datetime"]) 

# remove rows with no volume data
raw = raw.dropna(subset=["volume"])


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


