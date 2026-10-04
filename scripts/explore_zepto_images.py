from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.zeptonow.com")

input("Set location to 421301, search 'milk', confirm you see the product grid, then press Enter here...")

images = driver.find_elements(By.TAG_NAME, "img")
print(f"Found {len(images)} total images on page\n")

for i, img in enumerate(images[:30]):
    alt_text = img.get_attribute("alt")
    if alt_text and len(alt_text) > 3:  # skip empty/icon images
        print(f"[{i}] alt=\"{alt_text}\"")

input("\nPress Enter to close...")
driver.quit()