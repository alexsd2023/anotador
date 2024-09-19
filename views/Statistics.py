import streamlit as st
import pandas as pd
import tempfile
from bs4 import BeautifulSoup
from pathlib import Path
import streamlit.components.v1 as components
from utils import annotate_txt
import matplotlib.colors as mcolors
import glob

def run():
    
    if 'df_entities' in st.session_state.keys():
        df_entities=  st.session_state['df_entities']
        labels= df_entities['Label'].unique()
         
    else:
        df_entities= None
    #print(labels)
    options= ['All']
    options+= labels.tolist()
    option= st.selectbox('Select an entity', options)   
    if option == 'All':
        st.table(df_entities)            
    else: 
        temp= df_entities[df_entities['Label'] == option]
        temp= temp[['Text' , 'Start char' ,'End char']]
        N= len(temp.index)
        temp['No.']= list(range(N))
        temp.set_index('No.', inplace= True)
        st.table(temp)

    options= glob.glob('../COLLECTIONS/*')
    for collection in glob.glob('../COLLECTIONS/*.csv'):
        print(collection)
    print('collections:', options)
    collections= st.selectbox('Select a collection', options) 
