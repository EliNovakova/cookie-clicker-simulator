import time
from selenium import webdriver


CHROME_DRIVER_PATH = r"<INSERT-CHROME-DRIVER-PATH>"     # r before the string converts normal string to a path string
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)   # creates the driver which is going to drive and interact with the website

driver.get("http://orteil.dashnet.org/experiments/cookie/")
cookie_click = driver.find_element_by_css_selector("#cookie")   # locates cookie
money = driver.find_element_by_css_selector("#money")   # locates money

timeout = time.time() + 5   # every 5 seconds
five_min = time.time() + 60*5   # 5minutes

while True:     # loop runs
    cookie_click.click()    # clicks cookie

    # Every 5 seconds:
    if time.time() > timeout:
        store = driver.find_elements_by_css_selector("#store b")  # locates all items in the store
        affordable_items = {}

        # list of keys
        store_ids = []  # creating list of keys (item names) for future dictionary
        for store_id in store:  # takes out each name of an item from store
            if len(store_id.text.split(
                    "- ")) == 2:  # only in case text split in two (name - price) (there is some kind if an exception)
                store_ids.append((store_id.text.split("- ")[
                    0]))  # we get the items text and split it by the dash (first part is its name)

        # list of values
        store_prices = []  # creating list of values (item prices) for future dictionary
        for store_price in store:  # takes out each price of an item from store
            if len(store_price.text.split("- ")) == 2:  # only in case text split in two (name - price) (there is some kind if an exception)
                store_prices.append((store_price.text.split("- ")[1]).replace(",", ""))  # we get the items text and split it by the dash (second part is its price), plus we need to get rid of the coma so it can be converted to int later

        # dictionary comprehension
        store_dict = {store_ids[i]: store_prices[i] for i in
                      range(len(store_ids))}  # creates dictionary where names are keys and price

        for id, price in store_dict.items():    # for each item in store
            if int(money.text) >= int(price):   # if we have more money than some item costs (we can afford it)
                affordable_items[int(price)] = id  # dict item is added to a new dictionary called affordable_items
        highest_price_item = max(affordable_items)     # gets max key (price)
        print(affordable_items)
        print(store_dict)
        print(highest_price_item)
        buy_item = affordable_items[highest_price_item]     # gets max keys value (id of most expensive item)
        print(buy_item)
        driver.find_element_by_css_selector(f"#buy{buy_item}") .click()    # locates this item in the store by its id (name)
        # clicks that item = buys it

        timeout = time.time() + 5

    if time.time() > five_min:
        cookie_per_s = driver.find_element_by_id("cps").text
        print(cookie_per_s)


    print(money.text)
