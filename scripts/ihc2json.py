#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/5 15:37
# @Author  : ZHANG Shaohua
# @Contact : sofazhg@outlook.com
# @File    : xls2json.py
# @Software: PyCharm

from os.path import abspath, join, dirname
import re
import pandas as pd
import random
import json

project_dir = dirname(dirname(abspath(__file__)))
data_dir=join(project_dir,'data')
reports_dir=join(data_dir,'reports')
json_dir=join(data_dir,'json_data')

# load
mri_path=join(reports_dir,'MRI200.xlsx')
mri_df = pd.read_excel(mri_path)
num_rows = mri_df.shape[0]  # 行数：shape[0] 列数：shape[1]
print("MRI报告份数：%d"%num_rows)

# process
mri_examples=[]
labels=[]
for i in range(num_rows):
    # IHC subtype
    label=mri_df['分子分型'][i]

    # # BI-RADS
    # nums=[]
    # s=mri_df['印象与建议'][i]
    # s=re.sub('[,；。\n]', '，', s)
    # for x in s.split('，'):
    #     if 'BI-RADS' in x:
    #         nums+=re.findall('\d',x)
    # label='BI-RADS '+max(nums)

    # # KI-67
    # s=mri_df['KI-67'][i]
    # nums=re.findall('\d+',s)
    # if nums and int(nums[-1])>20:
    #     label='KI-67 h'
    # else:
    #     label='KI-67 l'

    # # HER-2
    # s=mri_df['HER-2'][i]
    # label='HER2 -'
    # if re.search('\+\+',s) or re.search('2\+',s):
    #   if re.search('扩增',s) and not re.search('无',s):
    #       label='HER2 +'
    # if re.search('\+\+\+',s) or re.search('3\+',s):
    #     label='HER2 +'

    # # ER
    # s=mri_df['ER'][i]
    # nums=re.findall('\d+',s)
    # if nums and int(nums[0])>1:
    #     label='ER +'
    # else:
    #     label='ER -'

    # # PR
    # s=mri_df['PR'][i]
    # nums=re.findall('\d+',s)
    # if nums and int(nums[0])>1:
    #     label='PR +'
    # else:
    #     label='PR -'

    text = mri_df['MRI所见'][i]
    labels.append(label)
    mri_examples.append({"label":label,"text":text})


# statistics
print('LumB-1',labels.count('LumB-1'))
print('LumB-2',labels.count('LumB-2'))
print('LumA',labels.count('LumA'))
print('HER2',labels.count('H'))
print('TripleNegative',labels.count('T'))

# print("BI-RADS 3: ",labels.count('BI-RADS 3'))
# print("BI-RADS 4: ",labels.count('BI-RADS 4'))
# print("BI-RADS 5: ",labels.count('BI-RADS 5'))
# print("BI-RADS 6: ",labels.count('BI-RADS 6'))

# print("KI-67 h: ",labels.count('KI-67 h'))
# print("KI-67 l: ",labels.count('KI-67 l'))

# print("HER2 +: ",labels.count('HER2 +'))
# print("HER2 -: ",labels.count('HER2 -'))

# print("ER +: ",labels.count('ER +'))
# print("ER -: ",labels.count('ER -'))

# print("PR +: ",labels.count('PR +'))
# print("PR -: ",labels.count('PR -'))

# shuffle
random.seed(2019)
random.shuffle(mri_examples)

# save
mri_examples_path=join(json_dir,'ihc_subtype_examples.json')
with open(mri_examples_path,'w') as f:
    json.dump(mri_examples, f, indent=2, ensure_ascii=False)
