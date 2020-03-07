#!/usr/bin/python3
# encoding: utf-8
"""
@author: ZHANG Shaohua
@contact: sofazhg@outlook.com
@file: main.py
@time: 19-3-7 下午7:40
"""

import sys
import jieba  # Chinese Word Extraction Data https://github.com/fxsjy/jieba/
# Another Tool:http://thulac.thunlp.org/
import numpy as np  # Array manipulation tools
import xlrd  # Open Excel Table
import re
from os.path import abspath, join, dirname
import pandas as pd

project_dir = dirname(dirname(abspath(__file__)))
data_dir = join(project_dir, 'data')
mammograph_path = join(data_dir, '乳腺钼靶DR摄片(双侧).xls')
mammograph_df = pd.read_excel(mammograph_path)
num_rows = mammograph_df.shape[0]  # 行数：shape[0] 列数：shape[1]
print("钼靶报告份数：%d" % num_rows)  # 总共54行
mammograph_reports = [mammograph_df['IMAGING_FINDING'][i] for i in range(num_rows)]

desc_text = mammograph_reports[0]  # 第一篇钼靶阅片报告
desc_paras = desc_text.split('\n')  # 按换行符切分段落
desc_sents = []
for para in desc_paras:
    tmp = re.sub('。', '，', para)
    desc_sents.append(tmp.split('，'))  # 按逗号分割句子

for sent in desc_sents:
    for string in sent:
        # print(string)
        string = re.sub(' ', '', string)
        string = re.sub('。', '', string)
        match1 = re.match(r'双乳轮廓(.*?)$', string, re.M)
        if match1:
            # print("matchObj.group():", matchObj.group())
            print("双乳轮廓:", match1.group(1))
        match2 = re.match(r'皮肤及皮下脂肪(.*?)$', string, re.M)
        if match2:
            print("皮肤及皮下脂肪:", match2.group(1))
        match3 = re.match(r'乳头(.*?)$', string, re.M)
        if match3:
            print("乳头:", match3.group(1))
        match4 = re.match(r'双乳腺体(.*?)$', string, re.M)
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
        match8 = re.match(r'双侧腋下见(.*?)淋巴结影', string, re.M)
        if match8:
            print("双侧腋下淋巴结:", match8.group(1))
        match9 = re.match(r'淋巴结门(.*?)$', string, re.M)
        if match9:
            print("淋巴结门:", match9.group(1))
        match10 = re.match(r'^20(.*?)日', string, re.M)
        if match10:
            print("报告日期：20%s日" % match10.group(1))
