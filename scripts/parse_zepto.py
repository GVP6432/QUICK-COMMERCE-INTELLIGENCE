def parse_zepto_results(page_text, product_names):
    lines = [line.strip() for line in page_text.split("\n") if line.strip()]
    price_blocks = []

    i = 0
    while i < len(lines):
        if lines[i] == "ADD":
            j = i + 1
            prices = []
            while j < len(lines) and lines[j].startswith("₹"):
                prices.append(lines[j])
                j += 1

            size = lines[j] if j < len(lines) else None

            if prices and size:
                current_price = prices[0].replace("₹", "").strip()
                price_blocks.append({
                    "price": float(current_price.replace(",", "")),
                    "size": size,
                    "has_discount": len(prices) > 1,
                })
            i = j
        else:
            i += 1

    # Match each price block to a product name by position
    products = []
    for idx, block in enumerate(price_blocks):
        if idx < len(product_names):
            block["name"] = product_names[idx]
            products.append(block)

    return products


if __name__ == "__main__":
    sample_text = """ADD
₹46
₹49
1 pack (500 ml)
ADD
₹33
1 pack (450 ml)
ADD
₹30
1 pack (500 ml)"""

    sample_names = [
        "Humpy A2 Cow Fresh Milk | Pouch",
        "Amul Moti Toned Milk | 90 Days Shelf life",
        "Amul Taaza Toned Fresh Milk | Pouch",
    ]

    results = parse_zepto_results(sample_text, sample_names)
    for r in results:
        print(r)