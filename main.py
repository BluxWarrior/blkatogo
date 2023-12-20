import requests
import json
from datetime import datetime
from pathlib import Path

bodies = {"Sodavand": "body.sodavand", "Vand & danskvand": "body.vand", "Energidrikke": "body.energidrikke"}
current_date = datetime.now().strftime("%d/%m/%Y")
with open("header", "r", encoding='utf-8') as f:
    headers = json.load(f)

def get_products(body, category):
    res = requests.post(url, headers= headers, data= body)
    data = res.json()["results"][0]["hits"]

    products = []
    for dt in data:
        name = dt["_highlightResult"]["name"]["value"]
        brand = dt["_highlightResult"]["brand"]["value"]
        id = dt["objectID"]
        purl = "https://www.bilkatogo.dk/produkt/" + brand.replace(" ", "-").replace(".", "") + "-" + name.replace(" ", "-").replace(".", "") + f'/{id}/'
        storedata = dt["storeData"]

        description = ""
        for sd in dt["infos"]:
            if sd["title"] == "Produkt detaljer":
                description = [{ele["title"]: ele["value"]} for ele in sd["items"]]
        # for item in description:
        #     item.pop('type', None)
        pd = {
            "Category": category,
            "Name": name,
            "Url": purl,
            "Price": storedata[list(storedata.keys())[0]]["price"] / 100,
            "Description": description,
            "Date": current_date
        }

        products.append(pd)
    print(len(data))
    return products

with open("header", "r", encoding='utf-8') as f:
    headers = json.load(f)
url = "https://f9vbjlr1bk-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.3)%3B%20Browser"


data = []
for ct in bodies:
    with open(bodies[ct], "rb") as f:
        body = f.read()
        products = get_products(body, ct)
        data += products

data_file = Path("data.json")
if data_file.exists():
    try:
        with data_file.open("r", encoding="utf-8") as f:
            existing_data = json.load(f)
    except:
        existing_data = []
    
    data += existing_data


with data_file.open("w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)