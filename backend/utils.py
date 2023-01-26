import json, csv
from collections import defaultdict
from flask import jsonify

filename = "dynamicsDB.json"
dynamics_fname = "dynamics.csv"

db = open(filename, "r")
DATA = json.load(db)

dynamics_list = open(dynamics_fname, "r")
reader = csv.reader(dynamics_list)
h = next(reader)
DYNAMICS_LIST = [{"product_title": row[0], "product_price": row[1], "product_preview": row[2]} for row in reader]

def match_query(query: str, data_list: list) -> list:
    d = defaultdict()
    query_split = query.split(" ")

    for chunk in data_list:
        for word in query_split:
            count = 0
            if word in chunk["product_title"]:
                count += 1
            d[chunk["product_title"]] = (count, data_list.index(chunk))
    
    d_val = [v[0] for v in list(d.values())]
    high = max(d_val)

    high_matches = [d[k] for k in d if d[k][0] == high]
    match_indices = [m[1] for m in high_matches]
    high_matches = [data_list[i] for i in match_indices]

    return high_matches

def product_price_order(products):
    prices = []
    for product in products:
        if product.get("product_price"):
            if "-" in product["product_price"]:
                p = product["product_price"].split("-")[1].replace("$", "").replace(",", "").strip()
                prices.append(float(p))
            else:
                prices.append(float(product["product_price"].replace("$", "").replace(",", "").strip()))
    
    highest_value = max(prices)
    cheapest_value = min(prices)

    highest_product, cheapest_product = None, None

    for product in products:
        if product.get("product_price"):
            if "-" in product["product_price"]:
                p = product["product_price"].split("-")[1].replace("$", "").replace(",", "").strip()
                if float(p) == highest_value and not highest_product:
                    highest_product = product
                if float(p) == cheapest_value and not cheapest_product:
                    cheapest_product = product
            else:
                if float(product["product_price"].replace("$", "").replace(",", "").strip()) == highest_value and not highest_product:
                    highest_product = product
                if float(product["product_price"].replace("$", "").replace(",", "").strip()) == cheapest_value and not cheapest_product:
                    cheapest_product = product
            
            if highest_product and cheapest_product:
                break
    
    return highest_product, cheapest_product
    
def search(query):
    matches = match_query(query, DYNAMICS_LIST)
    product_list = list()

    for match in matches:
        product_list.extend(DATA["amazon"].get(match["product_title"], []))
        product_list.extend(DATA["saltwateraquarium"].get(match["product_title"], []))
        product_list.extend(DATA["bulkreef"].get(match["product_title"], []))
    
    highest, cheapest = product_price_order(products=product_list)
    dynamic_h, dynamic_c = product_price_order(matches)
    response = jsonify({
        "count": len(product_list), "product_metric": {"highest": highest, "cheapest": cheapest}, 
        "dynamic_metric": {"highest": dynamic_h, "cheapest": dynamic_c}, "products": product_list
        })
    response.headers["access-control-allow-origin"] = "*"
    return response
    

def get_all_products(limit=40, page=1):
    products_data = list()
    print(len(DYNAMICS_LIST))
    page = (int(page)-1) * int(limit)
    limit = int(page) + int(limit)
    print(page, limit)
    for product in DYNAMICS_LIST[page: limit]:
        # matches = match_query(product["product_title"], DYNAMICS_LIST)
        product_info = {
            "product_data": {
                "amazon": DATA["amazon"].get(product["product_title"], []),
                "bulkreef": DATA["bulkreef"].get(product["product_title"], []),
                "saltwateraquarium": DATA["saltwateraquarium"].get(product["product_title"], [])
            },
            "title": product["product_title"],
            "price": product["product_price"],
            "preview": product["product_preview"]
        }
        
        total_product_list = product_info["product_data"]["amazon"]+product_info["product_data"]["bulkreef"]+product_info["product_data"]["saltwateraquarium"]
        highest, cheapest = product_price_order(products=total_product_list)
        product_info["product_data"].update({
            "highest": highest,
            "cheapest": cheapest,
            "product_name": product
        })

        products_data.append(product_info)
    
    response = jsonify({"data": products_data})
    response.headers["access-control-allow-origin"] = "*"

    return response



# f1 =  open("exports/amazon.json", "r")
# f2 = open("exports/salt.json", "r")
# f3 = open("exports/bulkreef.json", "r")

# amaz = json.load(f1)
# salt = json.load(f2)
# breef = json.load(f3)

# with open("exports/dynamicsDB.json", "w") as f:
#     new_data = {"amazon": amaz, "saltwateraquarium": salt, "bulkreef": breef}
#     json.dump(new_data, f, indent=4)

# f.close()
