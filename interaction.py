from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

option = Options()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = option)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

#Prices in the store
store_items_price = driver.find_elements(By.CSS_SELECTOR, "div #store b")
prices = []
store = [items.text.split('-') for items in store_items_price]
stores = store[:-1]
for item in stores:
    if item != "":
        gadgets = int(item[1].strip().replace(",",""))
        prices.append(gadgets)

#Scrapping all the ids in the store
store_items = driver.find_elements(By.CSS_SELECTOR, "#store div")
store_ids = [id.get_attribute("id") for id in store_items]

#Creating a dictionary for items and prices
store_dic = {}
for i in range(0,len(prices)):
    store_dic[prices[i]] = store_ids[i]

#Every 5 sec
five_sec = time.time() + 5
end_time = time.time() + (5*60)

while True:
    clicker = driver.find_element(By.ID, "cookie")
    clicker.click()
    if time.time() > five_sec:
        # Obtaining Total Cookies
        money = driver.find_element(By.ID, "money").text
        if "," in money:
            money = money.replace(",", "")
        cookie_count = int(money)

        #Find the affordable upgrade
        affordable_dic = {}
        for price, ids in store_dic.items():
            if cookie_count > price:
                affordable_dic[price] = ids

            #Purchase the highest number
        max_affordable_upgrade = max(affordable_dic)
        to_purchase_item = affordable_dic[max_affordable_upgrade]
            #Clicks the expenesive item
        driver.find_element(By.ID, f"{to_purchase_item}").click()
        five_sec = time.time() + 5

    if time.time() > end_time:
        cps = driver.find_element(By.ID, "cps")
        print(cps.text)
        break

driver.quit()
