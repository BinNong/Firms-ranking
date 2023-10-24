import pandas as pd
import numpy as np
import math


# 财务指标数据计算
def calculate_list(example_input_data):
    financial_indicator_calculation = [
        example_input_data[0] / example_input_data[2],
        (example_input_data[0] - example_input_data[20] - example_input_data[3]) / example_input_data[2],
        example_input_data[2] / example_input_data[4],
        example_input_data[6] / example_input_data[2],
        example_input_data[2] / example_input_data[13],
        example_input_data[12] / example_input_data[9],
        example_input_data[24] / (example_input_data[4] + example_input_data[5]) / 2,
        example_input_data[24] / (example_input_data[14] + example_input_data[13]) / 2,
        example_input_data[6] / example_input_data[24],
        example_input_data[7] / (
                    example_input_data[15] + example_input_data[16] + example_input_data[17] + example_input_data[8]),
        (example_input_data[19] + example_input_data[9] - example_input_data[18]) / (
                    example_input_data[19] + example_input_data[18]) / 2,
        example_input_data[15] / example_input_data[20],
        example_input_data[9] / example_input_data[4],
        example_input_data[9] / (example_input_data[22] + example_input_data[23]) / 2,
        example_input_data[9] / (example_input_data[0] + example_input_data[1]) / 2,
        (example_input_data[4] - example_input_data[5]) / example_input_data[5],
        (example_input_data[24] - example_input_data[25]) / example_input_data[25],
        (example_input_data[9] - example_input_data[10]) / example_input_data[10],
        (example_input_data[12] - example_input_data[11]) / example_input_data[11]
    ]
    return financial_indicator_calculation


# 读取Excel中的全量原始数据 Excel中是92家公司，每家公司42个指标，其中，29个原始财务报表数据，13个非财务指标

df = pd.read_excel('原始数据.xlsx', sheet_name='Sheet1', usecols='B:AQ')
df = df.fillna(0)

# 对财务指标进行处理，结果是19个财务指标,将处理的结果拼接，最后是每家公司32个指标

financial_data = df.iloc[:, :29]
financial_data = financial_data.values.tolist()

new_list = []

for i in financial_data:

    financial_result = calculate_list(i)
    new_list.append(financial_result)

df_financial = pd.DataFrame(new_list)
df_un_financial = df.iloc[:, -13:]
new_columns = pd.RangeIndex(start=19, stop=32)
df_un_financial.columns = new_columns


concatenated_df = pd.concat([df_financial, df_un_financial], axis=1)


# 标准化数据函数，输入是19个财务指标和13个非财务指标
def standardize(data):
    standardized_data = pd.DataFrame()
    for column in data.columns:
        min_val = data[column].min()
        max_val = data[column].max()
        standardized_col = 0.1 + (data[column] - min_val) / (max_val - min_val) * 0.9
        standardized_data[column] = standardized_col
    return standardized_data
# 示例用法

example_standardized_data = standardize(concatenated_df)
# print(example_standardized_data.shape)


# 求区分度


def apply_formula_and_sum(df):
    def apply_formula(x):
        return x * math.log(x) if isinstance(x, (int, float)) and x != 0 else x

    df_formula = df.applymap(apply_formula)
    column_sum = df_formula.sum()
    c = column_sum * -1
    n = df.shape[0]
    ln_n = math.log(n)
    final_result = 1 - c/ln_n

    return final_result




final_result = apply_formula_and_sum(example_standardized_data)
# print(final_result.shape)


# 求权重
def apply_formula_and_sum(result_rat):

    sum_values1 = np.sum(result_rat[:5])
    sum_values2 = np.sum(result_rat[6:10])
    sum_values3 = np.sum(result_rat[10:15])
    sum_values4 = np.sum(result_rat[15:19])
    f_sum_values1 = np.sum(result_rat[19:22])
    f_sum_values2 = np.sum(result_rat[22:26])
    f_sum_values3 = np.sum(result_rat[26:30])
    f_sum_values4 = np.sum(result_rat[30:32])
    list_name = [
        '流动比率', '速动比率', '资产负债率', '经营现金流量负债比', '产权比率',                    # 对应二级指标’偿债能力‘
        '总资产报酬率', '净资产收益率', '盈余现金保障倍数', '成本费用利用率',                       # 对应二级指标’盈利能力‘
        '应收账款周转率', '存货周转率', '总资产周转率', '固定资产周转率', '流动资产周转率',           # 对应二级指标’经营能力‘
        '总资产增长率', '净利润增长率', '营业收入增长率', '营业利润增长率',                         # 对应二级指标’发展能力‘
        '参保人数', '成立年限', '注册资本',                                                    # 对应二级指标’企业规模‘
        '专利信息', '商标信息', '著作权', '软件著作权',                                         # 对应二级指标’创新能力‘
        '供应商', '客户数量', '控股企业个数', '对外投资次数',                                    # 对应二级指标’经营状况‘
        '行政处罚次数', '被执行金额',                                                         # 对应二级指标’企业信用‘
    ]
    list_count = [
        result_rat[0]/sum_values1, result_rat[1]/sum_values1, result_rat[2]/sum_values1, result_rat[3]/sum_values1, result_rat[4]/sum_values1,
        result_rat[6]/sum_values2, result_rat[7]/sum_values2, result_rat[8]/sum_values2, result_rat[9]/sum_values2,
        result_rat[10]/sum_values3, result_rat[11]/sum_values3, result_rat[12]/sum_values3, result_rat[13]/sum_values3, result_rat[14]/sum_values3,
        result_rat[15]/sum_values4, result_rat[16]/sum_values4, result_rat[17]/sum_values4, result_rat[18]/sum_values4,
        result_rat[19]/f_sum_values1, result_rat[20]/f_sum_values1, result_rat[21]/f_sum_values1,
        result_rat[22]/f_sum_values2, result_rat[23]/f_sum_values2, result_rat[24]/f_sum_values2, result_rat[25]/f_sum_values2,
        result_rat[26]/f_sum_values3, result_rat[27]/f_sum_values3, result_rat[28]/f_sum_values3, result_rat[29]/f_sum_values3,
        result_rat[30]/f_sum_values4, result_rat[31]/f_sum_values4,
    ]
    list_count1 = [x * (2/3) * 0.456609362859363 for x in list_count[:4]]
    list_count2 = [x * (2/3) * 0.221202408702409 for x in list_count[5:9]]
    list_count3 = [x * (2/3) * 0.201971639471639 for x in list_count[9:13]]
    list_count4 = [x * (2/3) * 0.120216588966589 for x in list_count[14:18]]

    list_count5 = [x * (1/3) * 0.25 for x in list_count[-13:]]

    list_count_final = list_count1 + list_count2 + list_count3 + list_count4 + list_count5

    return list_count_final

list_count_final = apply_formula_and_sum(final_result)
# print(list_count_final)

# 求经营得分,表格标准化的数据多了一列，删除第六列

example_standardized_data = example_standardized_data.drop(example_standardized_data.columns[5], axis=1)

final_score = []

for row in example_standardized_data.values:
    result = 100 * sum([row[i] * list_count_final[i] for i in range(len(list_count_final))])
    # print(result)
    final_score.append(result)


company_name = pd.read_excel('原始数据.xlsx', sheet_name='Sheet1', usecols='A')
company_name['分数'] = final_score

company_name.to_excel('企业评分.xlsx', index=False)