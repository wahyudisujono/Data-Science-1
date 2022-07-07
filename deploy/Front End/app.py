from itertools import tee
from pyparsing import col
import streamlit as st
import requests
st.set_page_config(
    page_title="Sistem Auto Sementation",
    page_icon="👜",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.title("Aplikasi Clustering Konsumen")
st.header('INPUT:')
cols=st.columns([2,2,2,2])
contain_input=st.container()
contain_output=st.container()
with contain_input:
    with cols[0]:
        st.subheader('Personal Information')
        education = st.selectbox("Education", ['Basic','Graduation', 'Master', 'PhD'])
        income = st.number_input("Income")
        kid = st.number_input("Number Of Kid", step=1)
        teen = st.number_input("Number Of Teen", step=1)
        days = st.number_input("Days", step=1)
        recency = st.number_input("Recency", step=1)
        age = st.number_input("Age", step=1)

    with cols[1]:
        st.subheader('Purchase Information')
        meat = st.number_input("Purchase Meat/Mounth", step=1)
        wines = st.number_input("Purchase wines/Mounth", step=1)
        fruit = st.number_input("Purchase Fruit/Mounth", step=1)
        fish = st.number_input("Purchase fish/Mounth", step=1)
        sweet = st.number_input("Purchase sweets/Mounth", step=1)
        gold = st.number_input("Purchase gold/Mounth", step=1)

    with cols[2]:
        st.subheader('Platform Information')
        purchase = st.number_input("Number of purchase", step=1)
        web = st.number_input("Purchase On Web / Month", step=1)
        deal = st.number_input("Number Purchase by Diskon", step=1)
        catalog = st.number_input("Number purchase by catalog", step=1)
        store = st.number_input("Number of purchase in store", step=1)
        web_visit= st.number_input("Number of Viewing Website", step=1)

    with cols[3]:
        st.subheader('Promotion Information')
        st.markdown("Check If **True**")
        accept1 = st.checkbox("Accept Promo in 1st offer?", ['no','yes'])
        accept2 = st.checkbox("Accept Promo in 2nd offer?", ['no', 'yes'])
        accept3 = st.checkbox("Accept Promo in 3rd offer?", ['no', 'yes'])
        accept4 = st.checkbox("Accept Promo in 4th offer?", ['no', 'yes'])
        accept5 = st.checkbox("Accept Promo in 5th offer?", ['no', 'yes'])
        complain = st.checkbox("There is Complain?", ['no', 'yes'])
        res = st.checkbox("There is Response?", ['no', 'yes'])
    # inference
    def isyes(yes):
        if yes=='yes': return 1
        else : return 0

data2={'Education':education, 
        'Income': income, 
        'Kidhome': kid, 
        'Teenhome': teen, 
        'Dt_Customer': days,
        'Recency': recency,
        'MntWines': wines, 
        'MntFruits': fruit, 
        'MntMeatProducts': meat, 
        'MntFishProducts': fish, 
        'MntSweetProducts': sweet, 
        'MntGoldProds': gold,
        'NumDealsPurchases': purchase,
        'NumWebPurchases': web, 
        'NumCatalogPurchases': catalog,
        'NumStorePurchases': store, 
        'NumWebVisitsMonth': web_visit, 
        'AcceptedCmp3': isyes(accept3), 
        'AcceptedCmp4': isyes(accept4), 
        'AcceptedCmp5': isyes(accept5), 
        'AcceptedCmp1': isyes(accept1), 
        'AcceptedCmp2' : isyes(accept2),
        'Complain': isyes(complain), 
        'Response':isyes(res), 
        'age':age

}
URL='https://model-backend-wahyudisujono.herokuapp.com/cluster_customer' # sebelum push backend

# komunikasi
r = requests.post(URL, json=data2)

res = r.json()
with contain_output:
    st.header('OUTPUT')
    if r.status_code == 200:
        st.header('Pelanggan ini adalah '+ res['label_name'])
    elif r.status_code == 400:
        st.title("ERROR BOSS")
        st.write(res['message'])
    if res['label_idx']=='0':
        st.image('priority.png', width=600)
    elif res['label_idx']=='1':
        st.image('potensial.png', width=600)
    else:
        st.image('reguler.png', width=600)