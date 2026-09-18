import requests
from bs4 import BeautifulSoup
import json, csv, time, random
from selenium import webdriver

def scrape_dynamic_site(url, output="products.json"):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    products = []
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2 + random.random())
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for item in soup.select(".product-item"):
            try:
                name = item.select_one(".product-title").text.strip()
                price = item.select_one(".price").text.strip()
                products.append({"name": name, "price": price})
            except: continue
    driver.quit()
    cleaned = [p for p in products if p['name'] and p['price']]
    with open(output, 'w') as f:
        json.dump(cleaned, f, indent=2)
    return cleaned
