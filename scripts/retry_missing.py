import time
import json
import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

sys.path.append(os.path.dirname(__file__))
from parse_blinkit import parse_blinkit_results
from config import PINCODES

# Exactly the gaps we found - city label mapped to its missing categories
MISSING = {
    "Kalyan": ["biscuits", "chocolate", "dal", "diapers"],
    "Mumbai": ["chips", "fruits"],
    "Nagpur": ["chocolate", "soap", "vegetables"],
    "Pune": ["chocolate", "noodles", "vegetables"],
    "Thane": ["diapers", "toothpaste"],
}

PINCODE_BY_CITY = {v: k for k, v in PINCODES.items()}


def wait_for_results(driver, timeout=15):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.find_element(By.TAG_NAME, "body").text.count("ADD") >= 2
        )
        return True
    except Exception:
        return False


def retry_category(driver, category_term, pincode, city_label, max_attempts=3):
    search_query = category_term.replace(" ", "+")
    url = f"https://blinkit.com/s/?q={search_query}"

    for attempt in range(1, max_attempts + 1):
        driver.get(url)
        loaded = wait_for_results(driver, timeout=15)

        body_text = driver.find_element(By.TAG_NAME, "body").text
        parsed = parse_blinkit_results(body_text)

        if parsed:
            print(f"  {category_term}: SUCCESS on attempt {attempt} - {len(parsed)} results")
            for item in parsed:
                item["searched_category"] = category_term
                item["pincode"] = pincode
                item["city"] = city_label
                item["platform"] = "blinkit"
                item["scraped_at"] = datetime.now().isoformat()
            return parsed

        print(f"  {category_term}: attempt {attempt} returned 0 results, waiting before retry...")
        time.sleep(4)

    print(f"  {category_term}: FAILED after {max_attempts} attempts - genuinely no results, or persistent block")
    return []


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get("https://blinkit.com")

    backfilled = []

    for city_label, categories in MISSING.items():
        pincode = PINCODE_BY_CITY[city_label]
        input(f"\nSet your delivery location to {pincode} ({city_label}), then press Enter here...")
        print(f"Retrying {len(categories)} missing categories for {city_label}...")

        for category_term in categories:
            results = retry_category(driver, category_term, pincode, city_label)
            backfilled.extend(results)

    print(f"\nTotal backfilled records: {len(backfilled)}")

    # Merge into the existing full dataset
    existing = json.load(open("data/blinkit_full_run.json"))
    combined = existing + backfilled

    with open("data/blinkit_full_run.json", "w") as f:
        json.dump(combined, f, indent=2)

    print(f"Merged. New total in blinkit_full_run.json: {len(combined)}")

    input("\nPress Enter to close the browser...")
    driver.quit()