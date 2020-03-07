#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/31 11:51
# @Author  : ZHANG Shaohua
# @Contact : sofazhg@outlook.com
# @File    : mri_classify_tfidf.py
# @Software: PyCharm

import jieba  # Chinese Word Extraction Data https://github.com/fxsjy/jieba/
import numpy as np
from os.path import abspath, join, dirname
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold,StratifiedShuffleSplit,GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report,roc_auc_score,accuracy_score,roc_curve,auc
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb
from scipy.interpolate import interp2d
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

project_dir = dirname(dirname(abspath(__file__)))
data_dir=join(project_dir,'data')
json_dir=join(data_dir,'json_data')

# load
mri_examples_path=join(json_dir,'birads_split_examples.json')
with open(mri_examples_path,'r',encoding='gbk') as f:
    mri_examples=json.load(f)

# Chinese segmentation
# dict_dir=join(project_dir,'dict')
# dict_mri_path=join(dict_dir,'dict_mri.txt')
# jieba.load_userdict(dict_mri_path)  # 载入MRI关键词词典
# stoplist_mri_path=join(dict_dir,'stoplist_mri.txt')
# stoplist=[line.strip() for line in open(stoplist_mri_path,'r',encoding='utf-8')]
# X_text=[' '.join(seg for seg in jieba.cut(example['text']) if seg not in stoplist) for example in mri_examples]
X_text=[' '.join(jieba.cut(example['text'])) for example in mri_examples]

# tf-idf process
tfidf = TfidfVectorizer()
tfidf.fit(X_text)
X_tfidf=np.array([tfidf.transform([text]).toarray()[0] for text in X_text])

# label encoder
Y_label=[]
# for example in mri_examples:
#     if example['label'] in ['T']:
#         Y_label.append('T')
#     else:
#         Y_label.append('non_T')
Y_label=[example['label'] for example in mri_examples]
le = LabelEncoder()
le.fit(Y_label)
Y_le = le.transform(Y_label)
print(le.inverse_transform([0,1,2,3,4,5]))

# train
tprs=[]
aucs=[]
mean_fpr=np.linspace(0,1,100)
sfolder = StratifiedKFold(n_splits=10,random_state=0,shuffle=False)
# sfolder = StratifiedShuffleSplit(n_splits=10,random_state=0)
auc_scores=[]
acc_scores=[]
count=0
i=0
for train, test in sfolder.split(X_tfidf,Y_le):
    print("="*20, "\nProcessing Round {} ...".format(count))
    X_train = np.array([X_tfidf[i] for i in train])
    Y_train = np.array([Y_le[i] for i in train])
    X_test = np.array([X_tfidf[i] for i in test])
    Y_test = np.array([Y_le[i] for i in test])

    assert X_train.shape[0] == Y_train.shape[0]
    assert X_test.shape[0] == Y_test.shape[0]

    # # SVC 'rbf'
    # param_grid = {'C': [1e1, 1e2, 1e3, 1e4, 1e5], 'gamma': [0.0001, 0.001, 0.01, 0.1]}
    # clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced', probability=True), param_grid=param_grid, cv=5)
    # # SVC 'linear'
    # param_grid = {'C': [1e1, 1e2, 1e3, 1e4, 1e5]}
    # clf = GridSearchCV(SVC(kernel='linear', class_weight='balanced', probability=True), param_grid=param_grid, cv=5)
    # RandomForest
    # param_grid = {'n_estimators': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
    # clf = GridSearchCV(RandomForestClassifier(bootstrap=True, oob_score=True, criterion='gini'), param_grid=param_grid,cv=5)
    # lightGBM
    param_grid = {'num_leaves':[2,4,6,8,10,12,14,16,18,20],
                  'learning_rate':[0.02,0.04,0.06,0.08,0.1,0.12,0.14,0.16,0.18,0.2],
                  'n_estimators': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
    clf = GridSearchCV(lgb.sklearn.LGBMClassifier(), param_grid=param_grid,cv=5)
    # train model
    clf.fit(X_train,Y_train)
    Y_pred=clf.predict(X_test)

    # 计算fpr(假阳性率),tpr(真阳性率),thresholds(阈值)[绘制ROC曲线要用到这几个值]
    # fpr, tpr, thresholds = roc_curve(Y_test, Y_pred)
    # 插值 把结果添加到tprs列表中
    # tprs.append(interp2d(mean_fpr, fpr, tpr))
    # tprs[-1][0] = 0.0
    # 计算auc
    # roc_auc = auc(fpr, tpr)
    # aucs.append(roc_auc)
    # 画图，只需要plt.plot(fpr,tpr),变量roc_auc只是记录auc的值，通过auc()函数计算出来
    # plt.plot(fpr, tpr, lw=1, alpha=0.3, label='ROC fold %d(area=%0.2f)' % (i, roc_auc))
    # i += 1

    # auc_score = round(roc_auc_score(Y_test, Y_pred),2)
    # auc_scores.append(auc_score)
    acc_score = round(accuracy_score(Y_test, Y_pred), 2)
    acc_scores.append(acc_score)
    print("Y_test:", Y_test)
    print("Y_pred:", Y_pred)
    # print("Auc score:", auc_score)
    print("Acc score:", acc_score)
    print("Best score:", clf.best_score_)
    print("Best param:", clf.best_params_)
    print("Classification Report:\n", classification_report(Y_test, Y_pred))
    count += 1

# print("Auc scores:", auc_scores)
print("Acc scores:", acc_scores)
# print("Average auc scores:", round(sum(auc_scores) / 10, 2))
print("Average acc scores:", round(sum(acc_scores) / 10, 2))

# 画对角线
# plt.plot([0,1],[0,1],linestyle='--',lw=2,color='r',label='Luck',alpha=.8)
# mean_tpr=np.mean(tprs,axis=0)
# mean_tpr[-1]=1.0
# mean_auc=auc(mean_fpr,mean_tpr)  # 计算平均AUC值
# std_auc=np.std(tprs,axis=0)
# plt.plot(mean_fpr,mean_tpr,color='b',label=r'Mean ROC (area=%0.2f)'%mean_auc,lw=2,alpha=.8)
# std_tpr=np.std(tprs,axis=0)
# tprs_upper=np.minimum(mean_tpr+std_tpr,1)
# tprs_lower=np.maximum(mean_tpr-std_tpr,0)
# plt.fill_between(mean_tpr,tprs_lower,tprs_upper,color='gray',alpha=.2)
# plt.xlim([-0.05,1.05])
# plt.ylim([-0.05,1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('ROC')
# plt.legend(loc='lower right')
# plt.show()

