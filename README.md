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

---

## Live Preview
* My attempt at deploying a website using Jekyll. It's very basic and unoptimized as I'm still a beginner but its functional!
* [Link Here](https://sugarandqueries.github.io/Prime-Set-Price-Checker/)

## Quick start
```bash
git clone https://github.com/sugarandqueries/Prime-Set-Price-Checker.git
cd Prime-Set-Price-Checker
pip install -r requirements.txt
python prime_scraper.py      # generates the latest CSV locally as prime_prices_clean.csv
```

---


## Dashboard
Download PrimePricePulse.pbit, open in Power BI Desktop, hit Refresh and enjoy the stonks.

---

## License
MIT
### Disclaimer 
>Large chunks of the scraping script and dashboard layout ideas were co-piloted with ChatGPT (OpenAI o3). I still tested, tweaked, and shipped everything myself, but I still think adding this disclaimer is necessary. Always practice safe AI usage!
