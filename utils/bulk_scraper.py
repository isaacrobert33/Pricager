from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.safari.options import Options
import time, json, csv

BASE_URL = "https://www.bulkreefsupply.com/catalogsearch/result?q="
driver_options = Options()
driver_options.add_argument("--headless")
# ext = Extractor.from_yaml_file("bulkreef.yml")

def search_bulkreef(queries, export=False):
    urls = [f"{BASE_URL}{q}" for q in queries]
    search_result = dict()

    for url in urls:
        try:
            driver = webdriver.Safari(options=driver_options)
            
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "result-wrapper"))
                )
            except Exception as e:
                print(Exception)
                driver.quit()
            try:
                product_list = driver.find_element(By.CLASS_NAME, "ais-Hits-list").find_elements(By.CLASS_NAME, "ais-Hits-item")
            except:
                product_list = []
                
            product_data = list()

            for product in product_list:
                try:
                    try:
                        product_title  = product.find_element(By.CSS_SELECTOR, "h2.result-title").text.strip()
                        product_url = product.find_element(By.CSS_SELECTOR, "a.result").get_attribute("href")
                        product_price = product.find_element(By.CSS_SELECTOR, "span.price-wrapper").text.strip()
                        product_preview = product.find_element(By.TAG_NAME, "img").get_attribute("src")
                        product_category = product.find_element(By.CSS_SELECTOR, "div.product-brand").text.strip()
                        product_info = {"product_title": product_title, "product_price": product_price, "product_category": product_category, "product_preview": product_preview, "product_url": product_url}
                        product_data.append(product_info)
                    except KeyboardInterrupt:
                        break
                except Exception as e:
                    print(f"[!] Error fetching a product\n{e}")
            
            search_result[queries[urls.index(url)]] = product_data

            print(f"[*] Exported {len(product_data)} products")
            
            driver.close()
        except KeyboardInterrupt:
            break

    if export:
        with open("exports/bulkreef_search.json", "w") as f:
            json.dump(search_result, f, indent=4)
        f.close()

    return search_result

queries  = []
with open("exports/dynamics.csv", "r") as f:
    r = csv.reader(f)
    header = next(r)
    for row in r:
        queries.append(row[0].strip())

print(f"Searching for {len(queries)} products...")
ret = search_bulkreef(queries=queries, export=True)
print(ret)