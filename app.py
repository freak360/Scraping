from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Setup WebDriver with ChromeDriverManager
# options = webdriver.ChromeOptions()
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome()

# Open the website
url = 'http://fastpeoplesearch.com'
driver.get(url)

# Use WebDriverWait to handle the timing issues
wait = WebDriverWait(driver, 20)

try:
    # First, interact with the preliminary options to make the search form appear
    # Example: Click the third option from a set of options
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
    time.sleep(50)  # Adjust this based on actual page load times or replace with another WebDriverWait

    # Scrape the data
    names = [el.text for el in driver.find_elements(By.XPATH, '/html/body/div[4]/div/div[1]/div[2]/div/div/h2')]
    addresses = [el.text for el in driver.find_elements(By.XPATH, '/html/body/div[4]/div/div[1]/div[2]/div/div/div[1]')]
    phone_numbers = [el.text for el in driver.find_elements(By.XPATH, '/html/body/div[4]/div/div[1]/div[2]/div/div/strong/a')]

finally:
    # Ensure the driver quits no matter what
    driver.quit()

# Create a DataFrame and store the data
df = pd.DataFrame({
    'Name': names,
    'Address': addresses,
    'Phone Number': phone_numbers
})

# Save to Excel
df.to_excel('output.xlsx', index=False)

print('Data has been saved to Excel.')
