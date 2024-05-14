import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Setup Undetected Chromedriver
options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
driver = uc.Chrome(options=options)

url = 'http://fastpeoplesearch.com'
driver.get(url)
wait = WebDriverWait(driver, 20)

data = []

try:
    option_to_select = wait.until(EC.element_to_be_clickable((By.XPATH, "//html/body/section[1]/div[4]/div[1]/ul/li[3]/a")))
    option_to_select.click()

    search_box = wait.until(EC.element_to_be_clickable((By.XPATH, "//html/body/section[1]/div[4]/div[2]/div[3]/form/div[1]/input")))
    search_box.send_keys('321 main st')

    search_box2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//html/body/section[1]/div[4]/div[2]/div[3]/form/div[2]/input")))
    search_box2.send_keys('Philadelphia PA 19143')

    search_box2.send_keys(Keys.RETURN)

    # Wait for search results to be visible
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'larger')))
    results = driver.find_elements(By.XPATH, '//*[@id="G-1500406130705278383"]/div')

    for result in results:
        name = result.find_element(By.CLASS_NAME, 'larger').text
        address = result.find_element(By.XPATH, './div[1]/strong/a').text
        number = result.find_element(By.CLASS_NAME, 'nowrap').text
        # Example of using .get_attribute to fetch hidden text
          # Adjust class name as per actual HTML structure
        data.append({'Name': name, 'Address': address, 'Number': number})

finally:
    driver.quit()

# Create a DataFrame and store the data
df = pd.DataFrame(data)

# Save to Excel
df.to_excel('output.xlsx', index=False)
print('Data has been saved to Excel.')
