from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://blinkit.com")

input("Set your location to 421301. Then click the search box, type 'milk', and press ENTER on your keyboard (don't click any dropdown suggestion that appears). Once you see a GRID of multiple products, press Enter here...")

driver.save_screenshot("scripts/blinkit_debug.png")
print("Screenshot saved")
print(f"\nCurrent URL: {driver.current_url}")

body_text = driver.find_element(By.TAG_NAME, "body").text
print(f"\nFull visible page text:\n{body_text}")

input("\nPress Enter to close the browser...")
driver.quit()