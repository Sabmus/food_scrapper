import time
from tqdm import tqdm
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


# instantiate options
options = webdriver.ChromeOptions() 
# run browser in headless mode 
options.add_argument('--headless')
#options.add_argument('--disable-notifications')
#options.add_argument('--disable-extensions')
options.add_argument('--log-level=3') 
#options.add_argument('--ignore-certificate-errors')
#options.add_argument('--ignore-ssl-errors')
#options.add_experimental_option("excludeSwitches", ["enable-automation"])
#options.add_experimental_option('useAutomationExtension', False)
# create driver
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

# lists of data
super = []
name = []
price = []
unit = []
brand = []
# data dict
data = {}

# terms
terms = ['pollo', 'arroz']
# urls dict
urls = {'jumbo': 'https://www.jumbo.cl/busqueda?ft=',
        'lider': 'https://www.lider.cl/supermercado/search?query='}

urls_dict = {}
# create dict of urls
for k, v in urls.items():
    urls_dict[k] = [v + term for term in terms]
print(urls_dict)
print("\n"*2)

def delay(sec):
    print('\n')
    print(f"delay of {sec} seconds")
    print('\n')
    pbar = tqdm(total=100)
    for i in range(sec):
        time.sleep(1)
        pbar.update(100/sec)
    pbar.close()

def collect_jumbo(urls):
    for url in urls:
        print("\n")
        print(f'getting data of: Jumbo')
        print("\n"*2)
        print(f'searching: {url}')
        print("\n")

        driver.get(url)

        # select elements by class name
        elements = driver.find_elements(By.CLASS_NAME, 'product-card')

        for item in tqdm(elements):
            #if(len(item.find_elements(By.CLASS_NAME, 'out-of-stock')) != 0):
            #    continue
            super.append("jumbo")
            name.append(item.find_element(By.CLASS_NAME, 'product-card-name').text)
            price.append(item.find_element(By.CLASS_NAME, 'prices-main-price').text)
            unit.append(item.find_element(By.CLASS_NAME, 'unitMeasurement').text)
            brand.append(item.find_element(By.CLASS_NAME, 'product-card-brand').text)
            
        delay(10)

def collect_lider(urls):
    for url in urls:
        print("\n")
        print(f'getting data of: Lider')
        print("\n"*2)
        print(f'searching: {url}')
        print("\n")

        driver.get(url)

        # select elements by class name 
        elements = driver.find_elements(By.CLASS_NAME, 'ais-Hits-item')

        for item in tqdm(elements): 
            super.append(k)
            name.append(item.find_element(By.CLASS_NAME, 'product-card_description-wrapper').text)
            price.append(item.find_element(By.CLASS_NAME, 'product-card__sale-price').text)
            unit.append(0)
            brand.append("")
        
        delay(10)


collect_jumbo(urls_dict["jumbo"])
collect_lider(urls_dict["lider"])

driver.quit()

data["super"] = super
data["name"] = name
data["price"] = price
data["unit"] = unit
data["brand"] = brand

df = pd.DataFrame(data)

print(df.shape)
print(df.describe)
