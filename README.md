# Prime Set Price Checker 

**Stonks for your wishlisted Primes in one click.**

This repo:

1. 🐍 Scrapes **warframe.market** for 90-day price stats on *specified* Prime sets  
2. 🤖 Runs a nightly GitHub Action to refresh `prime_prices_clean.csv`  
3. 📊 Powers a **Power BI** dashboard (template included) that shows  
   * daily plat trends  
   * 7-day volatility  
   * top movers & shakers  
   * auto-generated market narrative
  
 > Perfect for traders, content creators, or anyone who just likes watching numbers go BRRRRR.

## Preview 
![image](https://github.com/user-attachments/assets/1d9a1fab-90b1-4e9d-8abc-3bc2dbf27339)

---


## Quick start
```bash
git clone https://github.com/<you>/Prime-Set-Price-Checker.git
cd Prime-Set-Price-Checker
pip install -r requirements.txt
python prime_scraper.py      # generates the latest CSV locally
```

---


## Dashboard
Download PrimePricePulse.pbit, open in Power BI Desktop, hit Refresh and enjoy the stonks.

---

## License
MIT
