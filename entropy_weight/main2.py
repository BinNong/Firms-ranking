import json
import pandas as pd

file_name = 'model2_input.json'


def dataframe_to_year(year, file_name):

    with open(file_name, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    columns = json_data['total']
    company_name_list = []

    for i in range(int(columns)):
        company_name = list(json_data["data"][year].keys())[i]
        company_name_list.append(company_name)

    dfs = []

    for company_name, financial_info in json_data["data"][year].items():
        df = pd.DataFrame([financial_info])
        df.insert(0, "Company Name", company_name)
        dfs.append(df)

    result_df = pd.concat(dfs, ignore_index=True)

    return result_df, company_name_list


def result_to_excel(years):

    result_df_2020 = dataframe_to_year(years, file_name)[0]
    df_2020_company = dataframe_to_year(years, file_name)[1]

    result_df_2020 = result_df_2020.drop(['Company Name'], axis=1)

    mixed_type_columns = result_df_2020.applymap(type).eq(str).any()
    for column in result_df_2020.columns:
        if mixed_type_columns[column]:
            result_df_2020[column] = pd.to_numeric(result_df_2020[column], errors='coerce')


    def normalize_column(column):
        min_value = column.min()
        max_value = column.max()
        return 0.1 + 0.9 * (column - min_value) / (max_value - min_value)


    result_df_2020_normalized = result_df_2020.apply(normalize_column)

    result_df_2020_company = pd.Series(df_2020_company, name='Company Name')
    result_df_2020_final = pd.concat([result_df_2020_company, result_df_2020_normalized], axis=1)

    return result_df_2020_final


result_to_excel('2020').to_excel('output_2020.xlsx', sheet_name='2020')
result_to_excel('2021').to_excel('output_2021.xlsx', sheet_name='2021')
result_to_excel('2022').to_excel('output_2022.xlsx', sheet_name='2022')

