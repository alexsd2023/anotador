
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

#import utils
from utils import annotate_txt
import matplotlib.colors as mcolors
import streamlit.components.v1 as components
import tempfile
from pathlib import Path



def run():
   
    if 'entities' in st.session_state:
        print(st.session_state['entities'])

    option= 'Annotate'
    if option == 'Annotate':
        uploaded_file= st.file_uploader("Choose a file")
        texto= ''
        st.session_state['uploaded_file']= uploaded_file
    
        if uploaded_file is not None:
            #print(uploaded_file) 
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                #st.markdown("# Original text file")
                fp = Path(tmp_file.name)
                fp.write_bytes(uploaded_file.getvalue())
                #print(fp)
        
            with open(fp,'r') as file:
                texto = " ".join(line for line in file)
                #print(texto)
        
    
        tag=''
        lista_entidades= []
        lista_colores= []
        lista_campos= []
        html_fields= ''

        if 'entities' in st.session_state.keys():
            df_entidades= st.session_state['entities']
            for index in df_entidades.index:
                entidad= df_entidades.loc[index, 'Entity-Name']

                if not df_entidades.isnull().loc[index, 'Field-Name']:
                    campo= df_entidades.loc[index, 'Field-Name']
                    entities_fields= '''<input type="hidden" name="'''+entidad
                    entities_fields+='''" value="''' +campo
                    entities_fields+= '''" />'''
                    html_fields+= entities_fields
                    html_fields+='\n'

     
        if 'entities_colors' in st.session_state.keys():    
            df_colores= st.session_state['entities_colors']
            print(df_colores)
            for index in df_colores.index:
                color= df_colores.loc[index, 'Color']
                entidad=df_colores.loc[index, 'Entity-Name']
                lista_entidades.append(entidad)
                lista_colores.append(color)

        

        menu_options= ""
        menu_entities= ""
        colors_rect=""

        for i in range(0, len(lista_entidades)):
            menu_str= "<option value="+ lista_entidades[i]+ ">"+lista_entidades[i]+"</option> "
            menu_options+= menu_str
            
            menu_str_1= "<div class='item' style= 'background' onclick=getEntity(this,'value','color')>"+ lista_entidades[i]+ "</div> "
            menu_str_1= menu_str_1.replace('value', lista_entidades[i])
            menu_str_1= menu_str_1.replace('color', lista_colores[i])

            menu_str_1= menu_str_1.replace('background', 'background-color: '+lista_colores[i])
            menu_entities+= menu_str_1
            
        html_string= html_fields
        html_string+= '''
        
        <div id="context-menu">
                <div>
                    <input type="text" placeholder="Search an entity" id="search" onkeyup="filterFunction()">
                </div>
                
                <div id="sidebar">
                    <div title= "Entidades"> '''+ menu_entities + '''
                    </div>
                    <div  id="fields">Fields 
                        
                    </div>
                </div>
                <hr/>
                <div>
                    <input type="checkbox" id= "clear-checkbox" name="clear-checkbox" value="Clear all" onclick="clear_entities()" align= "center">
                    <label for="clear-checkbox"> Clear all </label><br>
                </div>
                
        
        </div>
        
    
        <style type="text/css">

            
            #search {
            box-sizing: border-box;
            width: 100% ;
            height: 20px;
            background-repeat: no-repeat;
            font-size: 1.0rem;
            padding: 1px;
            
            border: none;
            border-bottom: 3px solid #ddd;
            }
            #sidebar{
            margin: 4px, 4px;
            padding: 4px;
            width:100%;
            height: 8em;
            overflow-x: hidden;
            overflow-y: auto;
            text-align: justify;
            
            
            }
            
            #context-menu{
                
                background-color: #ffffff;
                box-shadow: 0 0 40px rgba(37, 40, 42, 0.22);
                color: #1f194c;
                width:25em;
                padding: 0.8em 0.6em;
                font-size: 1.0rem;
                position: fixed;
                visibility: hidden;
            
            }
        
            .item{
                padding: 0.3em 1.2em;
                width: 50%;
                white-space: nowrap;
                float: inline-start;
                margin-right: 30px;
            }
            .field{
                padding: 0.4em 1.2em;
                width: 30%;
                white-space: nowrap;
                float: initial;
                
                
            }
            .field:hover{
                background-color: orange;
                cursor: pointer;
                font-weight:bold;
            }
            .item:hover{
            
                background-color: orange;
                cursor: pointer;
                font-weight:bold;
            }
            
            menu:hover{
                background-color: rgba(44, 141, 247, 0.2);
                cursor: pointer;
                font-weight:bold;
            }
            menu:hover > menu{
                display:block;
            }
            menu > menu{
                display:none;
                position:relative;
                top:-20px;
                left:100%;
                width:150px;
            }
            menu[title]:before{
                content:attr(title);
            }
            menu:not([title]):before{
                content:"\2630";
            }
            
            .break-spaces {
            white-space: break-spaces;
            }

            .pre-wrap {
            white-space: pre-wrap;
            }
        </style>
        
            
        <div  id="notepad" class="pre-wrap" >
        
            
            <p id="texto_anotacion" >''' + texto  +'''</p>
            <input type="hidden" id="actual-color" name="actual-color" value="grey" />
            <input type="hidden" id="last-text" name="last-text" value="" />
            <input type="hidden" id="last-entity" name="actual-entity" value="" />

            <input type="hidden" id="last-startIndex" name="last-startIndex" value="" />
            <input type="hidden" id="last-endIndex" name="last-endIndex" value="" />
            
        </div>

    <script>
    /* When the user clicks on the button,
    toggle between hiding and showing the dropdown content */
    function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
    }

    function clear_entities(){

        last_text= document.getElementById('last-text').value;
        regex_word = new RegExp(last_text,"g");
        
        spans= document.getElementsByTagName("span");
        for (let span of spans){
            console.log(span.style.getPropertyValue('background-color'));
            if (span.textContent == last_text)
                span.style.setProperty('background-color', '#FFFFFF');
        }
    
    }
    function filterFunction() {

        //Resetear la lista de fields
        fieldsNode= document.getElementById("fields");
        while (fieldsNode.firstChild){
            fieldsNode.removeChild(fieldsNode.lastChild);
        }

        items= document.getElementsByClassName("item");
        input = document.getElementById("search");
        filter = input.value.toUpperCase();

        for (let item of items){
            
        console.log(item);
        console.log(item.textContent);
        txtValue= item.textContent;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
                item.style.display = "";
                
            } else {
                item.style.display = "none";
            }
        }
    /* var input, filter, ul, li, a, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdown");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
        txtValue = a[i].textContent || a[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
        } else {
        a[i].style.display = "none";
        }
    }
    */
    }
    </script>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>    

    <script> 
        
    var elem;
    elem= document.getElementById("texto_anotacion");
    document.addEventListener('dblclick', function(event){
        alert("Double click disabled!");
        event.preventDefault();
        event.stopPropagation();
    }, true);

    //elem.ondblclick= marcar_seleccion;

    elem.onmouseup= marcar_seleccion;
    //console.log(elem);

    function getOptionEntity(){
    console.log("Selección de Entidad");
    }

    var notepad = document.getElementById("notepad");
        
    var menuState = 0;
    var contextMenuActive = "block";
    var ctxMenu = document.getElementById("context-menu");
    notepad.addEventListener("contextmenu",function(event){
            event.preventDefault();
            toggleMenuOn(event);
        },false);
            
    notepad.addEventListener("click",function(event){
                
        toggleMenuOff();
                
        },false);
            
    // Turns the custom context menu on.
    function toggleMenuOn(event) {
    if (menuState !== 1) {
        menuState = 1;
        ctxMenu.style.visibility = "visible";
        ctxMenu.style.left = (event.clientX - 10)+"px";
        ctxMenu.style.top = (event.clientY - 10)+"px";
        
        document.getElementById("clear-checkbox").checked= false;
        
    }
    }     
        
    // Turns the custom context menu off.
    function toggleMenuOff() {
    if (menuState !== 0) {
        menuState = 0;
        ctxMenu.style.visibility = "hidden";
        ctxMenu.style.left = "";
        ctxMenu.style.top = "";
        document.getElementById("clear-checkbox").checked= false;
    }
    }      
        
    //Contextual Menú    
    //FUNCION QUE GENERA EL LOG DE MARCADO

    function getEntity(element, entity_name, color){

    //Get fields
    let elements= document.getElementsByName(entity_name);
    

    //Delete all previous fields
    fieldsNode= document.getElementById("fields");
    while (fieldsNode.firstChild){
            fieldsNode.removeChild(fieldsNode.lastChild);
    }
    //Add new fields
    for (let elem of elements){
        field_of_entity= elem.value;
        tag= '<div class="field">' +field_of_entity+ '</div>';
        fieldsNode.innerHTML+= tag ;
    }

    
    elem_color= document.getElementById('actual-color');
    elem_color.setAttribute('value', color);

    elem_last_entity= document.getElementById('last-entity');
    elem_last_entity.setAttribute('value', entity_name);
    
    last_text= document.getElementById('last-text').value;
    last_startIndex= document.getElementById('last-startIndex').value;
    last_endIndex= document.getElementById('last-endIndex').value;
    
    console.log('Entity name: ', entity_name, 'startIndex: ', last_startIndex, 'endIndex: ', last_endIndex, 'String: ', last_text, ' True');

    regex_word = new RegExp(last_text,"g");
    let span= "<span style='"+color+"';>"+last_text+"</span>";
    //console.log(document.getElementById('text'));
    
    spans= document.getElementsByTagName("span");
    for (let span of spans){
        //console.log(span.style.getPropertyValue('background-color'));
        if (span.textContent == last_text)
            span.style.setProperty('background-color', color);
    }
    
    //document.getElementById('text').innerHTML =
    //document.getElementById('text').innerHTML.replace(regex_word, span);
    }


    // FUNCION QUE HACE EL MARCADO VISUAL

    function marcar_seleccion(){
                
        var elem;
        var actual_color;
        var marcada= false;
    
        elem= document.getElementById('actual-color');
        actual_color= elem.value;

        elem= document.getElementById('last-entity');
        last_entity= elem.value;

        //console.log('Color actual: ', actual_color);
        
        
        // ** Obtener String, Posicion Inicio y Fin
        selection= window.getSelection();
        
        var element= document.getElementById("texto_anotacion");
        var textNode= element.childNodes[0];
        
        console.log('Anchor Offset: ', selection.anchorOffset);
        
        var range= selection.getRangeAt(0);  
        //clone= range.cloneRange();   
        //***********
        
        startIndex= range.startOffset;
        endIndex= range.endOffset;

        //**********    

        cadena_texto= selection.toString();

        //console.log('Start Index: ', startIndex);
        //console.log('End Index: ', endIndex);
        //console.log('Cadena de texto: ', selection.toString());
                
        //Check if marked
        
        elem=  window.getSelection().anchorNode.parentElement;
        //var marcada= false;
        //console.log(elem.style.cssText);
        background_color= elem.style.getPropertyValue('background-color');
        if (background_color != '')
            console.log('Background Color: ', background_color);

        if (background_color != actual_color){
            background_color = "background-color:"+actual_color;
            console.log('MARCANDO SELECCION: ', background_color);
            //marcada= true;

            if (last_entity != '' && cadena_texto != '')
                console.log('Entity name: ', last_entity, 'startIndex: ', startIndex, 'endIndex: ', endIndex, 'String: ', cadena_texto, ' True');

        }else{
        //Color Blanco
        background_color = "background-color:white";
        console.log("DESMARCAR SELECCION: ", background_color);
        console.log('Entity name: ', last_entity, 'startIndex: ', startIndex, 'endIndex: ', endIndex, 'String: ', cadena_texto, ' False');
                
        }
        
    
        //Change Word Color
        //Expresión regular, Exact Match
        regex_word = new RegExp(window.getSelection().toString(),"g");
        texto_seleccionado= window.getSelection().toString();
        
        if (texto_seleccionado != ''){
            let span= "<span style='"+background_color+"';>"+window.getSelection().toString()+"</span>";
            window.getSelection().anchorNode.parentElement.innerHTML =
            window.getSelection().anchorNode.parentElement.innerHTML.replace(regex_word, span);
            

            //Almacenar la selección: String, startIndex, endIndex
            elem_selection= document.getElementById('last-text');
            elem_selection.setAttribute('value', texto_seleccionado);

            elem_selection= document.getElementById('last-startIndex');
            elem_selection.setAttribute('value', startIndex);

            elem_selection= document.getElementById('last-endIndex');
            elem_selection.setAttribute('value', endIndex);
                
        }
        
    }
        
        
    </script>
    
        '''
        
        #st.markdown(content, unsafe_allow_html= True)
        components.html(html_string, height=600, scrolling=True)
        
        
       
        #entidades= st.session_state['user_entities']
        #colores= st.session_state['entities_color']
        #descripciones= st.session_state['entities_description']

        #list_entities= entidades.split(';')
        #list_colors= colores.split(';')
        #list_descripciones= descripciones.split(';')
        
        #entity= st.selectbox('Select your entity:', tuple(entidades.split(';')))
        #index= list_entities.index(entity)
        #st.session_state['last_color']= list_colors[index]
        
        #st.write(list_colors[index])
        #html=''' Color:  <div id='rectangle' style="width:25px; height:25px; background:
        #''' + list_colors[index] + ''' "></div><hr>'''
        
        #st.markdown(html, unsafe_allow_html= True)
        #st.write('Description: ')
        #st.write(list_descripciones[index])
        
        st.button("Save Annotations")
    
    