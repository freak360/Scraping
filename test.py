import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import time

# Setup Undetected Chromedriver
options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
driver = uc.Chrome(options=options)

url = 'http://fastpeoplesearch.com'
wait = WebDriverWait(driver, 5)

# Read addresses from Excel
input_file = 'new_add.xlsx'
df_addresses = pd.read_excel(input_file)
addresses = list(zip(df_addresses['Street'], df_addresses['City_State']))

data = []

try:
    for street, city_state in addresses:
        print(f"Searching for: {street}, {city_state}")
        driver.get(url)

        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//html/body/section[1]/div[4]/div[1]/ul/li[3]/a"))).click()
            search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//html/body/section[1]/div[4]/div[2]/div[3]/form/div[1]/input")))
        except:
            print("Exception occurred!! Refreshing for the next address.")
            continue

        search_box.clear()
        search_box.send_keys(street)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//html/body/section[1]/div[4]/div[1]/ul/li[3]/a"))).click()
            search_box2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//html/body/section[1]/div[4]/div[2]/div[3]/form/div[2]/input")))
        except:
            print("Exception occurred!! Refreshing for the next address.")
            continue
        
        search_box2.clear()
        search_box2.send_keys(city_state)
        search_box2.send_keys(Keys.RETURN)


        # XPaths for different divs
        xpaths = [
            '/html/body/div[4]/div/div[1]/div[3]/div[1]/div[1]',
            '/html/body/div[4]/div/div[1]/div[3]/div[4]/div[1]',
            '/html/body/div[4]/div/div[1]/div[3]/div[6]/div[1]',
            '/html/body/div[4]/div/div[1]/div[3]/div[8]/div[1]',
            '/html/body/div[4]/div/div[1]/div[3]/div[9]/div[1]',
            '/html/body/div[4]/div/div[1]/div[3]/div[10]/div[1]',
            '/html/body/div[4]/div/div[1]/div[3]/div[11]/div[1]',
            '/html/body/div[4]/div/div[1]/div[3]/div[12]/div[1]',
            '/html/body/div[4]/div/div[1]/div[3]/div[13]/div[1]',
            '/html/body/div[4]/div/div[1]/div[3]/div[14]/div[1]'
        ]

        for xpath in xpaths:
            try:
                result = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                name = result.find_element(By.XPATH, './h2/a/span[1]').text if result.find_elements(By.XPATH, './h2/a/span[1]') else None
                address = result.find_element(By.XPATH, './div[1]/strong/a').text if result.find_elements(By.XPATH, './div[1]/strong/a') else None
                number = result.find_element(By.XPATH, './strong/a').text if result.find_elements(By.XPATH, './strong/a') else None

                data.append({'Name': name, 'Address': address, 'Number': number})
            except (NoSuchElementException, TimeoutException):
                print(f"Could not locate elements for the div at {xpath}")

        time.sleep(2)  # Sleep to avoid too rapid requests

finally:
    driver.quit()

# Create a DataFrame and store the data
df = pd.DataFrame(data)

# Save to Excel
df.to_excel('output2.xlsx', index=False)
print('Data has been saved to Excel.')
