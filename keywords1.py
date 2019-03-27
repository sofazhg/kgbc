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
import os

"""
FilePath_ImgRpt = 'E:\project\DATA.xlsx'
ImgRpt = pd.read_excel(FilePath_ImgRpt)
rows_Img = ImgRpt.shape[0]

idf_dic = open('E:\project\idf_dic.txt', mode = 'w', encoding = 'utf-8')
idf_dic_new = open('E:\project\idf_dic_new.txt', mode = 'w', encoding = 'utf-8')
for i in range(rows_Img):
    idf_dic.write(ImgRpt['IMAGING_FINDING'][i]) #write all the data into the idf_dictionary
idf_dic.close()
idf_dic = open('E:\project\idf_dic.txt',mode = 'r', encoding = 'utf-8')

for line in idf_dic.readlines():
    data = line.strip("\n\r\t") #read in by lines,delete empty lines like \n,\t,\r
    if len(data)!=0:
        idf_dic_new.write(data)
idf_dic.close()
idf_dic_new.close()
jieba.analyse.set_idf_path('E:\project\idf_dic_new.txt')
"""
#尝试将整个影像报告文档作为IDF词库，但是IDF词库格式要求每行一个词条+一个频率，尝试失败。

FilePath_RptMG = 'E:\project\乳腺钼靶DR摄片(双侧).xls'
RptMG = pd.read_excel(FilePath_RptMG)
rows = RptMG.shape[0]

ExamMG = []
for i in range(rows):
    ExamMG.append(RptMG['IMAGING_FINDING'][i])

print("钼靶报告份数：" + str(len(ExamMG))) #54 rows in total
temp = ''.join(ExamMG) #convert list to string
tfidf = jieba.analyse.extract_tags
keywords = tfidf(temp,topK = 100, withWeight = True)

print("钼靶关键词提取：\n")
for keyword in keywords:
    print(keyword)
