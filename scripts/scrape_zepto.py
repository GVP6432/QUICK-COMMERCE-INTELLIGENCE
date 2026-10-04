import time
import json
import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

sys.path.append(os.path.dirname(__file__))
from parse_zepto import parse_zepto_results
from config import CATEGORY_SEARCHES, PINCODES


def wait_for_results(driver, timeout=15):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.find_element(By.TAG_NAME, "body").text.count("ADD") >= 2
        )
        return True
    except Exception:
        return False


def scrape_zepto_for_pincode(driver, pincode, pincode_label):
    all_results = []

    for category_term in CATEGORY_SEARCHES:
        search_query = category_term.replace(" ", "%20")
        url = f"https://www.zeptonow.com/search?query={search_query}"
        driver.get(url)

        loaded = wait_for_results(driver, timeout=15)
        if not loaded:
            print(f"  {category_term}: WARNING - retrying once...")
            time.sleep(3)
            loaded = wait_for_results(driver, timeout=15)

        body_text = driver.find_element(By.TAG_NAME, "body").text

        images = driver.find_elements(By.TAG_NAME, "img")
        product_names = [
            img.get_attribute("alt") for img in images
            if img.get_attribute("alt") and len(img.get_attribute("alt")) > 3
            and "Ad.png" not in img.get_attribute("alt")
        ]

        parsed = parse_zepto_results(body_text, product_names)

        for item in parsed:
            item["searched_category"] = category_term
            item["pincode"] = pincode
            item["city"] = pincode_label
            item["platform"] = "zepto"
            item["scraped_at"] = datetime.now().isoformat()

        all_results.extend(parsed)
        status = "OK" if parsed else "EMPTY - possible issue"
        print(f"  {category_term}: found {len(parsed)} results [{status}]")

    return all_results


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://www.zeptonow.com")

    all_pincode_results = []

    for pincode, city_label in PINCODES.items():
        input(f"\nSet your delivery location to {pincode} ({city_label}), then press Enter here...")
        print(f"Scraping for {city_label} ({pincode})...")
        results = scrape_zepto_for_pincode(driver, pincode, city_label)
        print(f"  -> {len(results)} products collected for {city_label}")
        all_pincode_results.extend(results)

    print(f"\nGrand total across all pincodes: {len(all_pincode_results)}")

    os.makedirs("data", exist_ok=True)
    with open("data/zepto_full_run.json", "w") as f:
        json.dump(all_pincode_results, f, indent=2)
    print("Saved to data/zepto_full_run.json")

    input("\nPress Enter to close the browser...")
    driver.quit()