import streamlit as st
import pandas as pd
import numpy as np
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import json

#setting page
st.set_page_config(
    page_title="Sistem Auto Classification Churn Customer",
    page_icon="🔄",
    layout="wide",
)

def open_model(model_path):
    with open (model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def process_input(data):
    pipeline_pre=open_model('preprocessing_pipeline.pkl')
    return pipeline_pre.transform(data)

def predict(data):
    input_data_json = json.dumps({
        "signature_name": "serving_default",
        "instances": data,
    })
    URL = 'https://tf-serving-wahyudi.herokuapp.com/v1/models/churn:predict'
    r=requests.post(URL, input_data_json).json()
    result= np.array(r['predictions'])
    return result


#downloaf file template
template=pd.read_csv('template.csv')
st.title('Sistem Auto Classification Churn Customer') 

#Uplaod data
st.markdown('## Import Your Data Here')
uploaded_file = st.file_uploader("just file csv!",type="csv")
st.download_button('Download Template Here!', template.to_csv(), file_name='template.csv')

# if file has uploaded
if uploaded_file is not None:
    st.markdown("""
    <h2 style="color:#26608e;"> Data Input Viewer </h2>
    """, unsafe_allow_html=True)
    data = pd.read_csv(uploaded_file)
    st.write(data)

    st.markdown("""
    <h2 style="color:#26608e;"> Clustering Result</h2>
    """, unsafe_allow_html=True)
    
    pred=predict(process_input(data).tolist())
    pred=np.where(pred>0.55,'Churn', 'No Churn')
    data_predict=data.copy()
    data_predict['predict']=pred
    st.write(data_predict[['customerID', 'gender', 'predict']])


    st.download_button('Download Clustering Result!', data_predict.to_csv(), file_name='result.csv')
    
    st.markdown(f'<h3 "> Clustering Overview </h3>',
            unsafe_allow_html=True)
    fig, ax=plt.subplots()
    sns.countplot(data=data_predict, x='predict', ax=ax)
    st.pyplot(fig)


else:
    st.markdown("""
    <br>
    <br>
    <h1 style="color:#26608e;"> Upload your CSV file to begin clustering </h1>
    """, unsafe_allow_html=True) 
    st.markdown('<hr>', unsafe_allow_html=True)

