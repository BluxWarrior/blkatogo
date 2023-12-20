from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import json

# options = Options()
# options.add_argument("--headless")
# driver = webdriver.Chrome(options= options)
# driver.get("https://www.bilkatogo.dk/kategori/drikkevarer/sodavand")
# time.sleep(2)
# for req in driver.requests:
#     headers = req.headers
#     url = req.url
#     data = req.body
    
#     if "algolia.net" in url:
#         print(url)
#         with open("body", "wb") as f:
#             f.write(data)
        
#         with open("header", "w", encoding= 'utf-8') as f:
#             json.dump(dict(headers), f)
#         print(headers)
#         break
    
url = "https://f9vbjlr1bk-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.3)%3B%20Browser"
with open("body.energidrikke", "rb") as f:
    data = f.read()
# data = data.encode()
with open("header", "r", encoding='utf-8') as f:
    headers = json.load(f)
res = requests.post(url, headers= headers, data= data)
# print(res.json())
print(res.status_code)
result = res.json()["results"][0]["hits"]
print(len(result))
with open("result.json", "w", encoding='utf-8') as f:
    json.dump(result, f, indent=4)
