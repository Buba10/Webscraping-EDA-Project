# importing libraries
import pandas as pd
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

laptop_name = []
laptop_rating = []
laptop_processor = []
laptop_memory = []
laptop_os = []
laptop_storage = []
laptop_display = []
laptop_inlcusion = []
laptop_price = []
laptop_specs = []

# Set up Selenium
driver_path = 'C:/DRIVERS/geckodriver.exe'
options = Options()
options.binary_location = 'C:/Program Files/Mozilla Firefox/firefox.exe'

service = Service(driver_path)
driver = webdriver.Firefox(service=service, options=options)

driver.get('https://www.flipkart.com/search?q=gaming+laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=gaming+laptop%7CLaptops&requestId=c1e0a154-c5dd-467f-989c-8f7b11ea8a2d&as-searchtext=gaming+&sort=price_desc&page=')


laptops = driver.find_elements(By.CLASS_NAME, 'CGtC98')

for laptop in laptops:
  try:
    name = laptop.find_element(By.CLASS_NAME, 'KzDlHZ').text
    print(name)
    rating = laptop.find_element(By.CLASS_NAME, 'XQDdHH').text
    print(rating)
    price = laptop.find_element(By.CLASS_NAME, 'cN1yYO').text
    # print(price)

    ## Split the lines for the prices. Take the discounted price only
    lines_price = price.splitlines()
    
    # Extract the first line as the price and convert it to a numeric value
    if lines_price:
        numeric_price = float(lines_price[0].replace('₹', '').replace(',', '').strip())
    else:
        numeric_price = 0.0  # Default if no price is found


    specs = laptop.find_element(By.CLASS_NAME, 'G4BRas').text
    print(specs)

    ## Splitting the lines for the specs. Divide it on OS, Storage, Memory, Display, Processor
    lines = specs.splitlines()
    array_line = []
    for line in lines:
        array_line.append(line)
    
    if len(array_line) == 6:
        laptop_name.append(name)  # The name of the laptop
        laptop_price.append(numeric_price)  # Store the numeric price
        laptop_rating.append(rating)
        
        # Append per specs
        laptop_processor.append(array_line[0])
        laptop_memory.append(array_line[1])
        laptop_os.append(array_line[2])
        laptop_storage.append(array_line[3])
        laptop_display.append(array_line[4])
        laptop_inlcusion.append(array_line[5])

  except:
    pass

  sleep(3)

# Save to CSV function
def save_to_csv():
    data = {
        'Name': laptop_name,
        'Price': laptop_price,
        'Rating': laptop_rating,
        'Processor': laptop_processor,
        'Memory': laptop_memory,
        'OS': laptop_os,
        'Storage': laptop_storage,
        'Display': laptop_display,
        'Inclusion': laptop_inlcusion
    }
    
    df = pd.DataFrame(data)
    df.to_csv('laptop_data.csv', index=False)
    print("Data saved to laptop_data.csv")

if __name__ == '__main__':
    save_to_csv()  # Call the save function
    driver.quit()  # Close the WebDriver
