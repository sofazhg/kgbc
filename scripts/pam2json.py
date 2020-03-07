#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/5 15:37
# @Author  : ZHANG Shaohua
# @Contact : sofazhg@outlook.com
# @File    : pam2json.py
# @Software: PyCharm

import numpy as np
import os
from os.path import abspath, join, dirname
import random
import pandas as pd
import json

project_dir = dirname(dirname(abspath(__file__)))
data_dir=join(project_dir,'data')
reports_dir=join(data_dir,'reports')
json_dir=join(data_dir,'json_data')

# load
mri_path=join(reports_dir,'MRI200.xlsx')
mri_df = pd.read_excel(mri_path)
num_mri = mri_df.shape[0]  # 行数：shape[0] 列数：shape[1]
print("MRI报告份数：%d"%num_mri)
pam_path=join(reports_dir,'PAM50.xlsx')
pam_df = pd.read_excel(pam_path)
num_pam = pam_df.shape[0]  # 行数：shape[0] 列数：shape[1]
print("PAM50报告份数：%d"%num_pam)

ids1,ids2=[],[]
mri_examples,pam_examples={},{}
for i in range(num_mri):
    id=mri_df['住院号'][i]
    text=mri_df['MRI所见'][i]
    mri_examples[id]=text
    ids1.append(id)
for j in range(num_pam):
    id=pam_df['ID'][j]
    label=pam_df['PAM50'][j]
    pam_examples[id]=label
    ids2.append(id)
ids =list(set(ids1)&set(ids2))  # 交集，除去[214646, 227803]
# print(ids1)
# print(ids2)
# print(ids)
# print(pam_examples)
# print(mri_examples)
# quit()

# mapping
mri_pam_examples=[]
labels=[]
for id in ids:
    label=pam_examples[id]
    labels.append(label)
    text=mri_examples[id]
    mri_pam_examples.append({"label": label, "text": text})

print("LumA型样本数量：",labels.count('LumA'))
print("LumB型样本数量：",labels.count('LumB'))
print("Her2型样本数量：",labels.count('Her2'))
print("Basal型样本数量：",labels.count('Basal'))
print("Normal型样本数量：",labels.count('Normal'))

# shuffle
random.seed(2019)
random.shuffle(mri_pam_examples)

# save
mri_pam_path=join(json_dir,'pam_subtype_examples.json')
with open(mri_pam_path,'w') as f:
    json.dump(mri_pam_examples, f, indent=2, ensure_ascii=False)
