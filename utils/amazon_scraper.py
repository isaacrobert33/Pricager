from selectorlib import Extractor
import requests 
import json, csv
from time import sleep
import random
# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('templates/amazon.yml')
BASE_URL = "https://www.amazon.com/s?k="
agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    ]

def scrape(url):  
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

    # Download the page using requests
    print("Downloading %s"%url)
    try:
        r = requests.get(url, headers=headers)
    except:
        return {"products": []}

    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return {"products": []}
    # Pass the HTML of the page and create 
    return e.extract(r.text)

def search_amazon(queries: list, export: bool=False):
    url_list = [f"{BASE_URL}{query}" for query in queries]
    search_result = dict()
    for url in url_list:
        try:
            data = scrape(url=url)
            if not data:
                raise "[!] Error fetching data from amazon"

            product_list = [{**product, **{"search_url": url}} for product in data["products"]]
            print(f"Got {len(product_list)} products!")
            search_result[queries[url_list.index(url)]] = product_list
        except KeyboardInterrupt:
            break
    
    print("Exporting result...")
    with open("amazon.json", "w") as f:
        json.dump(search_result, f, indent=4)
    f.close()

    return search_result

queries  = []
with open("exports/dynamics.csv", "r") as f:
    r = csv.reader(f)
    header = next(r)
    for row in r:
        queries.append(row[0].strip())


ret = search_amazon(
        queries=queries,
        export=True
    )
# print(ret)