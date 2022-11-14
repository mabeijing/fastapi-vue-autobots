# @Time 2022/11/11 17:34
# Author: beijingm

import requests

BASE_URL = "http://10.148.61.40"

# 请求product的api
product_search = "/api/gcc/product/search"

session = requests.Session()

session.headers.update({"session": "c3da6b2483fca098f5ffb7428e5d6ab6"})

data = {"page": 1, "pageSize": 9, "userName": "beijingm", "productName": "vcenter-all", "statuses": []}
resp = session.post(BASE_URL + product_search, json=data)

product: dict = resp.json()["data"]["rows"][0]

source_pipeline = product.pop("sourcePipeline")
translation_pipeline = product.pop("translationPipeline")
user_data = product.pop("data")

# print(product)
print(source_pipeline)