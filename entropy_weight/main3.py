import json
import pandas as pd
import numpy as np

file_name = 'model1_input.json'


def start_dataframe(input_file_path):
    # 获取公司名称并使用Dataframe存储在result_df中
    with open(input_file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    columns = json_data['total']
    company_name_list = []

    for i in range(int(columns)):
        company_name = json_data['data'][i]['company_name']
        company_name_list.append(company_name)

    json_data_keys = list(json_data['data'][0].keys())
    company_name_df = pd.DataFrame(company_name_list, columns=['company_name'])

    # 获取全量数据并使用Dataframe存储在concatenated_df中
    list_of_dfs = []
    key_names = []

    for key in json_data_keys[1:]:
        key_names.append(key)
        columns_list_1 = []
        for j in range(int(columns)):
            list1 = json_data['data'][j][key]
            columns_list_1.append(list1)
        list_of_dfs.append(columns_list_1)

    concatenated_df = pd.DataFrame(list_of_dfs).transpose()
    concatenated_df = concatenated_df.apply(lambda col: col.astype(float, errors='ignore') if col.dtype == 'object' else col, axis=0)

    return company_name_df, concatenated_df


# 公司名称和全量数据
company_name_df, concatenated_df = start_dataframe(file_name)


def excel_original_data(concatenated_df):
    # 偿债能力对应的指标
    debt_payment = pd.DataFrame()
    debt_payment['流动比率'] = concatenated_df.iloc[:, 6] / concatenated_df.iloc[:, 11]  # 流动比率
    debt_payment['速动比率'] = (concatenated_df.iloc[:, 6] - concatenated_df.iloc[:, 4] - concatenated_df.iloc[:, 2]) / concatenated_df.iloc[:, 11]  # 速动比率
    debt_payment['资产负债率'] = concatenated_df.iloc[:, 12] / concatenated_df.iloc[:, 10]   # 资产负债率
    debt_payment['经营现金流量负债比'] = concatenated_df.iloc[:, 26] / concatenated_df.iloc[:, 12]  # 经营现金流量负债比
    debt_payment['产权比率'] = concatenated_df.iloc[:, 12] / concatenated_df.iloc[:, 14]  # 产权比率

    # 盈利能力对应的指标
    profit_ability = pd.DataFrame()
    profit_ability['总资产报酬率'] = concatenated_df.iloc[:, 25] / ((concatenated_df.iloc[:, 9] + concatenated_df.iloc[:, 10]) / 2)  # 总资产报酬率
    profit_ability['净资产收益率'] = concatenated_df.iloc[:, 25] / ((concatenated_df.iloc[:, 13] + concatenated_df.iloc[:, 14]) / 2)  # 净资产收益率
    profit_ability['盈余现金保障倍数'] = concatenated_df.iloc[:, 26] / concatenated_df.iloc[:, 25]  # 盈余现金保障倍数
    profit_ability['成本费用利用率'] = concatenated_df.iloc[:, 23] / (concatenated_df.iloc[:, 17] + concatenated_df.iloc[:, 18] + concatenated_df.iloc[:, 19] + concatenated_df.iloc[:, 20])  # 成本费用利用率

    # 经营能力对应的指标
    operation_ability = pd.DataFrame()
    operation_ability['应收账款周转率'] = (concatenated_df.iloc[:, 0] + concatenated_df.iloc[:, 16] - concatenated_df.iloc[:, 1]) / ((concatenated_df.iloc[:, 0] + concatenated_df.iloc[:, 1]) / 2)
    operation_ability['存货周转率'] = concatenated_df.iloc[:, 17] / ((concatenated_df.iloc[:, 3] + concatenated_df.iloc[:, 4]) / 2)
    operation_ability['总资产周转率'] = concatenated_df.iloc[:, 16] / concatenated_df.iloc[:, 10]
    operation_ability['固定资产周转率'] = concatenated_df.iloc[:, 16] / ((concatenated_df.iloc[:, 7] + concatenated_df.iloc[:, 8]) / 2)
    operation_ability['流动资产周转率'] = concatenated_df.iloc[:, 16] / ((concatenated_df.iloc[:, 5] + concatenated_df.iloc[:, 6]) / 2)

    # 发展能力对应的指标
    development_ability = pd.DataFrame()
    development_ability['总资产增长率'] = (concatenated_df.iloc[:, 10] - concatenated_df.iloc[:, 9]) / concatenated_df.iloc[:, 9]
    development_ability['净利润增长率'] = (concatenated_df.iloc[:, 25] - concatenated_df.iloc[:, 24]) / concatenated_df.iloc[:, 24]
    development_ability['营业收入增长率'] = (concatenated_df.iloc[:, 16] - concatenated_df.iloc[:, 15]) / concatenated_df.iloc[:, 15]
    development_ability['营业利润增长率'] = (concatenated_df.iloc[:, 22] - concatenated_df.iloc[:, 21]) / concatenated_df.iloc[:, 21]

    # 企业规模对应的指标
    enterprise_scale = pd.DataFrame()
    enterprise_scale['参保人数'] = concatenated_df.iloc[:, 27]
    enterprise_scale['成立年限'] = concatenated_df.iloc[:, 28]
    enterprise_scale['注册资本'] = concatenated_df.iloc[:, 29]

    # 创新能力对应的指标
    innovation_ability = pd.DataFrame()
    innovation_ability['专利信息'] = concatenated_df.iloc[:, 30]
    innovation_ability['商标信息'] = concatenated_df.iloc[:, 31]
    innovation_ability['著作权'] = concatenated_df.iloc[:, 32]
    innovation_ability['软件著作权'] = concatenated_df.iloc[:, 33]

    # 经营状况对应的指标
    operation_condition = pd.DataFrame()
    operation_condition['供应商'] = concatenated_df.iloc[:, 34]
    operation_condition['客户数量'] = concatenated_df.iloc[:, 35]
    operation_condition['控股企业个数'] = concatenated_df.iloc[:, 36]
    operation_condition['对外投资次数'] = concatenated_df.iloc[:, 37]

    # 企业信用对应的指标
    enterprise_credit = pd.DataFrame()
    enterprise_credit['行政处罚次数'] = concatenated_df.iloc[:, 38]
    enterprise_credit['被执行金额'] = concatenated_df.iloc[:, 39]

    # 合并所有数据框
    all_indicators = pd.concat([debt_payment, profit_ability, operation_ability, development_ability,
                                enterprise_scale, innovation_ability, operation_condition], axis=1)

    new_indicators = all_indicators.copy()

    # 定义两种不同的公式
    def formula_1(x, col):
        return 0.1 + 0.9 * (x - all_indicators[col].min()) / (all_indicators[col].max() - all_indicators[col].min())

    def formula_2(x, col):
        return 0.1 + 0.9 * (all_indicators[col].max() - x) / (all_indicators[col].max() - all_indicators[col].min())

    # 指定需要应用 formula_2 的列索引
    formula_2_columns = [2, 4]

    # 应用公式到指定的列
    for col_index in formula_2_columns:
        col_name = new_indicators.columns[col_index]
        new_indicators[col_name] = new_indicators[col_name].apply(lambda x: formula_2(x, col_name))

    # 应用 formula_1 到其他列
    formula_1_columns = set(range(len(new_indicators.columns))) - set(formula_2_columns)
    for col_index in formula_1_columns:
        col_name = new_indicators.columns[col_index]
        new_indicators[col_name] = new_indicators[col_name].apply(lambda x: formula_1(x, col_name))

    return all_indicators, new_indicators


# 应用于计算的数据和标准化之后的数据
calculated_data, standardized_data = excel_original_data(concatenated_df)


def calculate_weight(standardized_data):

    def apply_formula(x):
        return x * np.log(x)

    # 将每一列的值取对数
    ln_indicators = standardized_data.applymap(apply_formula)

    # 求每一列的和
    sum_cols = ln_indicators.sum()
    # 求行数
    num_rows = ln_indicators.shape[0]
    # 求熵值
    z = -1 / np.log(num_rows)
    # 求区分度
    discrimination = 1 - sum_cols * z

    # 计算权重
    indicator_weights = discrimination.copy()
    indicator_weights = indicator_weights / indicator_weights.sum()

    return indicator_weights


# 计算模一标准化的权重指标
indicator_weights = calculate_weight(standardized_data)


def calculate_solution(calculated_data, indicator_weights):

    numpy_data = calculated_data.to_numpy()
    normalized_data = np.zeros_like(numpy_data, dtype=float)

    for col in range(numpy_data.shape[1]):
        # 对每一列应用公式
        normalized_data[:, col] = numpy_data[:, col] / np.sqrt(np.sum(np.square(numpy_data[:, col])))

    weights_array = indicator_weights.to_numpy()
    standardized_weight_matrix = normalized_data * weights_array

    positive_solution = np.max(standardized_weight_matrix, axis=0)
    negative_solution = np.min(standardized_weight_matrix, axis=0)

    positive_solution_distance = np.sqrt(np.sum(np.square(standardized_weight_matrix - positive_solution), axis=1))
    negative_solution_distance = np.sqrt(np.sum(np.square(standardized_weight_matrix - negative_solution), axis=1))

    total_sum = positive_solution_distance + negative_solution_distance

    # 防止除以零，将和为零的地方替换为一个小的非零值（例如1e-10）
    total_sum[total_sum == 0] = 1e-10

    # 接近度
    proximity = negative_solution_distance / total_sum

    proximity_sum = np.sum(proximity)

    # 防止除以零，将和为零的地方替换为一个小的非零值（例如1e-10）
    proximity_sum = max(proximity_sum, 1e-10)

    proximity_score = proximity / proximity_sum

    average_weight = proximity_score.mean()
    # 计算最终得分
    final_score = ((proximity_score - average_weight) / (proximity_score.max() - average_weight) * 0.15 + 0.85) * 100

    return final_score

final_score = calculate_solution(calculated_data, indicator_weights)

# 将最终的结果写入json
final_score_df = pd.DataFrame(final_score, columns=['score'])

merged_df = pd.concat([company_name_df, final_score_df], axis=1)
merged_df.columns = ['公司', 'score']

result_json = {"code": 200, "msg": "Success", "data": merged_df.set_index('公司').to_dict()['score']}

with open('model3.json', 'w', encoding='utf-8') as json_file:
    json.dump(result_json, json_file, ensure_ascii=False)

# 打印最终结果
print(result_json)