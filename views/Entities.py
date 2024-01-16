#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from PIL import Image
import glob
import os

from annotated_text import annotated_text
from st_click_detector import click_detector
from bs4 import BeautifulSoup
from utils import annotate_txt
import matplotlib.colors as mcolors


def run():    
   
    
    st.title("Setup")
    tab1, tab2, tab3= st.tabs(["Entities/Fields", "Assign Color", "Colours Table"])
    colors = {
                        'name': mcolors.CSS4_COLORS.keys(),
                        'hex': mcolors.CSS4_COLORS.values()
            }
                
    with tab1:            
                annotation_file= st.file_uploader("Choose an annotation file", type={"csv"}, key="annotation_file")
                
                data= []
                flag= False
                edited_df= None
                with st.container(border= True):
                    
                        
                    if  annotation_file is not None:
                        df = pd.read_csv(annotation_file, index_col= False)
                        df= df[['Entity-Name', 'Field-Name']]
                        df['Description']=""
                        df["Color"]= ""
                            
                        df= df.sort_values(by='Entity-Name', ignore_index= True)
                        df['ID']= list(range(1, df.shape[0]+1))
                        df_entities= df.reindex(columns=['ID', 'Entity-Name', 'Field-Name', 'Description', 'Color'])
                        edited_df= st.data_editor(df_entities, use_container_width=True, num_rows="dynamic", \
                                                column_order=('Entity-Name', 'Field-Name', 'Description'), hide_index= True)
                         
                    else:
                          
                        #edited_df= st.data_editor(df, use_container_width=True, num_rows="dynamic")
                        #st.write(edited_df)
                    
                        if not 'entities' in st.session_state:
                            
                            df= pd.DataFrame([['<entity>', '<field>', '<description>', '']], columns=('Entity-Name', 'Field-Name', 'Description', 'Color') ) 
                            st.session_state['entities']= df
                        
                        edited_df = st.data_editor(st.session_state['entities'], num_rows="dynamic", hide_index= True, column_order=('Entity-Name', 'Field-Name', 'Description'),use_container_width=True)
                        
                        #favorite_command = edited_df.loc[edited_df["Field-Name"].idxmax()]["Entity-Name"]
                        #st.markdown(f"Your favorite command is **{favorite_command}** 🎈")

                    if st.button("Save", key='save_entities'):
                        #st.runtime.legacy_caching.clear_cache()
                        print('Saving entities')
                        #print(edited_df)
                        st.session_state['entities']= edited_df
                        
                            
                with tab2:
                    
                    entity_color_file= st.file_uploader('Choose pairwise entity-color information', type={"csv"})
                    edited_df= None
                    if "entities_colors" in st.session_state:
                                
                        with st.container(border= True): 
                            edited_df= st.data_editor(st.session_state['entities_colors'], use_container_width=True, num_rows="dynamic")

                    elif entity_color_file is not None:
                        df= pd.read_csv(entity_color_file, index_col= False)
                        df= df[['Entity-Name', 'Color']]
                        df['Hex']=''
                        df['Background']= ''

                        df_colors = pd.DataFrame(colors)
                        df_colors['rgb'] = df_colors['hex'].apply(mcolors.hex2color)
                        
                        colors_dict= {}
                        for index in df.index:
                            if not pd.isnull(df.loc[index, 'Color']):
                                color_name= df.loc[index, 'Color']
                            else:
                                color_name =''
                            if color_name != '':
                                color_hex= df_colors.loc[df_colors['name'] == color_name]['hex']
                                color_hex= color_hex.values[0]
                            else:
                                color_hex= None        
                            df.loc[index, 'Hex']= color_hex

                        edited_df= df.copy()    
                        styled_df= df.style.apply(annotate_txt.format_color_groups, color=df['Hex'],  axis=None)
                        
                        with st.container(border= True):
                            st.table(styled_df)
                        

                    elif 'entities' in st.session_state:
                        df= st.session_state['entities']
                        df= df[['Entity-Name', 'Color']]
                        df_entities= df.drop_duplicates()
                        df_entities.reset_index(drop=True, inplace=True)
                        if 'colors' in st.session_state.keys():
                            color_options= st.session_state['colors']
                            color_options=  color_options['name']
                        else:
                            color_options= []

                        with st.container(border= True): 
                            edited_df= st.data_editor(df_entities, num_rows="dynamic", use_container_width=True, column_config= {"Color": st.column_config.SelectboxColumn("Color", options= color_options, required= True)})
                            
                        
                    else:
                        df= pd.DataFrame([['<entity-name>', '<color>']], columns=('Entity-Name',  'Color') ) 
                        edited_df= st.data_editor(df, use_container_width=True)

                    if st.button("Save", key="save_entities_color"):
                        
                        print('Saving entities and colors')
                        #print(edited_df)
                        st.session_state['entities_colors']= edited_df
                        #st.runtime.legacy_caching.clear_cache()

                    

                with tab3:
                        
                        
                        df_colors = pd.DataFrame(colors)
                        df_colors['rgb'] = df_colors['hex'].apply(mcolors.hex2color)

                        df_colors['rgb'] = df_colors['rgb'].apply(lambda x:[round(c, 5) for c in x])
                        df_colors['Background'] = ''
                        df_colors= df_colors[['name', 'hex', 'Background']]
                        #print(df_colors.hex)
                        styled_df= df_colors.style.apply(annotate_txt.format_color_groups, color=df_colors.hex,  axis=None)
                        with st.container(border= True):
                            st.table(styled_df)
                        st.session_state['colors']= df_colors
                        
                    

