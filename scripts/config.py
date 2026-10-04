# Pincodes across Maharashtra - metro, tier-2, and local coverage
PINCODES = {
    "400001": "Mumbai",
    "411001": "Pune",
    "440001": "Nagpur",
    "400601": "Thane",
    "421301": "Kalyan",
}

# Broad category searches - each one returns 15-25 real products automatically,
# giving much wider coverage than hand-picking exact SKUs
CATEGORY_SEARCHES = [
    "milk", "bread", "butter", "atta", "rice", "dal", "oil",
    "biscuits", "chips", "noodles", "cold drink", "chocolate",
    "toothpaste", "soap", "shampoo", "detergent", "dishwash",
    "diapers", "fruits", "vegetables", "ghee", "dry fruits",
]

# Platforms we're tracking - used to tag records consistently across all scrapers
PLATFORMS = ["blinkit", "zepto", "instamart"]