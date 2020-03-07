# coding: utf-8

import sys
import jieba  # Chinese Word Extraction Data https://github.com/fxsjy/jieba/
# Another Tool:http://thulac.thunlp.org/
import numpy as np  # Array manipulation tools
import xlrd  # Open Excel Table
import re
from os.path import abspath, join, dirname
import pandas as pd

project_dir=dirname(dirname(abspath(__file__)))
data_dir=join(project_dir,'data')
mammograph_path=join(data_dir,'乳腺钼靶DR摄片(双侧).xls')
mammograph_df = pd.read_excel(mammograph_path)
num_rows = mammograph_df.shape[0]  # 行数：shape[0] 列数：shape[1]
print("钼靶报告份数：%d"%num_rows)  # 总共54行
mammograph_reports=[mammograph_df['IMAGING_FINDING'][i] for i in range(num_rows)]

desc_text = mammograph_reports[0]  # 第一篇钼靶阅片报告
desc_paras = desc_text.split('\n')  # 按换行符切分段落
desc_sents = [para.split('，') for para in desc_paras]  # 按逗号分割句子


def my_split(instr, sep=u"双乳轮廓|皮肤及皮下脂肪|乳头|双乳腺体|所示腺体|以|双乳见|双侧腋下|淋巴结门"):  # 分隔符可为多样的正则表达式
    wdict = {}
    wlist = re.split(sep, instr)
    sepword = re.findall(sep, instr)
    sepword.insert(0, " ")  # 开头（或末尾）插入一个空字符串，以保持长度和切割成分相同
    for x, y in zip(sepword, wlist):
        wdict[x] = y
    return wdict


if __name__ == "__main__":
    instr = re.sub('[，。\n]', '', desc_text)
    res = my_split(instr)
    print(res)

