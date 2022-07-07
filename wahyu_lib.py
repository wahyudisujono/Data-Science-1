import math
import matplotlib.pyplot as plt
import seaborn as sns

def pisah_skew_gaus(data):
    list_num_skew=[]
    list_num_gaus=[]
    for col in data.columns:
        if data[col].skew()<0.5 and data[col].skew()>-0.5: list_num_gaus.append(col)
        else: list_num_skew.append(col)
    print('kolom gausian    : ', ",".join(list_num_gaus))
    print('kolom Skew       : ', ",".join(list_num_skew))
    return list_num_gaus, list_num_skew


def show_kde(data, list, hue, column=3, figsize=[15,6]):
    baris= math.ceil(len(list)/column)
    fig, ax = plt.subplots(baris,column, figsize=figsize)
    fig.tight_layout(h_pad=1.5)
    i=0
    j=0
    for col in list:
        sns.kdeplot(data=data, hue=hue, x = col, ax=ax[j][i], palette='Set1')
        i=i+1
        if i==column:
            i=0
            j=j+1

def show_count(data, list, hue, column=3, figsize=[15,6]):
    baris= math.ceil(len(list)/column)
    fig, ax = plt.subplots(baris,column, figsize=figsize)
    fig.tight_layout(h_pad=1.5)
    i=0
    j=0
    for col in list:
        sns.countplot(data=data, hue=hue, x = col, ax=ax[j][i], palette='Set1')
        i=i+1
        if i==column:
            i=0
            j=j+1