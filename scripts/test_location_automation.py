import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def set_location(driver, pincode):
    driver.get("https://blinkit.com")
    time.sleep(3)

    try:
        # Case 1: a location search input might already be visible (auto-prompt on fresh session)
        search_input = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
        )
        print("Location input already visible, no click needed.")
    except Exception:
        # Case 2: need to click the address bar to open it first
        print("No input visible yet, trying to click the address bar...")
        address_element = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Maharashtra') or contains(text(), 'Delivery in')]"))
        )
        driver.execute_script("arguments[0].click();", address_element)  # JS click avoids overlay interception
        time.sleep(1)
        search_input = driver.find_element(By.XPATH, "//input[@type='text']")

    search_input.clear()
    search_input.send_keys(pincode)
    time.sleep(2)

    search_input.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.5)
    search_input.send_keys(Keys.ENTER)
    time.sleep(2)

    body_text = driver.find_element(By.TAG_NAME, "body").text
    if pincode in body_text:
        print(f"SUCCESS: Location set to {pincode}")
        return True
    else:
        print(f"UNCERTAIN: Could not confirm {pincode} in page text.")
        return False


if __name__ == "__main__":
    driver = webdriver.Chrome()
    result = set_location(driver, "411001")
    input(f"\nAutomation result: {result}. Look at the browser - does it actually show Pune 411001? Press Enter to close...")
    driver.quit()