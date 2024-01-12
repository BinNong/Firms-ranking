# -*- coding: utf-8 -*-
# @Time    : 2024/1/12 20:26
# @Author  : nongbin
# @FileName: credit_eval.py
# @Software: PyCharm
# @Affiliation: tfswufe.edu.cn

import pandas as pd
import numpy as np


def evaluate(data, group, total):
    def start_dataframe(data, group, columns):

        company_name_list = []

        for i in range(int(columns)):
            company_name = data[i]['company_name']
            company_name_list.append(company_name)

        json_data_keys = list(data[0].keys())
        company_name_df = pd.DataFrame(company_name_list, columns=['company_name'])

        # 获取全量数据并使用Dataframe存储在concatenated_df中
        list_of_dfs = []
        key_names = []

        for key in json_data_keys[1:]:
            key_names.append(key)
            columns_list_1 = []
            for j in range(int(columns)):
                list1 = data[j][key]
                columns_list_1.append(list1)
            list_of_dfs.append(columns_list_1)

        concatenated_df = pd.DataFrame(list_of_dfs).transpose()
        concatenated_df = concatenated_df.apply(
            lambda col: col.astype(float, errors='ignore') if col.dtype == 'object' else col, axis=0)

        return company_name_df, concatenated_df

    # 公司名称和全量数据
    company_name_df, concatenated_df = start_dataframe(data, group, total)

    def excel_original_data(concatenated_df):
        # 偿债能力对应的指标
        debt_payment = pd.DataFrame()
        debt_payment['流动比率'] = concatenated_df.iloc[:, 6] / concatenated_df.iloc[:, 11]  # 流动比率
        debt_payment['速动比率'] = (concatenated_df.iloc[:, 6] - concatenated_df.iloc[:, 4] - concatenated_df.iloc[:,
                                                                                              2]) / concatenated_df.iloc[
                                                                                                    :, 11]  # 速动比率
        debt_payment['资产负债率'] = concatenated_df.iloc[:, 12] / concatenated_df.iloc[:, 10]  # 资产负债率
        debt_payment['经营现金流量负债比'] = concatenated_df.iloc[:, 26] / concatenated_df.iloc[:, 12]  # 经营现金流量负债比
        debt_payment['产权比率'] = concatenated_df.iloc[:, 12] / concatenated_df.iloc[:, 14]  # 产权比率

        # 盈利能力对应的指标
        profit_ability = pd.DataFrame()
        profit_ability['总资产报酬率'] = concatenated_df.iloc[:, 25] / (
                (concatenated_df.iloc[:, 9] + concatenated_df.iloc[:, 10]) / 2)  # 总资产报酬率
        profit_ability['净资产收益率'] = concatenated_df.iloc[:, 25] / (
                (concatenated_df.iloc[:, 13] + concatenated_df.iloc[:, 14]) / 2)  # 净资产收益率
        profit_ability['盈余现金保障倍数'] = concatenated_df.iloc[:, 26] / concatenated_df.iloc[:, 25]  # 盈余现金保障倍数
        profit_ability['成本费用利用率'] = concatenated_df.iloc[:, 23] / (
                concatenated_df.iloc[:, 17] + concatenated_df.iloc[:, 18] + concatenated_df.iloc[:,
                                                                            19] + concatenated_df.iloc[:,
                                                                                  20])  # 成本费用利用率

        # 经营能力对应的指标
        operation_ability = pd.DataFrame()
        operation_ability['应收账款周转率'] = (concatenated_df.iloc[:, 0] + concatenated_df.iloc[:,
                                                                            16] - concatenated_df.iloc[:, 1]) / (
                                                      (concatenated_df.iloc[:, 0] + concatenated_df.iloc[:, 1]) / 2)
        operation_ability['存货周转率'] = concatenated_df.iloc[:, 17] / (
                (concatenated_df.iloc[:, 3] + concatenated_df.iloc[:, 4]) / 2)
        operation_ability['总资产周转率'] = concatenated_df.iloc[:, 16] / concatenated_df.iloc[:, 10]
        operation_ability['固定资产周转率'] = concatenated_df.iloc[:, 16] / (
                (concatenated_df.iloc[:, 7] + concatenated_df.iloc[:, 8]) / 2)
        operation_ability['流动资产周转率'] = concatenated_df.iloc[:, 16] / (
                (concatenated_df.iloc[:, 5] + concatenated_df.iloc[:, 6]) / 2)

        # 发展能力对应的指标
        development_ability = pd.DataFrame()
        development_ability['总资产增长率'] = (concatenated_df.iloc[:, 10] - concatenated_df.iloc[:,
                                                                             9]) / concatenated_df.iloc[:, 9]
        development_ability['净利润增长率'] = (concatenated_df.iloc[:, 25] - concatenated_df.iloc[:,
                                                                             24]) / concatenated_df.iloc[:, 24]
        development_ability['营业收入增长率'] = (concatenated_df.iloc[:, 16] - concatenated_df.iloc[:,
                                                                               15]) / concatenated_df.iloc[:, 15]
        development_ability['营业利润增长率'] = (concatenated_df.iloc[:, 22] - concatenated_df.iloc[:,
                                                                               21]) / concatenated_df.iloc[:, 21]

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
                                    enterprise_scale, innovation_ability, operation_condition, enterprise_credit],
                                   axis=1)

        new_indicators = all_indicators.copy()

        # 定义两种不同的公式
        def formula_1(x, col):
            return 0.1 + 0.9 * (x - all_indicators[col].min()) / (all_indicators[col].max() - all_indicators[col].min())

        def formula_2(x, col):
            return 0.1 + 0.9 * (all_indicators[col].max() - x) / (all_indicators[col].max() - all_indicators[col].min())

        # 指定需要应用 formula_2 的列索引
        formula_2_columns = [2, 4, 29, 30]

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

        ranges = [(1, 5), (6, 9), (10, 14), (15, 18), (19, 21), (22, 25), (26, 29), (30, 31)]

        sums = []
        for start, end in ranges:
            subset = discrimination.iloc[start - 1:end]  # 索引从0开始，因此需要减去1
            sum_value = subset.sum()
            sums.append(sum_value)

        # 计算权重
        indicator_weights = discrimination.copy()

        for i, (start, end) in enumerate([(1, 5), (6, 9), (10, 14), (15, 18), (19, 21), (22, 25), (26, 29), (30, 31)]):
            indicator_weights.iloc[start - 1:end] /= sums[i]

        return indicator_weights

    # 标准化后的数据计算权重指标
    indicator_weights = calculate_weight(standardized_data)

    def enterprise_capability_index(standardized_data, indicator_weights):
        # 偿债能力
        x1 = standardized_data.iloc[:, :5]
        y1 = indicator_weights.iloc[:5]
        z1 = pd.DataFrame(np.dot(x1, y1), columns=['pay_ability'])
        # 盈利能力
        x2 = standardized_data.iloc[:, 5:9]
        y2 = indicator_weights.iloc[5:9]
        z2 = pd.DataFrame(np.dot(x2, y2), columns=['income_ability'])
        # 经营能力
        x3 = standardized_data.iloc[:, 9:14]
        y3 = indicator_weights.iloc[9:14]
        z3 = pd.DataFrame(np.dot(x3, y3), columns=['operating_ability'])
        # 发展能力
        x4 = standardized_data.iloc[:, 14:18]
        y4 = indicator_weights.iloc[14:18]
        z4 = pd.DataFrame(np.dot(x4, y4), columns=['development_ability'])
        # 企业规模
        x5 = standardized_data.iloc[:, 18:21]
        y5 = indicator_weights.iloc[18:21]
        z5 = pd.DataFrame(np.dot(x5, y5), columns=['scale'])
        # 创新能力
        x6 = standardized_data.iloc[:, 21:25]
        y6 = indicator_weights.iloc[21:25]
        z6 = pd.DataFrame(np.dot(x6, y6), columns=['creative_ability'])
        # 经营状况
        x7 = standardized_data.iloc[:, 25:29]
        y7 = indicator_weights.iloc[25:29]
        z7 = pd.DataFrame(np.dot(x7, y7), columns=['operating_situation'])
        # 企业信用
        x8 = standardized_data.iloc[:, 29:31]
        y8 = indicator_weights.iloc[29:31]
        z8 = pd.DataFrame(np.dot(x8, y8), columns=['credit'])
        # 企业八大能力指数
        enterprise_capability = pd.concat([z1, z2, z3, z4, z5, z6, z7, z8], axis=1)

        return enterprise_capability

    # 输出企业八大能力指数
    eight_capability = enterprise_capability_index(standardized_data, indicator_weights)

    # print(eight_capability)

    def final_score(eight_capability):
        final_weight1 = pd.Series([0.456609363, 0.221202409, 0.201971639, 0.120216589])
        final_weight2 = pd.Series([0.25, 0.25, 0.25, 0.25])

        financial_features = eight_capability.iloc[:, :4]
        non_financial_features = eight_capability.iloc[:, 4:]

        financial_index = pd.DataFrame(np.dot(financial_features, final_weight1), columns=['score'])
        non_financial_index = pd.DataFrame(np.dot(non_financial_features, final_weight2), columns=['score'])
        weight_score = (financial_index * (2 / 3)) + (non_financial_index * (1 / 3))

        # 计算平均值
        average_weight = weight_score['score'].mean()
        # 计算最终得分
        final_score = ((weight_score['score'] - average_weight) / (
                weight_score['score'].max() - average_weight) * 0.15 + 0.85) * 100

        return final_score

    # 输出最终得分
    final_score = final_score(eight_capability)

    result_df = pd.concat([company_name_df, final_score, eight_capability], axis=1)

    # 生成最终的 JSON 格式
    result_json = {
        "code": 200,
        "msg": "Success",
        "data": []
    }

    for _, row in result_df.iterrows():
        company_data = {
            row['company_name']: {
                'score': str(row['score']),
                'pay_ability': str(row['pay_ability']),
                'income_ability': str(row['income_ability']),
                'operating_ability': str(row['operating_ability']),
                'development_ability': str(row['development_ability']),
                'scale': str(row['scale']),
                'creative_ability': str(row['creative_ability']),
                'operating_situation': str(row['operating_situation']),
                'credit': str(row['credit'])
            }
        }
        result_json['data'].append(company_data)

    return result_json
