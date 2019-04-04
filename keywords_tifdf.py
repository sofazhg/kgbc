#!/usr/bin/python3
# encoding: utf-8
"""
@author: Shaohua Zhang
@contact: sofazhg@outlook.com
@file: splitdf.py
@time: 2019-03-13 20:20
"""

import jieba  # Chinese Word Extraction Data https://github.com/fxsjy/jieba/
# Another Tool:http://thulac.thunlp.org/
from jieba import analyse
import numpy as np  # Array manipulation tools
import xlrd  # Open Excel Table

FilePath = 'E:\project'
PatientRecordFile = FilePath + '\DATA.xlsx'
PatientRecordData = xlrd.open_workbook(PatientRecordFile)
data = PatientRecordData.sheets()[0]

DescExam = data.row_values(1)[5]
# arrayrow = DescExam.split('\n')

tfidf = analyse.extract_tags
keywords = tfidf(DescExam,topK = 30, withWeight = True)

print("关键词提取：\n")
for keyword in keywords:
    print(keyword)
