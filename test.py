# -*- coding: utf-8 -*-
# @Time    : 2024/1/12 20:36
# @Author  : nongbin
# @FileName: test.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import json

#以post方式请求http接口
import requests
# 第一个模型
url = "http://127.0.0.1:18880/credit/evaluation"

with open("./entropy_weight/model1_input.json", 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

response = requests.post(url, json=json_data)
print(response.json())



# 第二个模型
url = "http://127.0.0.1:18880/operation/efficiency"

with open("./entropy_weight/model2_input.json", 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

response = requests.post(url, json=json_data)
print(response.json())


# 第三个模型
url = "http://127.0.0.1:18880/operation/risk"

with open("./entropy_weight/model1_input.json", 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

response = requests.post(url, json=json_data)
print(response.json())