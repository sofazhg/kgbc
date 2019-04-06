#!/usr/bin/python3
# encoding: utf-8
"""
@author: ZHANG Shaohua
@contact: sofazhg@outlook.com
@file: main.py
@time: 19-3-7 下午7:40
"""

import jieba  # Chinese Word Extraction Data https://github.com/fxsjy/jieba/
# Another Tool:http://thulac.thunlp.org/

import numpy as np # Array manipulation tools
import xlrd # Open Excel Table
import re

#FilePath = 'E:\project'
#PatientRecordFile = FilePath + '\DATA.xlsx'
PatientRecordData = xlrd.open_workbook('.\data\乳腺钼靶DR摄片(双侧).xls')
data = PatientRecordData.sheets()[0]

DescExam = data.row_values(1)[5]
arrayrow = DescExam.split('\n')
#print(arrayrow)
SplitDesc = []
for row in arrayrow:
    SplitDesc.append(row.split('，'))
#print(SplitDesc)

for line in SplitDesc:
    for string in line:
        #print(type(string))
        #print(string)
        #line = line + '$'
        match1 = re.match(r' 双乳轮廓(.*?)$', string, re.M)
        if match1:
            #print("matchObj.group():", matchObj.group())
            print("双乳轮廓:", match1.group(1))
        match2 = re.match(r'皮肤及皮下脂肪(.*?)$', string, re.M)
        if match2:
            print("皮肤及皮下脂肪:", match2.group(1))
        match3 = re.match(r'乳头(.*?)$', string, re.M)
        if match3:
            print("乳头:", match3.group(1))
        match4 = re.match(r' 双乳腺体(.*?)$', string, re.M)
        if match4:
            print("双乳腺体:", match4.group(1))
        match5 = re.match(r'所示腺体(.*?)$', string, re.M)
        if match5:
            print("腺体形态:", match5.group(1))
        match6 = re.match(r'以(.*?)为著$', string, re.M)
        if match6:
            print("方位:", match6.group(1))
        match7 = re.match(r'双乳见(.*?)钙化', string, re.M)
        if match7:
            print("钙化:", match7.group(1))
        match8 = re.match(r' 双侧腋下见(.*?)淋巴结影', string, re.M)
        if match8:
            print("双侧腋下淋巴结:", match8.group(1))
        match9 = re.match(r'淋巴结门(.*?)$', string, re.M)
        if match9:
            print("淋巴结门:", match9.group(1))

#print(SplitDesc)

