import streamlit as st
import pandas as pd

def run():
    uploaded_files= st.file_uploader("Choose a txt/html file", accept_multiple_files= True)
    df= None
    
    if uploaded_files:
        data= []
        owner= st.session_state['name']
        for uploaded_file in uploaded_files:
            
            data.append([uploaded_file.name, uploaded_file.type, uploaded_file.size, owner, 'Pending'])
            df= pd.DataFrame(data, columns=('Filename', 'Type', 'Size', 'Owner', 'Status') )
    else:
        df= pd.read_csv('file_logs.csv', usecols=['Filename', 'Status', 'Owner'])

    with st.container(border= True):    
        
        edited_df= st.data_editor(df, use_container_width=True,column_config={"Status": st.column_config.SelectboxColumn("Status", options=['Completed', 'Pending', 'Raw'], required=True)})
        if st.button("Save", key="save_file_logs"):
            st.session_state['file_logs']= edited_df
            edited_df.to_csv('file_logs.csv')