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
sales = []
with_card = []
# data dict
data = {}

# terms
terms = ['pollo', 'arroz']
# urls dict
url = 'https://www.jumbo.cl/busqueda?ft='

urls = [url + term for term in terms]

print(urls, end='\n')

def delay(sec):
    print(f"delay of {sec} seconds", end='\n')
    pbar = tqdm(total=100)
    for i in range(sec):
        time.sleep(1)
        pbar.update(100/sec)
    pbar.close()

def collect_jumbo(urls):
    for url in urls:
        print(f'getting data of: Jumbo', end='\n')
        print(f'searching: {url}', end='\n')
  
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

            sale = item.find_elements(By.CLASS_NAME, 'prices-price price-box order-1')
            if len(sale) > 0:
                sales.append(sale[0].text)
            else:
                sales.append("")

            cards = item.find_elements(By.CLASS_NAME, 'prices-price price-box order-4')
            if len(cards) > 0:
                with_card.append(cards[0].text)
            else:
                with_card.append("")
            
        delay(5)

collect_jumbo(urls)

driver.quit()

data["super"] = super
data["name"] = name
data["price"] = price
data["unit"] = unit
data["brand"] = brand
data["sales"] = sales
data["with_card"] = with_card

df = pd.DataFrame(data)

print(df.shape)
df.to_csv('results.csv', index=False)
