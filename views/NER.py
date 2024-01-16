import streamlit as st
import spacy
from spacy.lang.es.examples import sentences 
from spacy.lang.es.stop_words import STOP_WORDS
from spacy import displacy
from spacy.tokens import Span
import streamlit.components.v1 as components
import tempfile
from pathlib import Path

def run():
        if 'uploaded_file' in st.session_state:
            uploaded_file= st.session_state['uploaded_file']
            texto= ""
            if uploaded_file is not None:
                print(uploaded_file) 
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    #st.markdown("# Original text file")
                    fp = Path(tmp_file.name)
                    fp.write_bytes(uploaded_file.getvalue())
                    #print(fp)


                with open(fp,'r') as file:
                    texto = " ".join(line for line in file)
                    print(texto)
                    
        
            #with tab2:
            #st.header('Dependencies')
            #svg= displacy.render(doc, style='dep', jupyter=False)
            #st.image(svg, width= 400, use_column_width= 'never')
            
            #with tab3:
                
            #st.header('Dependency visualizer')
            st.text_area("Annotated text", value= texto,  key= "text", height=520)
                
            
            nlp = spacy.load('es_core_news_sm')
            doc= nlp(texto)
            
            
            ent_html= displacy.render(doc, style="ent", jupyter= False)
            st.markdown(ent_html, unsafe_allow_html= True)
                