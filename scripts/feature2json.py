#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/16 16:46
# @Author  : ZHANG Shaohua
# @Contact : sofazhg@outlook.com
# @File    : feature2json.py
# @Software: PyCharm

import numpy as np
from os.path import abspath, join, dirname
import re
import pandas as pd
import random
import json
import warnings
warnings.filterwarnings("ignore")

project_dir = dirname(dirname(abspath(__file__)))
data_dir=join(project_dir,'data')
json_dir=join(data_dir,'json_data')
reports_dir=join(data_dir,'reports')

# load
mri_path=join(reports_dir,'MRI200.xlsx')
mri_df = pd.read_excel(mri_path)
num_rows = mri_df.shape[0]  # 行数：shape[0] 列数：shape[1]
print("MRI报告份数：%d"%num_rows)

# convert
sizes=[]
ADCs=[]
labels=[]
mri_examples=[]
for i in range(num_rows):

    # IHC subtype
    label = mri_df['分子分型'][i]

    # BI-RADS
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

    feature=[]

    symmetry=mri_df['双乳对称性'][i]
    symmetry_dict={'对称':0,'欠对称':1,'NG':0}
    feature.append(symmetry_dict[symmetry])

    skin=mri_df['皮肤'][i]
    skin_dict = {'光整': 0, '增厚水肿凹陷': 1,'穿刺': 0, 'NG': 0}
    feature.append(skin_dict[skin])

    nipple=mri_df['乳头'][i]
    nipple_dict = {'正常': 0, '凹陷回缩': 1, '先天凹陷': 0, '扁平': 0,'NG': 0}
    feature.append(nipple_dict[nipple])

    gland=mri_df['腺体含量'][i]
    gland_dict={'丰富':0,'退化':1,'少量':1,'NG':0}
    feature.append(gland_dict[gland])

    duct=mri_df['乳导管'][i]
    duct_dict = {'正常': 0, '扩张': 1, '扩张积液': 1, 'NG': 0}
    feature.append(duct_dict[duct])

    position=mri_df['肿块位置'][i]
    position_dict = {'左': 0, '右': 1}
    feature.append(position_dict[position])

    quadrant=mri_df['肿块象限'][i]  # 三维坐标系
    quadrant_dict = {'上方': [0,0,1], '内上': [0.707,0,0.707],'内侧': [1,0,0], '内下': [0.707,0,-0.707],'下方': [0,0,-1],
                     '外下': [-0.707,0,-0.707],'外侧': [-1,0,0], '外上': [-0.707,0,0.707],'后方': [0,1,0], 'NG': [0,0,0]}
    feature+=quadrant_dict[quadrant]

    orient=mri_df['肿块方位'][i]  # 二维坐标系
    orient_dict = {'1点': [0.5,0.8667],'2点': [0.8667,0.5], '3点': [1,0],'4点': [0.8667,-0.5], '5点': [0.5,-0.8667],
                   '6点': [0,-1], '7点': [-0.5,-0.8667],'8点': [-0.8667,-0.5], '9点': [-1,0],'10点':[-0.8667,0.5],
                   '11点':[-0.5,0.8667], '12点':[0,1],'NG': [0,0]}
    feature+=orient_dict[orient]

    size=mri_df['肿块尺寸'][i]
    if size=='NG':
        feature.append('NG')
    elif size[-2:]=='cm':
        size=re.sub('cm','',size)
        if size[:2]=='直径':
            size=re.sub('直径约','',size)
            volume=4/3*np.pi*(float(size)/2)**3
        else:
            lengths = [float(a) for a in size.split('*')]
            volume = 1
            for a in lengths:
                volume*=a
        feature.append(round(volume,4))
        sizes.append(round(volume,4))
    elif size[-2:]=='mm':
        size = re.sub('mm', '', size)
        if size[:2]=='直径':
            size=re.sub('直径约','',size)
            volume=4/3*np.pi*(float(size)/20)**3
        else:
            lengths = [float(a)/10 for a in size.split('*')]
            volume = 1
            for a in lengths:
                volume*=a
        feature.append(round(volume,4))
        sizes.append(round(volume,4))

    shape=mri_df['肿块形态'][i]
    shape_dict = {'不规则': 0, '分叶状': 0,'斑片状': 0, '团片状': 0,'类圆形': 1, '类椭圆形': 1,'规则': 1,'NG':1}
    feature.append(shape_dict[shape])

    margin=mri_df['肿块边界'][i]
    margin_dict = {'清晰光整': 0,'欠清晰光整': 1, '毛刺': 1,'分叶': 1,'NG':0}
    feature.append(margin_dict[margin])

    TIC=mri_df['强化曲线类型'][i]  # 五维one-hot：（渐增，平台，洗脱，速升，缓升）
    TIC_dict = {'渐增型':[1,0,0,0,0],'速升渐增型': [1,0,0,1,0], '平台型': [0,1,0,0,0],
                '速升平台型': [0,1,0,1,0],'缓升平台型': [0,1,0,0,1],'渐增平台型':[1,1,0,0,0],
                '洗脱型': [0,0,1,0,0],'速升洗脱型':[0,0,1,1,0],'速升速降型':[0,0,0,1,0],
                '持续上升型': [0,0,0,0,1],'缓慢持续强化':[0,0,0,0,1], 'NG':[0,0,0,0,0]}
    feature+=TIC_dict[TIC]

    T2WI=mri_df['T2WI信号强度'][i]
    T2WI_dict={'高':1,'等高':0.5,'等':0,'等低':-0.5,'低':-1,'混杂':0,'NG':0}
    feature.append(T2WI_dict[T2WI])

    DWI=mri_df['DWI信号强度'][i]
    DWI_dict={'增高':0,'NG':1}
    feature.append(DWI_dict[DWI])

    ADC=mri_df['ADC值'][i]
    if ADC=='NG':
        feature.append('NG')
    else:
        a=float(ADC.split('*')[0])
        feature.append(a)
        ADCs.append(a)

    lymph=mri_df['腋窝淋巴结'][i]
    lymph_dict = {'正常': 0,'肿大': 1}
    feature.append(lymph_dict[lymph])

    # lymph_size=mri_df['淋巴结尺寸'][i]

    labels.append(label)
    mri_examples.append({"label": label, "feature": feature})
print(mri_examples)

# substitute
mean_size=round(np.mean(sizes),4)
mean_ADC=round(np.mean(ADCs),4)
for example in mri_examples:
    if example['feature'][11]=='NG':
        example['feature'][11]=mean_size
    if example['feature'][21]=='NG':
        example['feature'][21]=mean_ADC

print(mri_examples)

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
mri_json_path=join(json_dir,'ihc_subtype_features.json')
with open(mri_json_path, 'w') as f:
    json.dump(mri_examples,f,indent=2,ensure_ascii=False)
