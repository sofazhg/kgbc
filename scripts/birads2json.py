#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/4 10:37
# @Author  : ZHANG Shaohua
# @Contact : sofazhg@outlook.com
# @File    : birads2json.py
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
mri_path=join(reports_dir,'MRI200拆分bi-rads.xlsx')
mri_df = pd.read_excel(mri_path)
num_rows = mri_df.shape[0]  # 行数：shape[0] 列数：shape[1]
print("MRI报告份数：%d"%num_rows)

# process
mri_examples=[]
labels=[]
for i in range(num_rows):
    nums=[]
    s=mri_df['印象与建议'][i]
    s=re.sub('[（）()]','',s)
    s=re.sub('[,；。\n]', '，', s)
    for x in s.split('，'):
        if 'BI-RADS' in x:
            nums+=re.findall('\d',x)
            # print(s)
            # print(nums)
            label='BI-RADS '+max(nums)
            text = mri_df['MRI所见'][i]
            labels.append(label)
            mri_examples.append({"label": label, "text": text})

# statistics
print("BI-RADS 0: ",labels.count('BI-RADS 0'))
print("BI-RADS 1: ",labels.count('BI-RADS 1'))
print("BI-RADS 2: ",labels.count('BI-RADS 2'))
print("BI-RADS 3: ",labels.count('BI-RADS 3'))
print("BI-RADS 4: ",labels.count('BI-RADS 4'))
print("BI-RADS 5: ",labels.count('BI-RADS 5'))
print("BI-RADS 6: ",labels.count('BI-RADS 6'))

# shuffle
random.seed(2019)
random.shuffle(mri_examples)

# save
mri_examples_path=join(json_dir,'birads_split_examples.json')
with open(mri_examples_path,'w') as f:
    json.dump(mri_examples, f, indent=2, ensure_ascii=False)
