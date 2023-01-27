from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, json, csv, random, traceback
from requests_html import HTMLSession

BASE_URL = "https://www.bulkreefsupply.com/catalogsearch/result?q="
agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    ]
driver_options = Options()
driver_options.add_argument("--headless")
# ext = Extractor.from_yaml_file("bulkreef.yml")

def search_2(queries: list):
    urls = [f"{BASE_URL}{q}" for q in queries]
    search_result = dict()
    session = HTMLSession()
    for url in urls:
        try:
            headers = {
                'dnt': '1',
                'upgrade-insecure-requests': '1',
                'user-agent': random.choice(agents),
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-user': '?1',
                'sec-fetch-dest': 'document',
                'referer': 'https://www.amazon.com/',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            }

            try:
                resp = session.get(url=url, headers=headers)
                resp.html.render()
            except:
                print(traceback.format_exc())
                continue
            
            with open("reef_2.html", "w") as f:
                f.write(resp.html.html)

            soup = BeautifulSoup(resp.html.html, "html.parser")
            product_list = soup.find("ol", "ais-Hits-list").find_all("li", class_="ais-Hits-item")
            product_data = list()
            for product in product_list:
                product_title  = product.find("h2", "result-title").text.strip()
                product_url = product.find("a", "result").attrs["href"]
                product_price = product.find("span", "price-wrapper").text.strip()
                product_preview = product.find("img").attrs["src"]
                product_category = product.find("div", "product-brand").text.strip()
                product_info = {"product_title": product_title, "product_price": product_price, "product_category": product_category, "product_preview": product_preview, "product_url": product_url}
                product_data.append(product_info)

            search_result[queries[urls.index(url)]] = product_data
        except (KeyboardInterrupt):
            break
    
    print(f"[*] Exported {len(product_data)} products")

    with open("exports/bulkreef_search3.json", "w") as f:
        json.dump(search_result, f, indent=4)
    f.close()

    return search_result


def search_bulkreef(queries, export=False):
    urls = [f"{BASE_URL}{q}" for q in queries]
    search_result = dict()
    driver = webdriver.Chrome(options=driver_options)
    
    for url in urls:
        try:
            try:
                driver.get(url)
            except:
                print(traceback.format_exc())
                continue
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "result-wrapper"))
                )
            except Exception as e:
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
            
        except KeyboardInterrupt:
            break

    with open("bulkreef_3.json", "w") as f:
        json.dump(search_result, f, indent=4)
    f.close()

    return search_result

queries  = []
with open("backend/dynamics.csv", "r") as f:
    r = csv.reader(f)
    header = next(r)
    for row in r:
        queries.append(row[0].strip())

print(f"Searching for {len(queries[641:])} products...")
ret = search_bulkreef(queries=queries[404:], export=True)
# ret = search_2(queries=queries)
print(ret)