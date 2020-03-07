#!/usr/bin/python3
# encoding: utf-8
"""
@author: Erin Cai
@contact: charlottecaiir@gmail.com
@file: main.py
@time: 19-3-7 下午7:40
"""

import jieba  # Chinese Word Extraction Data https://github.com/fxsjy/jieba/
# Another Tool:http://thulac.thunlp.org/
import numpy as np
from os.path import abspath, join, dirname
import re
import pandas as pd

project_dir = dirname(dirname(abspath(__file__)))
data_dir=join(project_dir,'data')
mammograph_path=join(data_dir,'乳腺钼靶DR摄片(双侧).xls')
mammograph_df = pd.read_excel(mammograph_path)
num_rows = mammograph_df.shape[0]  # 行数：shape[0] 列数：shape[1]
print("钼靶报告份数：%d"%num_rows)  # 总共54行
mammograph_reports=[mammograph_df['IMAGING_FINDING'][i] for i in range(num_rows)]

dict_dir=join(project_dir,'dict')
mammograph_dict_path=join(dict_dir,'dict_mammograph.txt')
jieba.load_userdict(mammograph_dict_path)  # 载入钼靶关键词词典


# 根据分词结果调整分词频率
jieba.suggest_freq(('以','外'), True)
jieba.suggest_freq('为著', True)
jieba.suggest_freq('散在粗大钙化灶', True)
jieba.suggest_freq('外上象限', True)
jieba.suggest_freq('双乳轮廓', True)
jieba.suggest_freq('双乳腺体', True)
jieba.suggest_freq('所示腺体', True)
jieba.suggest_freq('双侧腋下', True)
jieba.suggest_freq('未见明显异常', True)
jieba.suggest_freq('皮肤及皮下脂肪', True)
jieba.suggest_freq('未见凹陷', True)


# 若字符串在任一列表元素中，就对该列表进行检索
def string_in_list(string, list):
    is_in=False
    for element in list:
        if string in element:
            is_in=True
    return is_in


# 若字符串在任一列表元素中，返回该元素
def string_in_element(string, list):
    matched_elements=[]
    for element in list:
        if string in element:
            matched_elements.append(element)
    return matched_elements


for report_text in mammograph_reports:
    # report = mammograph_reports[0]  # 第一篇钼靶阅片报告
    report_text = re.sub(r"\s{2,}", "，", report_text)
    report_text = re.sub(r"\n", " ", report_text)
    report_text = re.sub(r"。", "，", report_text)
    report_sents = report_text.split('，')[:-2]  # 按逗号切分句子
    print('=' * 50)
    # print(report_sents)
    for sent in report_sents:
        token_list = jieba.lcut(sent, cut_all=False)
        print(token_list)
        """
        if string_in_list('双乳轮廓',token_list):
            matched_token=string_in_element('常',token_list)
            print('双乳轮廓：')
            print(matched_token)  # 如果只匹配到一个token, 那就打印第一个token
        if string_in_element('乳头', token_list):
            matched_token = string_in_element('凹陷', token_list)
            print('乳头:')
            print(matched_token)
        if string_in_element('双乳腺体', token_list):
            matched_token = string_in_element('丰富', token_list)
            matched_token+=string_in_element('退化', token_list)
            print('双乳腺体:')
            print(matched_token)
        if string_in_element('所示腺体', token_list):
            matched_token = string_in_element('状', token_list)
            matched_token += string_in_element('密度影', token_list)
            print('腺体形状:')
            print(matched_token)
        if string_in_element('为著', token_list):
            matched_token = string_in_element('象限', token_list)
            print('腺体方位:')
            print(matched_token)
        if string_in_element('钙化', token_list):
            matched_token = string_in_element('钙化', token_list)
            print('钙化形状:')
            print(matched_token)
        if string_in_element('皮肤及皮下脂肪', token_list):
            matched_token = string_in_element('常', token_list)
            print('皮肤及皮下脂肪:')
            print(matched_token)


        DesXTHL = ['丰富','退化']
        for i in range(len(token_array)):
            for j in range(len(DesXTHL)):
                if token_array[i] == DesXTHL[j]:
                    print('腺体含量：'+ DesXTHL[j])
"""