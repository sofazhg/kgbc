#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/9 16:54
# @Author  : ZHANG Shaohua
# @Contact : sofazhg@outlook.com
# @File    : mammo_structurize.py
# @Software: PyCharm

import csv
from os.path import abspath, join, dirname

project_dir = dirname(dirname(abspath(__file__)))
data_dir=join(project_dir,'data')
json_dir=join(data_dir,'json_data')
reports_dir=join(data_dir,'reports')

mammo_path=join(reports_dir,'乳腺钼靶100.txt')
with open(mammo_path,'r',encoding='utf-8') as f:
    mammo=f.read()

csv_path=join(reports_dir,'乳腺钼靶100.csv')
f=open(csv_path,'w',encoding='gbk')
csv_writer = csv.writer(f)
csv_writer.writerow(['病人性别','年龄','检查项目','设备名称','临床诊断','既往病史','影像学表现','影像学诊断'])

reports=mammo.split('\n\n\n')
for report in reports:
    tmp=report.split('\n\n')
    if len(tmp)==7:
        tmp=tmp[:5]+['']+tmp[5:]
    print(tmp)
    csv_writer.writerow(tmp)
f.close()

