import streamlit as st
import numpy as np
import requests
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import json
import re

#setting page
st.set_page_config(
    page_title="Sentimen Classifier",
    page_icon="🔄",
    layout="wide",
)

def predict(teks):
    input_data_json = json.dumps({
        "signature_name": "serving_default",
        "instances": [[teks]],
    })
    URL = 'http://tf-serving-sentiment.herokuapp.com/v1/models/sentiment:predict'
    r=requests.post(URL, input_data_json).json()
    result= r['predictions'][0]
    result= np.argmax(result)
    if result==0:
        return 'Negative'
    elif result==1:
        return 'Neural'
    else:
        return 'positive'


def preprocessing_text(texts):
  lemmatizer = WordNetLemmatizer()
  texts = texts.lower() #membuat menjadi huruf kecil
  texts = texts.strip()
  texts = re.sub("@[a-z0-9_.]+"," ", texts) # menghilangkan kata yang berawalan @
  texts = re.sub(r"\\n"," ",texts) #menghapus tanda enter
  texts = re.sub(r"http\S+", " ", texts) #menghapus link
  texts = re.sub(r"www.\S+", " ", texts) #menghapus link
  texts = re.sub("[^a-z\s']","", texts) # menghapus selain alfabet
  texts=lemmatizer.lemmatize(texts) #lematizing
  tokens = word_tokenize(texts) # tokeenize
  texts = ' '.join([word for word in tokens if word not in stop_words]) #menghapus stop word
  return texts

stop_words = []
with open('stopwords.txt') as f:
    for line in f:
        line=line.strip()
        stop_words.append(line)
#==============================================================
st.sidebar.header('What Your Tweet Sentimen?')
st.sidebar.write('This application is an application that can understand the sentiment content in your tweets.')
st.sidebar.write('Be Enjoy!')

st.markdown("""
<h1 style="color:#26608e;">Classification Sentiment Twitter</h1>
""", unsafe_allow_html=True)
input_teks=st.text_input('Input your tweet here', max_chars = 280)

if input_teks!='':  
    teks_bersih=preprocessing_text(input_teks)
    predict=predict(teks_bersih)
    # st.markdown('<h3 style="color:#59a92f;"> Your tweet is '+predict+' sentiment</h3>', unsafe_allow_html=True)
    st.info('Your tweet is **'+predict+'** sentiment')
else:
    # st.markdown('<h3 style="color:#59a92f;">Your tweet is empty</h3>', unsafe_allow_html=True)
    st.warning('Your tweet is empty')
    