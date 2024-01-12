# -*- coding: utf-8 -*-
# @Time    : 2024/1/12 20:27
# @Author  : nongbin
# @FileName: operation_effi.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn
import os
import shutil
from collections import defaultdict
from typing import Dict, List

import pandas as pd
from pyDEA.core.data_processing.parameters import Parameters
from pyDEA.core.utils.dea_utils import clean_up_pickled_files
from pyDEA.core.utils.run_routine import RunMethodTerminal

__dea_columns_map = {"net_profit_end": "O1", "operating_income_end": "O2", "assets_amount_end": "I1",
                     "debt_amount": "I2", "owner_equity_current": "I3", "operating_cost": "I4"}


def evaluate(data, total, group):
    #
    # 注意：传输多年的数据,转化为json，同时返回所有年份
    years = json2excel(data)

    # 设置参数（为了快速验证，先不采用配置的方式）,直接赋值。
    para = Parameters()
    # update_parameter方法用于向Parameters对象中设置参数。参数是以字典的形式进行存储，key是参数名，value是参数值。
    para.update_parameter("DATA_FILE", "./data/input.xlsx")  # 模型输入数据（excel表格，也可以是csv文件）
    para.update_parameter('DEA_FORM', 'env')  # 一般保持不变
    para.update_parameter('ORIENTATION', 'input')  # 一般保持不变
    para.update_parameter('OUTPUT_CATEGORIES', 'O2;O1')  # 设置输入表格中哪些列是公司的产出系数，比如这里设置'O2;O1'，因为输入表格中这两列是公司的产出指标
    para.update_parameter('MULTIPLIER_MODEL_TOLERANCE', '0')  # 一般保持不变
    para.update_parameter('RETURN_TO_SCALE', 'VRS')  # 暂时保持i不变
    para.update_parameter('INPUT_CATEGORIES',
                          'I2;I3;I1;I4')  # 设置输入表格中哪些列是公司的投入系数，比如这里设置'I2;I3;I1;I4'，因为输入表格中这两列是公司的产出指标

    for year in years:
        result_path = f"./data/result/{year}"
        make_sure_path_exists(result_path)
        # 获取计算函数（方法）
        run_method = RunMethodTerminal(params=para
                                       , sheet_name_usr=f"{year}"  # 这个参数表示使用哪张表单，已经以年份命名表单
                                       , output_format='xlsx'  # 设置输出格式，也可设置成csv，如果是csv结果保存在data/DEAtestData_result中
                                       , output_dir=result_path)
        run_method.run(para)
        clean_up_pickled_files()  # 清除临时文件

    # 从excel表格数据中读取efficiencyScore的数据，转化为json，赋值给result
    result = excel2json(years)
    return {'code': 200, "data":result}


def make_sure_path_exists(path: str):
    """如果路径不存在，则创建路径"""
    if not os.path.exists(path):
        os.makedirs(path)


def json2excel(json_data) -> List[str]:
    companies_info = json_data
    years = []  # 收集年份

    excel_writer = get_excel_writer()
    company_names = None
    for year in companies_info:
        years.append(year)
        all_company_data: Dict[str, dict] = companies_info[year]
        if not company_names:
            company_names = list(all_company_data.keys())

        every_company_info = defaultdict(list)  # dea模型的输入数据
        for company_name in company_names:
            company_data: Dict[str, float] = all_company_data[company_name]
            for field in company_data:
                every_company_info[__dea_columns_map[field]].append(float(company_data[field]))

        df = pd.DataFrame(every_company_info, index=company_names)
        # 遍历每一列，对每一列进行归一化
        for column in df.columns:
            df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
        df.to_excel(excel_writer, sheet_name=year)

    excel_writer.close()

    return years


def excel2json(years):
    scores = {}
    for year in years:
        result = pd.read_excel(f"./data/result/{year}/input_result.xlsx"
                               , sheet_name="EfficiencyScores"
                               , engine="openpyxl")
        # 复制本地excel文件
        shutil.copy(f"./data/result/{year}/input_result.xlsx", f"./data/result/{year}/result.xlsx")
        os.remove(f"./data/result/{year}/input_result.xlsx")
        ## 遍历dataframe每一行，取出每一行的数据
        for index, row in result.iterrows():
            if index == 0:
                continue
            company_name = row[0]
            if company_name not in scores:
                scores[company_name] = {}
            scores[company_name][str(year)] = row[1]
    # 计算综合得分
    for company_name in scores:
        scores[company_name]["final"] = sum(scores[company_name].values()) / len(scores[company_name])

    return scores


def get_excel_writer(file_name="input.xlsx"):
    # 判断data文件夹是否存在
    if not os.path.exists("./data"):
        os.mkdir("./data")

    return pd.ExcelWriter(os.path.join("./data", file_name))
