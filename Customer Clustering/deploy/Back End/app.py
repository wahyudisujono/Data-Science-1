import pickle
from flask import Flask, request
import pandas as pd

app=Flask(__name__)

def open_model(model_path):
    with open (model_path, 'rb') as f:
        model = pickle.load(f)
    return model


model_cluster=open_model('finalpipe.pkl') #pandas
def inference_cluster(data, model):
    LABEL= ['Pelanggan Prioritas', 'Pelanggan Potensial', 'Pelanggan Regular']
    columns= ['Education', 'Income', 'Kidhome', 'Teenhome', 'Dt_Customer','Recency', 
        'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds',
       'NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases','NumStorePurchases', 'NumWebVisitsMonth', 
       'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1', 'AcceptedCmp2',
       'Complain', 'Response', 'age']
    newdata=pd.DataFrame(data=[data], columns=columns)
    res = model.predict(newdata)
    return res[0], LABEL[res[0]]

@app.route('/')
def homepage():
    return 'halo'
   
@app.route('/cluster_customer', methods=['POST'])
def cluster_customer():
    konten=request.json
    new_data=[
            konten['Education'],
            konten['Income'],
            konten['Kidhome'],
            konten['Teenhome'],
            konten['Dt_Customer'],
            konten['Recency'], 
            konten['MntWines'], 
            konten['MntFruits'], 
            konten['MntMeatProducts'], 
            konten['MntFishProducts'], 
            konten['MntSweetProducts'], 
            konten['MntGoldProds'],
            konten['NumDealsPurchases'], 
            konten['NumWebPurchases'], 
            konten['NumCatalogPurchases'],
            konten['NumStorePurchases'], 
            konten['NumWebVisitsMonth'], 
            konten['AcceptedCmp3'], 
            konten['AcceptedCmp4'], 
            konten['AcceptedCmp5'], 
            konten['AcceptedCmp1'], 
            konten['AcceptedCmp2'],       
            konten['Complain'], 
            konten['Response'], 
            konten['age']
            ]
    res_idx, res_label=inference_cluster(new_data, model_cluster)
    result={
            'label_idx': str(res_idx),
            'label_name':res_label
    }
    return result, 200
    


# app.run(debug=True)

#fungsi untuk inference 