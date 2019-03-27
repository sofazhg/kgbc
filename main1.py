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

FilePath = 'E:\project'
PatientRecordFile = FilePath + '\DATA.xlsx'
PatientRecordData = xlrd.open_workbook(PatientRecordFile)
data = PatientRecordData.sheets()[0]

DescExam = data.row_values(1)[5]
arrayrow = DescExam.split('\n')
SplitDesc = []


temp2 = arrayrow[2].split('，')
SplitDesc.append(temp2)
seg_list2 = list(jieba.cut(temp2[0], cut_all= False))
seg_array2 = np.array(seg_list2)
print(seg_array2)
DesContour = ['未见']
for i in range(len(seg_array2)):
    for j in range(len(DesContour)):
        if(seg_array2[i] == DesContour[j]):
            print('双乳轮廓异常:'+ DesContour[j])

temp3 = arrayrow[3].split('，')
SplitDesc.append(temp3)
seg_list3 = list(jieba.cut(temp3[0], cut_all= False))
seg_array3 = np.array(seg_list3)
print(seg_array3)
DesGland = ['丰富','退化']
for i in range(len(seg_array3)):
    for j in range(len(DesGland)):
        if(seg_array3[i] == DesGland[j]):
            print('双乳腺体含量：'+ DesGland[j])

temp4 = arrayrow[4].split('，')
SplitDesc.append(temp4)
seg_list4 = list(jieba.cut(temp4[0], cut_all= False))
seg_array4 = np.array(seg_list4)
print(seg_array4)
DesLymph = ['未见','小','细小','多发','多枚','数枚','饱满','较大']               
for i in range(len(seg_array4)):
    for j in range(len(DesLymph)):
        if(seg_array4[i] == DesLymph[j]):
            print('双侧腋下淋巴结影：'+DesLymph[j])

print(SplitDesc)

