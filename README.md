# Quick-Commerce Market Intelligence

Comparative analysis of Blinkit and Zepto — pricing, catalog availability,
and discounting behavior across 5 Maharashtra cities and 22 product categories.

## What it does
- Scrapes live product listings (name, size, price, discount flag) from Blinkit
  and Zepto across 5 pincodes (Mumbai, Pune, Nagpur, Thane, Kalyan)
- Cleans and normalizes product names/sizes to enable fuzzy cross-platform matching
  (exact-string matching initially found 0% overlap; normalization recovered 140
  genuinely comparable products)
- Loads into PostgreSQL with SQL views for price comparison and category availability
- Visualizes findings in a 3-page Power BI dashboard (cross-platform comparison,
  Blinkit detail, Zepto detail)

## Key findings
- Among 140 directly comparable products, Zepto was cheaper 126 times vs
  Blinkit's 108 (~54% vs 46%)
- Only ~2.6% of each platform's catalog could be confidently matched by name,
  revealing how differently platforms brand and bundle identical products
- Both platforms independently price ghee and diapers as their most expensive
  categories, and apply near-universal discounting to dal, diapers, fruits,
  rice, and vegetables — suggesting category economics drive pricing more
  than platform-specific strategy

## Platform coverage note
A third platform (Swiggy Instamart) was evaluated but excluded after
encountering an active WAF block (bare "Access Denied" response) requiring
bot-detection evasion beyond this project's scope.

## Stack
Python (Selenium, BeautifulSoup patterns) · PostgreSQL · Power BI

## How to run
1. `pip install -r requirements.txt`
2. Set up `.env` with your DB credentials (see `.env.example`)
3. `python scripts/scrape_blinkit.py` and `python scripts/scrape_zepto.py`
   (interactive — prompts for manual location-setting per pincode)
4. `python scripts/match_products.py` to build the normalized/matched dataset
5. `python scripts/load_to_db.py`
6. Run SQL scripts in `sql/` against your database
7. Open `dashboards/quick_commerce_dashboard.pbix` in Power BI