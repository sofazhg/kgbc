# coding: utf-8

import sys

import re


def my_split(str, sep=u"双乳轮廓|双乳腺体|双侧腋窝"):  # 分隔符可为多样的正则表达式
    wdict={}
    wlist = re.split(sep, str)
    sepword = re.findall(sep, str)
    sepword.insert(0, " ")  # 开头（或末尾）插入一个空字符串，以保持长度和切割成分相同
    for x, y in zip(sepword, wlist):
        wdict[x]= y
    return wdict


if __name__ == "__main__":
    inputstr = "双乳轮廓未见明显异常，双乳腺体丰富。\n双侧腋窝未见明显淋巴结。\n"
    instr = re.sub('[，。；\n]','',inputstr)
    res = my_split(instr)
    print(res)