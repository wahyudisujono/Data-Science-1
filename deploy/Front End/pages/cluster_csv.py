import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import requests
import seaborn as sns
import matplotlib.pyplot as plt

#setting page
st.set_page_config(
    page_title="Sistem Auto Sementation",
    page_icon="👜",
    layout="wide",
)

#file template
template=pd.read_csv('template.csv')

st.title('Sistem Auto Cluster') #Specify title of your app
st.sidebar.markdown('## Data Import') #Streamlit also accepts markdown

#file to cluster
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv") #data uploader
st.sidebar.download_button('Download Template Here!', template.to_csv(), file_name='template.csv')

# if file has uploaded
if uploaded_file is not None:
    st.markdown("""
    <h2 style="color:#26608e;"> Data Input Viewer </h2>
    """, unsafe_allow_html=True)
    data = pd.read_csv(uploaded_file)
    st.write(data)
    URL='https://model-backend-wahyudisujono.herokuapp.com/cluster_from_csv' # sebelum push backend
    # komunikasi
    r = requests.post(URL, json=data.to_json())
    output=r.json()


    st.markdown("""
    <h2 style="color:#26608e;"> Clustering Result</h2>
    """, unsafe_allow_html=True)
    data['Prediction']=output['prediction']
    st.write(data[['Nama','Prediction']])
    st.download_button('Download Clustering Result!', data.to_csv(), file_name='result.csv')
    
    st.markdown(f'<h3 "> Clustering Overview </h3>',
            unsafe_allow_html=True)
    fig, ax=plt.subplots()
    sns.countplot(data=data, x='Prediction', ax=ax)
    st.pyplot(fig)


else:
    st.markdown("""
    <br>
    <br>
    <h1 style="color:#26608e;"> Upload your CSV file to begin clustering </h1>
    """, unsafe_allow_html=True) 
    st.markdown('<hr>', unsafe_allow_html=True)

