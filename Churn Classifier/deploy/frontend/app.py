import pickle
import streamlit as st
import pandas as pd
import requests
import json
import numpy as np

st.set_page_config(
    page_title="Sistem Auto Classification Churn Customer",
    page_icon="🔄",
    layout="wide",
)

def open_model(model_path):
    with open (model_path, 'rb') as f:
        model = pickle.load(f)
    return model

def isyes(data):
    if data: return 'Yes'
    else: return 'No'

def process_input(data):
    data=pd.DataFrame(data, index=[0])
    pipeline_pre=open_model('preprocessing_pipeline.pkl')
    return pipeline_pre.transform(data)

def predict(data):
    input_data_json = json.dumps({
        "signature_name": "serving_default",
        "instances": data,
    })
    URL = 'https://tf-serving-wahyudi.herokuapp.com/v1/models/churn:predict'
    r=requests.post(URL, input_data_json).json()
    result= np.array(r['predictions'][:][0])
    if result>0.55: return 'Churn'
    else: return 'No Churn'

st.markdown("""
    <h1 style="color:#26608e;"> Auto Prediction System </h1>
    """, unsafe_allow_html=True)
contain_input=st.container()
contain_output=st.container()
with contain_input:
    st.subheader('Customer Information')
    MonthlyCharges = st.number_input("Monthly Charges", min_value=0)
    TotalCharges = st.number_input("TotalCharges", min_value=0)
    Contract = st.selectbox("Contract", ['One year', 'Two year', 'Month-to-month'])
    PaymentMethod = st.selectbox("Payment Method", ['Mailed check','Electronic check','Bank transfer (automatic)','Credit card (automatic)'])
    InternetService = st.selectbox("Internet Service", ['No', 'DSL', 'Fiber optic'])
    PaperlessBilling = st.checkbox("Paperless Billing", ['No', 'Yes'])
    TechSupport = st.checkbox("Tech. Support", ['No' 'Yes'])


data={'MonthlyCharges':MonthlyCharges,
    'TotalCharges':TotalCharges,
    'Contract':Contract,
    'PaymentMethod':PaymentMethod,
    'InternetService':InternetService,
    'PaperlessBilling':isyes(PaperlessBilling),
    'TechSupport':isyes(TechSupport)}
st.markdown("""
    <h2 style="color:#26608e;"> Clustering Result</h2>
    """, unsafe_allow_html=True)
data=process_input(data).tolist()
predict = predict(data)
if predict=="Churn":
    st.markdown('<h3 style="color:#cc0000;">'+predict+'</h3>', unsafe_allow_html=True)
else:
    st.markdown('<h3 style="color:#59a92f;">'+predict+'</h3>', unsafe_allow_html=True)