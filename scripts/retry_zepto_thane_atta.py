import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from parse_zepto import parse_zepto_results

def wait_for_results(driver, timeout=15):
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.find_element(By.TAG_NAME, "body").text.count("ADD") >= 2
        )
        return True
    except Exception:
        return False

driver = webdriver.Chrome()
driver.get("https://www.zeptonow.com")
input("Set location to 400601 (Thane), then press Enter...")

driver.get("https://www.zeptonow.com/search?query=atta")
wait_for_results(driver, timeout=20)
time.sleep(2)

body_text = driver.find_element(By.TAG_NAME, "body").text
images = driver.find_elements(By.TAG_NAME, "img")
product_names = [
    img.get_attribute("alt") for img in images
    if img.get_attribute("alt") and len(img.get_attribute("alt")) > 3
    and "Ad.png" not in img.get_attribute("alt")
]

parsed = parse_zepto_results(body_text, product_names)
for item in parsed:
    item["searched_category"] = "atta"
    item["pincode"] = "400601"
    item["city"] = "Thane"
    item["platform"] = "zepto"
    item["scraped_at"] = datetime.now().isoformat()

print(f"Found {len(parsed)} results")

existing = json.load(open("data/zepto_full_run.json"))
combined = existing + parsed
with open("data/zepto_full_run.json", "w") as f:
    json.dump(combined, f, indent=2)

print(f"New total: {len(combined)}")
input("Press Enter to close...")
driver.quit()