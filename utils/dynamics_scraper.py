from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests, csv, time

SURL = "https://www.amazon.com/s?k=NYOS+HIGH+SENSITIVITY+SEAWATER+MAGNESIUM+REEFER+TEST+KIT+%2850+TESTS%29"

driver = webdriver.Safari()
driver.get(SURL)
time.sleep(5)
driver.find_elements()
driver.close()

###### Dynamics products ####
# BASE_URL = "https://shopdynamictank.com"
# URL = "https://shopdynamictank.com/collections"
# # driver = webdriver.Firefox("./")
# # driver.get(URL)

# # driver.close()

# main_page = requests.get(URL)
# main_soup = BeautifulSoup(main_page.content, "html.parser")
# col_list = main_soup.find_all("div", class_="grid__cell")
# head = False
# for collection in col_list:
#     col_link = f'{BASE_URL}{collection.find("a", class_="collection-block-item").attrs["href"]}'
#     print(f"fetching collection: {col_link}...")
#     response = requests.get(col_link)
#     soup = BeautifulSoup(response.content, "html.parser")

#     with open("pg.html", "w") as f:
#         f.write(soup.prettify())

#     product_list = soup.find_all(class_="product-item")
#     product_data = []
#     for product in product_list:
#         try:
#             product_title = product.find(class_="product-item__title").text
#             product_price  = "$"+product.find("span", class_="price").text.split("$")[1]
#             product_category = product.find("a", class_="product-item__vendor").text
#             product_image_link = "https:"+product.find("img", class_="product-item__primary-image").attrs["data-src"].format(width="200")
            
#             product_data.append([product_title, product_price, product_image_link, product_category])
#         except:
#             print("[*] Error getting a product")
#             pass

#     with open("dynamics.csv", "a") as f:
#         writer = csv.writer(f)
#         if not head:
#             writer.writerow(["Product Title", "Product Price", "Product Preview", "Product Category"])
#             head = True
#         writer.writerows(product_data)
        
        
#     print(f"Exported {len(product_data)} product data")
