import streamlit as st
import pandas as pd
import tempfile
from bs4 import BeautifulSoup
from pathlib import Path
import streamlit.components.v1 as components
from utils import annotate_txt
import matplotlib.colors as mcolors

def run():
    html_file= st.file_uploader("Choose an annotation file", type={"html"}, key="review-file")

    if not html_file:
     if 'statistics' in st.session_state:
        html_file= st.session_state['statistics']

    if html_file:
        with st.container(border= True):
            col1, col2= st.columns([0.7, 0.3])
            spans= []

            colors = {
                                'name': mcolors.CSS4_COLORS.keys(),
                                'hex': mcolors.CSS4_COLORS.values()
                    }
            df_colors = pd.DataFrame(colors)
            df_colors['rgb'] = df_colors['hex'].apply(mcolors.hex2color)
            
            with col1:
                
                    st.session_state['statistics']= html_file
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                            #st.markdown("# Original text file")
                            fp = Path(tmp_file.name)
                            fp.write_bytes(html_file.getvalue())
                        
                    with open(fp,'r') as file:
                            html_string= file.read()
                            
                            html_string= """<style type="text/css"> 
                                                .pre-wrap {
                                                        white-space: pre-wrap;
                                                }</style>
                                                <div  id="notepad" class="pre-wrap" >
                                                    <p id="texto_anotacion" >""" + html_string  +"""</p>
                                                </div>"""

                            components.html(html_string, height=600, scrolling=True)
                            soup= BeautifulSoup(html_string, 'html.parser')
                            #plain_text= soup.get_text('\n')
                            #lines= plain_text.split('\n')
                            spans= soup.find_all('span')
                            
                            #head= soup.find("head")
                            #tag= soup.new_tag("script", src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js")
                            #str= """$('span').on('click', function(){console.log("hola");});"""
                            #tag.append(str)
                            #head.insert_after(tag)
                            
                            
                            
            with col2:
                
                    entities= []
                    fields= []
                    colors= []
                    stats= {}
                    stats_fields= {}

                    for span in spans:
                        entity= span['entity']
                        field= span['field']
                        color= span['style'].split(':')[1]
                        color= color.replace(';','')
                        color= color.lstrip()
                        
                        if field != '':
                            key=entity+'.'+field
                            if not key in stats_fields.keys():
                                stats_fields[key]= 1
                            else:          
                                stats_fields[key]+= 1
                            
                        if not entity in entities:
                            entities.append(entity)
                            colors.append(color)
                        if entity in stats.keys():
                            stats[entity]= stats[entity] + 1
                        else:
                            stats[entity]= 1
                    data= []
                    for key in stats.keys():
                        data.append([key, stats[key], colors[entities.index(key)], '', ''])

                    df=  pd.DataFrame(data, columns=('Entity', 'Total', 'Color', 'Hex', 'Background'))
                    df['Hex']= ''
                    df['Background']= ''
                    for index in df.index:
                        if not pd.isnull(df.loc[index, 'Color']):
                            color_name= df.loc[index, 'Color']
                            color_hex= df_colors.loc[df_colors['name'] == color_name]['hex']
                            color_hex= color_hex.values[0]
                            df.loc[index, 'Hex']= color_hex
                        else:
                            color_hex= None        
                    edited_df= df.copy()
                    edited_df= df[['Entity', 'Total', 'Background']]   
                    edited_df.reset_index(drop=True, inplace=True)    
                    styled_df= edited_df.style.apply(annotate_txt.format_color_stats, color=df['Hex'],  axis=None)
                    
                    if len(stats) > 0:
                        st.table(styled_df)
                        #st.dataframe(edited_df)  

                    data= []
                    for key in stats_fields.keys():
                        data.append([key, stats_fields[key]])
                    if len(data) > 0:
                        st.dataframe(pd.DataFrame(data, columns=('Entity.Field', 'Total')))               

