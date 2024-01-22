
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
    if not 'entities_colors' in st.session_state:
       st.info('You must add entities!')


    option= 'Annotate'
    if option == 'Annotate':
        uploaded_file= st.file_uploader("Choose a file")
        texto= ''
        if uploaded_file is None:
           if 'annot_file' in st.session_state:
               uploaded_file= st.session_state['annot_file']
        else:
            st.session_state['annot_file']= uploaded_file
    
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

        dict_entities= {}
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

                    if entidad in dict_entities.keys():
                        dict_entities[entidad]+=':'
                        dict_entities[entidad]+=campo 
                    else:
                        dict_entities[entidad]= campo
        print(dict_entities)

        if 'entities_colors' in st.session_state.keys():    
            df_colores= st.session_state['entities_colors']
            #print(df_colores)
            for index in df_colores.index:
                color= df_colores.loc[index, 'Color']
                entidad=df_colores.loc[index, 'Entity-Name']
                lista_entidades.append(entidad)
                lista_colores.append(color)

        

        menu_options= ""
        menu_entities= ""
        colors_rect=""
        #print(lista_entidades)
        #lista_entidades= ['A', 'B']
        
        menu_entities= "{title: 'Remove all', icon: 'delete', shortcut:'Ctrl + A',  onclick:function(){removeAll();}},"
        menu_entities+= "{title: 'Reload', icon: 'refresh', shortcut: 'Ctrl +  R', onclick:function(){reload();}},"
        menu_entities+= "{title: 'Download ', shortcut:'Ctrl + D', icon: 'download', onclick:function(){download();}},"
        menu_entities+= "{type: 'line'},"

        for i in range(0, len(lista_entidades)):
            menu_entities+= "{title:'"
            menu_entities+= lista_entidades[i]
            menu_entities+= "'"
            strFunc=  ", onclick:function() { setEntity('param1', 'param2');}".replace("param1", lista_entidades[i])
            strFunc=  strFunc.replace("param2", lista_colores[i])
            menu_entities+= strFunc
                                
            if lista_entidades[i] in dict_entities.keys():
                fields= dict_entities[lista_entidades[i]].split(':')
                #print(fields)
                menu_entities+= ", submenu: ["
                for index, field in enumerate(fields):
                    menu_entities+= "{title:'"
                    menu_entities+= field
                    menu_entities+= "', "
                    strFunc=  "onclick:function() { setField('param');}".replace("param", field)
                    print(strFunc)
                    menu_entities+= strFunc
                    if index == len(fields)-1:
                        menu_entities+= "}"
                    else:
                        menu_entities+= "},"
                
                menu_entities+= "],"
            
            menu_entities+= "},"
            
        

        print(menu_entities)
        html_string= '''
        
                        
        <script src="https://jsuites.net/v4/jsuites.js"></script>
        <link rel="stylesheet" href="https://jsuites.net/v4/jsuites.css" type="text/css" />
        <link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Material+Icons">
        <script src = "https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.0/FileSaver.min.js" integrity="sha512-csNcFYJniKjJxRWRV1R7fvnXrycHP6qDR21mgz1ZP55xY5d+aHLfo9/FcGDQLfn2IfngbAHd8LdfsagcCqgTcQ==" crossorigin = "anonymous" referrerpolicy = "no-referrer"> </script>
        
        <div id='contextmenu' >
        </div>
        

        <script>
        
        var contextMenu = jSuites.contextmenu(document.getElementById('contextmenu'), {
            items:['''+menu_entities+'''],
             onclick:function() {
                if ( document.getElementById('search') != document.activeElement)
                    contextMenu.close(false);
                
            }
        });
        
        var menu= document.getElementById("contextmenu");
        
        menu.addEventListener("load", myFunction);
        function myFunction(){
            console.log("menu contextual cargado")
        }

        function select_entity(entity){
           alert(entity);
        }

        </script>

         
        <style type="text/css">

            .center-block{
                margin: auto;
                display: block;
            }
            .break-spaces {
            white-space: break-spaces;
            }

            .pre-wrap {
            white-space: pre-wrap;
            }

            .jcontextmenu > div{
            font-size: 13px;
            
            }
            .jcontexthassubmenu > div{
                 padding: 2% !important;
                 max-height: 110px !important;
                 height: auto !important;
                 width: 160px !important;
                 overflow-x: hidden;
                 overflow-y: auto;
            }
            .jcontextmenu > div:hover{
                background-color: #9ebcf7;
                cursor: pointer;
                
                color:orange;
            }
      
            
        </style>
        
            
        <div  id="notepad" class="pre-wrap" >
        
            
            <p id="texto_anotacion" >''' + texto  +'''</p>
            <input type="hidden" id="actual-color" name="actual-color" value="orange" />
            <input type="hidden" id="actual-text" name="actual-text" value="" />
            <input type="hidden" id="actual-entity" name="actual-entity" value="" />
            <input type="hidden" id="actual-field" name="actual-field" value="" />

            <input type="hidden" id="last-startIndex" name="last-startIndex" value="" />
            <input type="hidden" id="last-endIndex" name="last-endIndex" value="" />
            
        </div>

    <script>
    /* When the user clicks on the button,
    toggle between hiding and showing the dropdown content */
    function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
    }
    var toggleField= false;

    function reload(){
      let string_HTML= window.localStorage.getItem("string_HTML");
      result= document.getElementById("texto_anotacion");
      result.innerHTML= string_HTML
    }
    function download(){
        result= document.getElementById("texto_anotacion");
        html= result.innerHTML;
        console.log(html);
        var blob= new Blob([result.innerHTML], {type:'text/html'});
        saveAs(blob, 'result.html');

        window.localStorage.setItem("string_HTML", html)
    }

    function removeAll(){
        console.log('Remove all');

        last_text= document.getElementById('actual-text').value;
        spans= document.getElementsByTagName("span");
        for (let span of spans){
            
            //console.log(span.style.getPropertyValue('background-color'));
            if (span.textContent == last_text){
                span.style.setProperty('background-color', "white");
                span.style.setProperty('entity', '');
                span.style.setProperty('field', '');
            }    
        }
    }
    function setEntity(entity, color){
    
        console.log(entity, ':', color);
        elem= document.getElementById("actual-entity");
        elem.setAttribute('value', entity)

        elem= document.getElementById("actual-color");
        elem.setAttribute('value', color)

        last_text= document.getElementById('actual-text').value;
        regex_word = new RegExp(last_text,"g");
        let span= "<span style='"+color+"';>"+last_text+"</span>";
        //console.log(document.getElementById('text'));
        
        spans= document.getElementsByTagName("span");
        for (let span of spans){
            
            //console.log(span.style.getPropertyValue('background-color'));
            if (span.textContent == last_text){
                span.style.setProperty('background-color', color);
                span.setAttribute('entity', entity);
                if (toggleField){
                   actual_field= document.getElementById('actual-field').value;
                   span.setAttribute('field', actual_field);
                   
                }else
                    span.setAttribute('field', '');
            }    
        }
        toggleField= false;
    }
    function setField(field){
        //console.log(field);
        elem= document.getElementById("actual-field");
        elem.setAttribute('value', field);
        toggleField= true;
    }

    function clear_entities(){

        last_text= document.getElementById('actual-text').value;
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
        //fieldsNode= document.getElementById("fields");
        //while (fieldsNode.firstChild){
        //    fieldsNode.removeChild(fieldsNode.lastChild);
        //}

        elem_menu= document.getElementById("contextmenu");
        items= elem_menu.childNodes;
        
        input = document.getElementById("search");
        filter = input.value.toUpperCase();

        for (let item of items){
            if (item.tagName == "DIV" &&  !(item.className == "header")){
                option= item.getElementsByTagName("a");
                console.log(option[0].textContent);
            
                txtValue= option[0].textContent;
                if (txtValue != 'Remove all')
                    if (txtValue.toUpperCase().indexOf(filter) > -1) 
                        item.style.display = "";
                    else 
                        item.style.display = "none";
            }
               
        }
    
    }
    </script>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js">
    
        
    </script>    

    <script> 
        
    var elem;
    elem= document.getElementById("texto_anotacion");
    notepad= document.getElementById("notepad");
    notepad.addEventListener("load", (event)=>{
        console.log('Cargado el TEXTO');
    });

    document.addEventListener('dblclick', function(event){
        
        event.preventDefault();
        event.stopPropagation();
    }, true);

    //elem.ondblclick= marcar_seleccion;
    elem.onmouseup= marcar_seleccion;
    

    function getOptionEntity(){
    console.log("Selección de Entidad");
    }

    var notepad = document.getElementById("notepad");   
    var contextMenuActive = "block";

    notepad.addEventListener("contextmenu", function(e) {
   
        //DESHABILITAR PARA EL DEBUGGER
        contextMenu.open(e);
        e.preventDefault();

        console.log('Menu Abierto');
        menu= document.getElementById("contextmenu");

        let input= document.getElementById("search");
        if (input == null) {
            //<input type="text" placeholder="Search an entity" id="search" onkeyup="filterFunction()">
            let input= document.createElement("input");
            input.type= "text";
            input.placeholder= "Search an entity";
            input.id="search";
            input.className= "center-block";
            input.setAttribute("onkeyup", "filterFunction()");

            menu.prepend(input);
        }
    });
 
    // FUNCION QUE HACE EL MARCADO VISUAL
  
    function marcar_seleccion(){
                
        var elem;
        var actual_color;
        
        elem= document.getElementById('actual-color');
        actual_color= elem.value;
        elem= document.getElementById('actual-entity');
        last_entity= elem.value;

        elem= document.getElementById('actual-field');
        last_field= elem.value;

        selection= window.getSelection();
        cadena_texto= selection.toString();
        if (cadena_texto != ''){

            elem_actual_text= document.getElementById('actual-text');
            elem_actual_text.setAttribute('value', cadena_texto); 

            console.log('Cadena de texto: ', cadena_texto);
            range= selection.getRangeAt(0);
            focus_node= selection.focusNode;
            span_element= focus_node.parentElement;
            console.log(span_element);
            
            console.log(range);
            if (span_element.tagName == 'SPAN'){
                    
                    // <MARCADO>
                    background_color= span_element.style.getPropertyValue('background-color');   
                    if (background_color == 'white'){
                        span_element.style.setProperty('background-color', actual_color);
                    } 
                    else{
                        span_element.style.setProperty('background-color', 'white');
                    } 
                    /*
                    if (background_color != 'orange'){
                        // <MARCADO DE ALGUNA ENTITY>  => <CAMBIAR ENTITY>
                        span_element.remove();
                        var span= document.createElement("span");
                        span.style.setProperty('background-color', actual_color);
                        span.style.setProperty('entity', last_entity);
                        span.style.setProperty('field', last_field);

                        span.appendChild(document.createTextNode(cadena_texto));
                        range.insertNode(span);
                    }else{
                       // <MARCADO CON 'defaul-color'> => <DESMARCAR> 
                        //selection.removeRange(range);
                        span_element.style.setProperty('background-color', 'white');

                    }
                    */    
          
            }else{
                    // <NO MARCADO> => <MARCAR CON 'actual-color'>
                    regex_word = new RegExp(cadena_texto, "g");
                    background_color = "background-color:"+actual_color;
                    let span= "<span style='"+background_color;
                    span+= "'";
                    span+= " entity=" + "'" + last_entity + "'";
                    span+= " field=" + "'" + last_field + "'";

                    span+= ";>"+cadena_texto+"</span>";
                    console.log(span);
                    window.getSelection().anchorNode.parentElement.innerHTML =
                    window.getSelection().anchorNode.parentElement.innerHTML.replace(regex_word, span)
                    
                    
            }

        }
    }
        
        
    </script>
    
        '''
        
        components.html(html_string, height=800, scrolling=True)
        
        if st.button("Log File Status"):
            if uploaded_file:
                if os.path.getsize('file_logs.csv') != 0:
                    df= pd.read_csv('file_logs.csv', usecols=['Filename', 'Status'])
                    df.loc[len(df.index)]= [uploaded_file.name, 'Pending']
                else:
                    df= pd.DataFrame([[uploaded_file.name, 'Pending']], columns= ['Filename', 'Status'])
                print(df)
                df.to_csv('file_logs.csv', encoding= 'utf-8', index= True)
                st.session_state['file_logs']= df
                print('File saved')
        
    
    