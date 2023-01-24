from bs4 import BeautifulSoup
import requests
import json
import csv
import random

BASE_URL = "https://www.saltwateraquarium.com/search.php?search_query={}&section=product"
agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    ]
  
def search_saltwater(queries: list, export=False):
    urls = [BASE_URL.format(q) for q in queries]
    search_result = dict()

    for url in urls:
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
        product_data = list()
        try:
            product_list = soup.find("div", "products-list").find_all("div", class_="product-layout")
        except:
            product_list = []

        for product in product_list:
            try:
                try:
                    product_title  = product.find_all("h4", class_="card-title")[0].text.strip()
                    product_url = product.find_all("h4", class_="card-title")[0].find("a").attrs["href"]
                    product_price = product.find_all("span", class_="price")[0].text.strip()
                    product_preview = product.find_all("img", class_="img-responsive")[0].attrs["src"]
                    product_category = product.find_all("p", class_="card-text")[0].text

                    product_info = {"product_title": product_title, "product_price": product_price, "product_category": product_category, "product_preview": product_preview, "product_url": product_url}
                    product_data.append(product_info)
                except KeyboardInterrupt:
                    break
            except:
                pass

        search_result[queries[urls.index(url)]] = product_data
    
    with open("exports/salt.json", "w") as f:
        json.dump(search_result, f, indent=4)
    f.close()

    return search_result

queries  = []
with open("exports/dynamics.csv", "r") as f:
    r = csv.reader(f)
    header = next(r)
    for row in r:
        queries.append(row[0].strip())

print(search_saltwater(queries=queries, export=True))
