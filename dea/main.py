import json
import os
from typing import Dict, List

import pandas as pd
from pyDEA.core.data_processing.parameters import Parameters
from pyDEA.core.utils.dea_utils import clean_up_pickled_files
from pyDEA.core.utils.run_routine import RunMethodTerminal

def get_dea_result(json_data):

    #
    # todo 在这里将json数据转化成excel表格,注意有6列数据，存入./data/DEAtestData.xlsx， 包含三张表单对应三年的数据，sheet1， sheet2， sheet3
    # 注意：传输多年的数据,转化为json，同时返回所有年份
    years = json2excel(json_data)

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
        # 获取计算函数（方法）
        run_method = RunMethodTerminal(params=para
                                       , sheet_name_usr=f"{year}"  # 这个参数表示使用哪张表单，已经以年份命名表单
                                       , output_format='xlsx'  # 设置输出格式，也可设置成csv，如果是csv结果保存在data/DEAtestData_result中
                                       , output_dir=f"./data/result/{year}")
        run_method.run(para)
        clean_up_pickled_files()  # 清除临时文件

    result = None

    #
    # todo 从excel表格数据中读取efficiencyScore的数据，转化为json，赋值给result

    return result

def json2excel(json_data)->List[str]:
    companies_info = json_data["data"]
    years = [] # 收集年份

    excel_writer = get_excel_writer()

    for year in companies_info:
        years.append(year)
        all_company_data: Dict[str, dict] = companies_info[year]

        indexes = [] # 收集公司名称，用于构建dataFrame的row index
        every_company_info = [] # dea模型的输入数据
        for company_name in all_company_data:
            company_data: Dict[str, float] = all_company_data[company_name]
            indexes.append(company_name)
            every_company_info.append(company_data)

        df = pd.DataFrame(every_company_info, index=indexes)
        df.to_excel(excel_writer, sheet_name=year)

    excel_writer.close()

    return years

def excel2json(years):
    for year in years:
        result = pd.read_excel(f"./data/result/{year}/input_result.xlsx"
                                , sheet_name="EfficiencyScores"
                                , engine="openpyxl").to_json()
    # todo:检查json格式是否正确
    # todo:计算综合得分
def get_excel_writer(file_name = "input.xlsx"):
    # 判断data文件夹是否存在
    if not os.path.exists("./data"):
        os.mkdir("./data")

    return pd.ExcelWriter(os.path.join("./data", file_name))

if __name__ == "__main__":
    get_dea_result(None)
