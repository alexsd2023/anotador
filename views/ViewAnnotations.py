#!/usr/bin/env python
# coding: utf-8
import streamlit as st
import pandas as pd
from PIL import Image
import glob
import os

from annotated_text import annotated_text
from st_click_detector import click_detector
from bs4 import BeautifulSoup

#import utils
from utils import annotate_txt
import tempfile
from pathlib import Path

def run():
    option= 'View Annotations'
    if option == 'View Annotations':
        
        uploaded_html_file= st.file_uploader("Choose a html file")
        uploaded_annotation_file= st.file_uploader("Choose an annotation file", type={"csv"})

        if uploaded_annotation_file is not None:
            
            annotations_df= pd.read_csv(uploaded_annotation_file)
            st.write(annotations_df)
            st.session_state['annotations_df']= annotations_df

        elif 'annotations_df' in st.session_state:
            annotations_df= st.session_state['annotations_df'] 
            st.write(annotations_df)

        buttonAnnotate= st.button("Annotate", "primary")
        if buttonAnnotate:
                
            if (uploaded_html_file is not None) or ('uploaded_html_file' in st.session_state):
                
                if 'uploaded_html_file' in st.session_state:
                    uploaded_html_file= st.session_state['uploaded_html_file']
                else:
                    st.session_state['uploaded_html_file']= uploaded_html_file

                print(uploaded_html_file) 
                
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    #st.markdown("# Original text file")
                    fp = Path(tmp_file.name)
                    fp.write_bytes(uploaded_html_file.getvalue())
                
                with open(fp,'r') as file:
                    #plain_text= file.read()
                    #st.markdown(plain_text, unsafe_allow_html= True)
                    soup= BeautifulSoup(file.read(), 'html.parser')
                    #plain_text= soup.get_text('\n')
                    #lines= plain_text.split('\n')
                    lines= soup.find_all('p')

                    index= 0
                    #print(plain_text)
                    print(lines)
                    for line in lines:
                        line= line.get_text()
                        df_line= annotations_df.loc[annotations_df['Line'] == index]    
                        #Call util function
                        
                        aline= annotate_txt.annotate_line(line, df_line)
                        
                        annotated_text(aline)
                        index+= 1
                        
