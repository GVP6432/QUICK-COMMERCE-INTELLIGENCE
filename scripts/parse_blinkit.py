import re

def parse_blinkit_results(page_text):
    lines = [line.strip() for line in page_text.split("\n") if line.strip()]
    products = []

    for i, line in enumerate(lines):
        if line == "ADD":
            j = i - 1
            prices = []

            while j >= 0 and lines[j].startswith("₹"):
                prices.append(lines[j])
                j -= 1

            if not prices:
                continue

            prices.reverse()
            current_price = prices[0].replace("₹", "").strip()
            size = lines[j] if j >= 0 else None
            j -= 1
            name = lines[j] if j >= 0 else None

            if name and size and current_price:
                products.append({
                    "name": name,
                    "size": size,
                    "price": float(current_price.replace(",", "")),
                    "has_discount": len(prices) > 1,
                })

    return products


if __name__ == "__main__":
    sample_text = """11 MINS
Pride of Cows Farm Cow Milk
500 ml
₹85
ADD
11 MINS
Amul Taaza Toned Milk
500 ml
₹30
ADD
22% OFF
11 MINS
Country Delight 25 g High Protein Vanilla Milk
250 ml
₹100
₹129
ADD"""

    results = parse_blinkit_results(sample_text)
    for r in results:
        print(r)