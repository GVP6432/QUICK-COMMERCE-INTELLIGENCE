from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.swiggy.com/instamart")

input("Set your delivery location to pincode 421301 (Kalyan). Then search 'milk' and press ENTER. Once you see a GRID of multiple products, press Enter here...")

driver.save_screenshot("scripts/instamart_debug.png")
print("Screenshot saved")
print(f"\nCurrent URL: {driver.current_url}")

body_text = driver.find_element(By.TAG_NAME, "body").text
print(f"\nFull visible page text:\n{body_text}")

input("\nPress Enter to close the browser...")
driver.quit()