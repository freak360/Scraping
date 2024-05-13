import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Setup Undetected Chromedriver
options = uc.ChromeOptions()
# Setting Chrome to undetectable
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
driver = uc.Chrome(options=options)

# Open the website
url = 'http://fastpeoplesearch.com'
driver.get(url)

# Use WebDriverWait to handle the timing issues
wait = WebDriverWait(driver, 20)

# def find_element_safe(driver, by, value):
#     """ Attempt to find an element safely, retrying if it's stale. """
#     attempts = 3
#     for attempt in range(attempts):
#         try:
#             element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
#             # Optional: you might want to interact with the element immediately to ensure it's not stale
#             element.is_displayed()
#             return element
#         except StaleElementReferenceException:
#             if attempt == attempts - 1:
#                 raise
#             continue

try:
    # First, interact with the preliminary options to make the search form appear
    option_to_select = wait.until(EC.element_to_be_clickable((By.XPATH, "//html/body/section[1]/div[4]/div[1]/ul/li[3]/a")))
    option_to_select.click()

    # Now wait for the search box to be clickable and interact with it
    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//html/body/section[1]/div[4]/div[2]/div[3]/form/div[1]/input")))
    search_box.send_keys('321 main st')

    search_box2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//html/body/section[1]/div[4]/div[2]/div[3]/form/div[2]/input")))
    search_box2.send_keys('Philadelphia PA 19143')

    # Submit the form
    search_box.send_keys(Keys.RETURN)
    search_box2.send_keys(Keys.RETURN)

    # Wait for search results to be visible
    time.sleep(30)  # Adjust based on actual page load times or replace with another WebDriverWait

    # element = find_element_safe(driver, By.XPATH, '//*[@id="G-1500406130705278383"]/div/h2/a/span[1]')
    # names, addresses, phone_numbers = [element.click()]

    # Scrape the data
    result = [el.text for el in driver.find_elements(By.CLASS_NAME, 'card')]
    # names = [el.text for el in driver.find_elements(By.ID, 'G-1500406130705278383')]
    # addresses = [el.text for el in driver.find_elements(By.ID, 'G-1500406130705278383')]
    # phone_numbers = [el.text for el in driver.find_elements(By.ID, 'G-1500406130705278383')]

finally:
    # Handle quitting the driver safely
    try:
        driver.quit()
    except Exception as e:
        print("Error closing the driver:", e)


# Create a DataFrame and store the data
df = pd.DataFrame({
    'Name': result,
    'Address': result,
    'Phone Number': result
})

# Save to Excel
df.to_excel('output.xlsx', index=False)

print('Data has been saved to Excel.')
