from bs4 import BeautifulSoup
import requests
import json
import traceback
import csv, random

agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    ]

BASE_URL = "https://www.reefh2o.com/searchresults.asp?Search={}"
DOMAIN = "https://www.reefh2o.com"

def search_central_pet(queries: list, export=True):
    urls = [BASE_URL.format(q) for q in queries]
    search_result = dict()

    for url in urls:
        try:
            print(f"Fetching for {url}")
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
                response = requests.get(url, headers=headers)
            except:
                continue
            soup = BeautifulSoup(response.content, "html.parser")
            with open("reef.html", "w") as f:
                f.write(soup.prettify())

            product_data = list()
            try:
                product_list = soup.find_all("div", class_="v-product-grid")[0].find_all("div", class_="v-product")
            except:
                print(traceback.format_exc())
                nurl = BASE_URL.format(" ".join(queries[urls.index(url)].split(" ")[:3]))
                print(nurl)
                try:
                    response = requests.get(nurl, headers=headers)
                except:
                    continue
                soup = BeautifulSoup(response.content, "html.parser")
                
                try:
                    product_list = soup.find_all("div", class_="v-product-grid")[0].find_all("div", class_="v-product")
                except:
                    print(traceback.format_exc())
                    product_list = []

            for product in product_list:
                try:
                    product_title  = product.find("a", "v-product__title").text.strip()
                    product_url = product.find("a", "v-product__img").attrs["href"]
                    product_price = "$"+product.find_all("p", class_="v-product__desc")[0].find("span").text.strip().split("$")[1]
                    product_preview = DOMAIN+product.find("a", "v-product__img").find("img").attrs["src"]
                    
                    product_info = {"product_title": product_title, "product_price": product_price, "product_preview": product_preview, "product_url": product_url}
                    product_data.append(product_info)
                except Exception as e:
                    print(traceback.format_exc())
                    pass

            search_result[queries[urls.index(url)]] = product_data
            
            print(f"Exporting {len(product_data)}...")
        except KeyboardInterrupt:
            break
        
    with open("exports/reef.json", "w") as f:
        json.dump(search_result, f, indent=4)
    f.close()

    return search_result

queries  = []
with open("exports/dynamics.csv", "r") as f:
    r = csv.reader(f)
    header = next(r)
    for row in r:
        queries.append(row[0].strip())

print(search_central_pet(queries=queries, export=True))
