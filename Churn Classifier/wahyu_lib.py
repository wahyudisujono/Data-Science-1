import math
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from feature_engine.outliers import Winsorizer
from sklearn.model_selection import train_test_split



## Preprocessing
def pisah_skew_gaus(data, massage=True):
    list_num_skew=[]
    list_num_gaus=[]
    for col in data.columns:
        if data[col].skew()<0.5 and data[col].skew()>-0.5: list_num_gaus.append(col)
        else: list_num_skew.append(col)
    if massage:
        print('kolom gausian    : ', ", ".join(list_num_gaus))
        print('kolom Skew       : ', ", ".join(list_num_skew))
        
    return list_num_gaus, list_num_skew

def handling_outliers(data, list):
    list_gaus, list_skew=pisah_skew_gaus(data[list])
    if list_gaus:
        data=Winsorizer(capping_method='gaussian', tail='both', fold=3, variables=list_gaus, missing_values='ignore').fit_transform(data)
    if list_skew:
        data=Winsorizer(capping_method='iqr', tail='both', fold=3, variables=list_skew, missing_values='ignore').fit_transform(data)
    return data

def split_data(data, target, test_ratio=0.2, val_ratio=0.2):
    X = data.drop(columns=target)
    y = data[[target]]
    X_train_full, X_test, y_train_full, y_test = train_test_split(X, y, test_size=test_ratio, random_state=17)
    X_train, X_val, y_train, y_val = train_test_split(X_train_full, y_train_full, test_size=val_ratio, random_state=17)
    return X_train, y_train, X_val, y_val, X_test, y_test

def pisah_num_cat(data, massage=True):
    num_list = data.select_dtypes(include=np.number).columns.tolist()
    cat_list = data.select_dtypes(include=['object']).columns.tolist()
    if massage:
        print('feature numerik   : ', ", ".join(num_list))
        print('feature kategorik : ', ", ".join(cat_list))
    return num_list, cat_list



#Plotting
def show_kde(data, list, hue=None, column=3, figsize=[15,6]):
    baris= math.ceil(len(list)/column)
    fig, ax = plt.subplots(baris,column, figsize=figsize)
    fig.tight_layout(h_pad=1.5)
    i=0
    j=0
    for col in list:
        sns.kdeplot(data=data, hue=hue, x = col, ax=ax[j][i])
        i=i+1
        if i==column:
            i=0
            j=j+1

def show_count(data, list, hue=None, column=3, figsize=[15,6]):
    baris= math.ceil(len(list)/column)
    fig, ax = plt.subplots(baris,column, figsize=figsize)
    fig.tight_layout(h_pad=1.5)
    i=0
    j=0
    for col in list:
        sns.countplot(data=data, hue=hue, x = col, ax=ax[j][i])
        i=i+1
        if i==column:
            i=0
            j=j+1

def histplot_1d(data,list, hue=None, figsize=[15,5]):
    fig, ax=plt.subplots(1,len(list), figsize=figsize)
    i=0
    for col in list:
        sns.histplot(data=data, x=col, kde=True, hue=hue, ax=ax[i])
        i=i+1