import streamlit as st
import spacy
from spacy.lang.es.examples import sentences 
from spacy.lang.es.stop_words import STOP_WORDS
from spacy import displacy
from spacy.tokens import Span
import streamlit.components.v1 as components
import tempfile
from pathlib import Path
import tensorflow as tf
from bs4 import BeautifulSoup
import pandas as pd


def read_htmlfile(html):
    file = open(html, "r")
    content = file.read()
    soup=BeautifulSoup(content)
    file.close()
    return soup.get_text()

def run():
    if 'index' in st.session_state.keys():
        index= st.session_state['index']
    else:
        index= 0  
    modelname = st.radio(
         "Select a model",
        ["Spacy Ruler (Sentences)", "DECM annotations with Paragraphs"],
         index=index,
    )
    if modelname == 'Spacy Ruler (Sentences)':
        st.session_state['index']= 0
        trained_nlp= spacy.load("./models/model_entities_ruler/model-last/")
    elif modelname == 'DECM annotations with Paragraphs':
        trained_nlp= spacy.load("./models/model_toponyms_patterns/model-last/")
        st.session_state['index']= 1

    uploaded_file= st.file_uploader("Choose a raw data file", type=['html', 'htm', 'txt', 'text'],  accept_multiple_files= False)
    texto= ""
    if 'uploaded_file' in st.session_state.keys():
        uploaded_file= st.session_state['uploaded_file']

    if uploaded_file is not None:
        print(uploaded_file) 
        st.session_state['uploaded_file']= uploaded_file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            #st.markdown("# Original text file")
            fp = Path(tmp_file.name)
            fp.write_bytes(uploaded_file.getvalue())
            #print(fp)
        flag= True  
        with open(fp,'r') as file:
            if Path(uploaded_file.name).suffix in ['txt', 'text']:
                texto = " ".join(line for line in file)
            else:  
                texto= read_htmlfile(fp)    
    

    doc= trained_nlp(texto)

    #st.text_area("Annotated text", value= texto,  key= "text", height=520)
    data= []
    for ent in doc.ents:
        #print (ent.text, ent.label_, ent.start_char, ent.end_char)
        data.append([ent.text, ent.label_, ent.start_char, ent.end_char])
    df_entities= pd.DataFrame(data, columns= ['Text', 'Label', 'Start char', 'End char'])
    st.session_state['df_entities']= df_entities

    ent_html= displacy.render(doc, style="ent", jupyter= False)
    st.markdown(ent_html, unsafe_allow_html= True)

