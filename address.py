import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Configure Selenium WebDriver
options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
driver = uc.Chrome(options=options)

wait = WebDriverWait(driver, 20)


def fetch_addresses_with_selenium(zipcode):
    try:
        # Open the webpage
        driver.get("https://www.trulia.com/")
        time.sleep(2)  # Wait for the page to load

        # Find the search box element by its name or ID (adjust as necessary)
        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/main/div[1]/div/div/div[2]/div/div[2]/div/button[3]/div"))).click()
        driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[1]/div/div/div[2]/div/div[2]/div/button[3]/div")
        search_box = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[1]/div/div/div[2]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/input")
        search_box.clear()
        search_box.send_keys(zipcode)

        # Find the search button by its name, ID, or text and click it (adjust as necessary)
        wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/main/div[1]/div/div/div[2]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div[2]"))).click()
        search_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[1]/div/div/div[2]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div[2]")
        search_button.click()
        time.sleep(2)  # Wait for the search results to load

        # Now extract the addresses, assuming they are in <div class="address">
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[2]/div[1]/ul/li[1]/div/div/div/div[2]/div/a/div')))
        addresses = [element.text for element in driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div[3]/div[2]/div[1]/ul/li[1]/div/div/div/div[2]/div/a/div")]
        return addresses
    finally:
        driver.quit()

def main():
    zipcodes = ["45812", "19143", "19141"]
    all_addresses = []

    for zipcode in zipcodes:
        addresses = fetch_addresses_with_selenium(zipcode)
        for address in addresses:
            all_addresses.append({
                'Zipcode': zipcode,
                'Address': address
            })

    # Convert list of dictionaries to a DataFrame
    df = pd.DataFrame(all_addresses)
    # Save the DataFrame to an Excel file
    df.to_excel('addresses.xlsx', index=False)

if __name__ == "__main__":
    main()
