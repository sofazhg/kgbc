#! /usr/bin/python3
# encoding: utf-8
"""
@author: Shaohua Zhang
@contact: sofazhg@outlook.com
@file: keywords1.py
@time: 2019-03-13 22:20
"""

import jieba
import jieba.analyse
import numpy as np
import pandas as pd
import sys
import re
from os.path import dirname,abspath,join

project_dir=dirname(dirname(abspath(__file__)))
data_dir=join(project_dir,'data')
mammograph_path=join(data_dir,'乳腺钼靶DR摄片(双侧).xls')
mammograph_df = pd.read_excel(mammograph_path)
num_rows = mammograph_df.shape[0]  # 行数：shape[0] 列数：shape[1]
print("钼靶报告份数：%d"%num_rows)  # 总共54行
mammograph_reports=[mammograph_df['IMAGING_FINDING'][i] for i in range(num_rows)]

dict_dir=join(project_dir,'dict')
mammograph_dict_path=join(dict_dir,'dict_mammograph.txt')
# jieba.load_userdict(mammograph_dict_path)  # 载入钼靶关键词词典

temp = ''.join(mammograph_reports)  # 把列表拼接为字符串
temp = re.sub(r'[A-Za-z0-9]','',temp)  # 过滤字符串中的英文和数字
tfidf = jieba.analyse.extract_tags
keywords = tfidf(temp, topK=100, withWeight=True)

print("钼靶关键词提取：\n")
for keyword in keywords:
    print(keyword)
