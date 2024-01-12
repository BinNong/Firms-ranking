# -*- coding: utf-8 -*-
# @Time    : 2024/1/12 20:04
# @Author  : nongbin
# @FileName: app.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn

from flask import Flask, request
from model import credit_eval, operation_effi, operation_risk

app = Flask(__name__)


@app.route('/credit/evaluation', methods=['POST'])
def evaluate_credit():
    json_data = request.json  # 获取JSON格式的请求数据
    total =json_data["total"]
    data = json_data["data"]
    result = credit_eval.evaluate(data, None, total)
    return result


@app.route('/operation/efficiency', methods=['POST'])
def evaluate_operation_efficiency():
    json_data = request.json  # 获取JSON格式的请求数据
    return operation_effi.evaluate(json_data["data"], json_data["total"], json_data["group"])


@app.route('/operation/risk', methods=['POST'])
def evaluate_operation_risk():
    json_data = request.json  # 获取JSON格式的请求数据
    return operation_risk.evaluate(json_data["data"], json_data["total"], json_data["group"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18880)
