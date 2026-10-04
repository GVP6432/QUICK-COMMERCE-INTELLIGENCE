import threading
import json
import os
from selenium import webdriver
from scrape_blinkit import scrape_blinkit_for_pincode

def run_one_pincode(pincode, city_label, output_file):
    driver = webdriver.Chrome()
    driver.get("https://blinkit.com")

    print(f"\n[{city_label}] Browser window opened. Manually set location to {pincode} in THIS window.")
    input(f"[{city_label}] Once location is set, press Enter here to start scraping...")

    print(f"[{city_label}] Scraping started...")
    results = scrape_blinkit_for_pincode(driver, pincode, city_label)
    print(f"[{city_label}] Done - {len(results)} products collected.")

    os.makedirs("data", exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"[{city_label}] Saved to {output_file}")

    driver.quit()
    print(f"[{city_label}] Browser closed.")


if __name__ == "__main__":
    jobs = [
        ("400001", "Mumbai", "data/blinkit_mumbai.json"),
        ("400601", "Thane", "data/blinkit_thane.json"),
    ]

    threads = []
    for pincode, city, output_file in jobs:
        t = threading.Thread(target=run_one_pincode, args=(pincode, city, output_file))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nAll pincodes done.")