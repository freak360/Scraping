import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Setup Undetected Chromedriver
options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
driver = uc.Chrome(options=options)

url = 'http://fastpeoplesearch.com'
wait = WebDriverWait(driver, 20)

# Read addresses from Excel
input_file = 'addresses.xlsx'  # Make sure the file name matches your actual file
df_addresses = pd.read_excel(input_file)
addresses = list(zip(df_addresses['Street'], df_addresses['City_State']))

data = []

try:
    for street, city_state in addresses:
        print(f"Searching for: {street}, {city_state}")  # Debug print
        
        driver.get(url)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//html/body/section[1]/div[4]/div[1]/ul/li[3]/a"))).click()

        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//html/body/section[1]/div[4]/div[2]/div[3]/form/div[1]/input")))
        search_box.clear()
        search_box.send_keys(street)

        search_box2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//html/body/section[1]/div[4]/div[2]/div[3]/form/div[2]/input")))
        search_box2.clear()
        search_box2.send_keys(city_state)
        search_box2.send_keys(Keys.RETURN)

        # Wait for search results to be visible
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/div/div[1]/div[2]/div[1]')))
        results = driver.find_elements(By.XPATH, '/html/body/div[4]/div/div[1]/div[2]/div[1]')

        for result in results:
            elements = result.find_elements(By.XPATH, './div/h2/a/span[1]')
            if elements:
                name = elements[0].text
            else:
                elements = result.find_elements(By.XPATH, '/html/body/div[4]/div/div[1]/div[3]/div[1]/div/h2/a/span[1]')
                name = elements[0].text if elements else None

            elements = result.find_elements(By.XPATH, './div/div[1]/strong/a')
            if elements:
                address = elements[0].text
            else:
                elements = result.find_elements(By.XPATH, '/html/body/div[4]/div/div[1]/div[3]/div[1]/div/div[1]/strong/a')
                address = elements[0].text if elements else None

            elements = result.find_elements(By.XPATH, './div/strong/a')
            if elements:
                number = elements[0].text
            else:
                elements = result.find_elements(By.XPATH, '/html/body/div[4]/div/div[1]/div[3]/div[1]/div/strong/a')
                number = elements[0].text if elements else None

            data.append({'Name': name, 'Address': address, 'Number': number})
        
        time.sleep(2)  # Sleep to avoid too rapid requests

finally:
    driver.quit()

# Create a DataFrame and store the data
df = pd.DataFrame(data)

# Save to Excel
df.to_excel('output.xlsx', index=False)
print('Data has been saved to Excel.')
