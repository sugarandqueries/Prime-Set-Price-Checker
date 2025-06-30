import requests, pandas as pd, datetime as dt, time, pathlib

prime_sets = [
    "wisp_prime_set",
    "hildryn_prime_set",
    "mesa_prime_set",   # add or remove sets here
    "saryn_prime_set",
]

def get_90d_history(url_name):
    r = requests.get(f"https://api.warframe.market/v1/items/{url_name}/statistics")
    r.raise_for_status()
    days = r.json()["payload"]["statistics_closed"]["90days"]
    df = pd.DataFrame(days)[["datetime", "avg_price", "min_price", "max_price", "volume"]]
    df["item"] = url_name.replace("_prime_set", "").title() + " Prime"
    return df

frames = []
for item in prime_sets:
    frames.append(get_90d_history(item))
    time.sleep(0.6)  # be kind to the API

out = pathlib.Path("prime_prices.csv")
pd.concat(frames).to_csv(out, index=False)
print(f"Saved ➜ {out.resolve()}")