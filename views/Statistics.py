import streamlit as st
import pandas as pd
import tempfile
from bs4 import BeautifulSoup
from pathlib import Path
import streamlit.components.v1 as components
from utils import annotate_txt
import matplotlib.colors as mcolors
import glob
import os
def run():
    
    if 'df_entities' in st.session_state.keys():
        df_entities=  st.session_state['df_entities']
        labels= df_entities['Label'].unique()
         
    else:
        df_entities= None
        labels= []
    #print(labels)
    temp= None
    options= ['All']
    if len(labels) > 0:
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

    options= []
    basepath= './COLLECTIONS/'
    for collection in glob.glob('./COLLECTIONS/*.csv'):
        options.append(os.path.basename(collection))
    
    collection= st.selectbox('Select a collection', options) 
    df_collection= pd.read_csv(basepath+collection)
    #st.dataframe(df_collection['Text'])

    entities= []
    for index in df_collection.index:
        #st.write(df_collection.loc[index, 'Text'])
        entities.append(df_collection.loc[index, 'Text'])
    total_coincidencias= 0
    nowords= []
    if temp is not None:
        for index in temp.index:
            if temp.loc[index, 'Text'] in entities:
                total_coincidencias+=1
            else:
                palabra= temp.loc[index, 'Text']  
                nowords= nowords +[palabra]
                     
        st.write('Total de coincidencias: ', total_coincidencias)
        st.write('No coincidencias: ', len(temp.index)-total_coincidencias)
        s= ''
        for i in nowords:
            s += "-" + i + "\n"
        st.markdown(s)