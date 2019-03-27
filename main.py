#!/usr/bin/python3
# encoding: utf-8
"""
@author: Erin Cai
@contact: charlottecaiir@gmail.com
@file: main.py
@time: 19-3-7 下午7:40
"""

import jieba # Chinese Word Extraction Data https://github.com/fxsjy/jieba/
# Another Tool:http://thulac.thunlp.org/
import numpy as np # Array manipulation tools
import xlrd # Open Excel Table

FilePath = '/home/yirancai/Project/NLP/01.Data/'
PatientRecordFile = FilePath + 'DATA.xls'
PatientRecordData = xlrd.open_workbook(PatientRecordFile)
data = PatientRecordData.sheets()[0]

DescExam = data.row_values(1)[5]
arrayrow = DescExam.split('\n')
SplitDesc = []
for i in range(len(arrayrow)):
    temp = arrayrow[i].split('，')
    SplitDesc.append(temp)
    seg_list = list(jieba.cut(temp[0], cut_all= True))
    seg_array = np.array(seg_list)
    #print(seg_array)
    DesXTHL = ['丰富','退化']

    for i in range(len(seg_array)):
        for j in range(len(DesXTHL)):
            if(seg_array[i] == DesXTHL[j]):
                print('腺体含量：'+ DesXTHL[j])


#print(SplitDesc)

