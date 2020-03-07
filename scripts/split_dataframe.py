#!/usr/bin/python3
# encoding: utf-8
"""
@author: Shaohua Zhang
@contact: sofazhg@outlook.com
@file: splitdf.py
@time: 2019-03-11 14:20
"""
import pandas as pd

FilePath = 'E:\project\DATA.xlsx'
data = pd.read_excel(FilePath)
rows = data.shape[0]  # 获取行数，shape[1]获取列数
exam_list = []

for i in range(rows):
    temp = data["ITEM_NAME"][i]
    if temp not in exam_list:
        exam_list.append(temp)  # 将不同检查项目的名称存到一个列表里面
print(exam_list)

for exam in exam_list:
    new_df = pd.DataFrame()  # 为每个检查项目创建一个新的工作表
    for i in range(0, rows):
        if data["ITEM_NAME"][i] == exam:
            new_df = pd.concat([new_df, data.iloc[[i], :]], axis=0, ignore_index=True)

    new_df.to_excel(str(exam) + ".xls", sheet_name=exam, index=False)  # 将每个检查项目存成单独的excel表格
