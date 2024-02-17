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
    df= pd.read_csv('file_logs.csv', usecols=['Filename', 'Status', 'Owner'])
    df= df[df['Status'] == 'Pending']
    print(df)
    options= []
    for index in df.index:
        options.append(df.loc[index, 'Filename'])

    sel= st.selectbox("Logged files", tuple(options), placeholder="Continue tagging your document")

    if option == 'Annotate':
        uploaded_file= st.file_uploader("Choose a raw file")
        
        
        texto= ''
        if uploaded_file is None:
           if 'annot_file' in st.session_state:
               uploaded_file= st.session_state['annot_file']
        else:
            st.session_state['annot_file']= uploaded_file
    
        if uploaded_file is not None:
             
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
        menu_entities+= "{title: 'Download', shortcut:'Ctrl + D', icon: 'download', onclick:function(){download();}},"
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

        leyenda= """<label for='entity-legend' style='font-size:14'> Check your document: </label>"""
        leyenda+= "<select name='entity-legend' id='leyenda' onclick='showLegend()' > "
        leyenda+= "<option selected disabled>--Select one Entity or Field-- </option>"
        for index in range(0, len(lista_entidades)):
            leyenda+="""<optgroup label='entity' style="font-size:12px;">"""
            entity= lista_entidades[index]
            leyenda= leyenda.replace('entity', entity)
            leyenda+= "<option value= 'without field' encolor='color-entidad'>without field</option>"
            leyenda= leyenda.replace('color-entidad', lista_colores[index]) 

            if entity in dict_entities.keys():
                fields= dict_entities[entity].split(':')
                
                for field in fields:
                    leyenda+= "<option value= 'pfield' encolor='color-entidad'>pfield</option>"
                    leyenda= leyenda.replace('pfield', field)
                    leyenda= leyenda.replace('color-entidad', lista_colores[index]) 

            leyenda+= "</optgroup>"
        leyenda+= "</select>"
        leyenda+= """<input class="styled" style="margin-left:10px" type= "button" value="Highlight"  onclick="highlight()" />""" 
        leyenda+= """<input class="styled" style="margin-left:5px" type= "button" value="Undo"  onclick="undo_highlight()" />""" 
        print(leyenda)   

        html_string= '''
                      
        <script src="https://jsuites.net/v4/jsuites.js"></script>
        <link rel="stylesheet" href="https://jsuites.net/v4/jsuites.css" type="text/css" />
        <link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Material+Icons">
        <script src = "https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.0/FileSaver.min.js" integrity="sha512-csNcFYJniKjJxRWRV1R7fvnXrycHP6qDR21mgz1ZP55xY5d+aHLfo9/FcGDQLfn2IfngbAHd8LdfsagcCqgTcQ==" crossorigin = "anonymous" referrerpolicy = "no-referrer"> </script>
        
        <div id='contextmenu' >
        </div>
        <script>
            
        </script>

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
           console.log(entity);
           alert(entity);
        }

        </script>

         
        <style type="text/css">

            input[type=button]{
                background-color: lightblue;
                border-radius: 8px;
                padding: 5px 10px;
                
            }
            input[type=button]:hover{
                
                box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
                cursor: pointer;
                font-size: 14px;
                background-color: #f44336;
            }
            select, option{
                background-color: lightblue;
                font-size: 14px;
                padding: 5px 10px;

            }
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
                 //max-height: 110px !important;
                 height: auto !important;
                 width: 160px !important;
                 overflow-x: hidden;
                 overflow-y: hidden;
            }
            .jcontextmenu > div:hover{
                background-color: #9ebcf7;
                cursor: pointer;
                
                color:orange;
            }
      
            
        </style>
        
        ''' + leyenda +'''<hr>

        <div  id="notepad" class="pre-wrap" >
        
            
            <p id="texto_anotacion" >''' + texto  +'''</p>
            <input type="hidden" id="actual-color" name="actual-color" value="orange" />
            <input type="hidden" id="actual-text" name="actual-text" value="" />
            <input type="hidden" id="actual-entity" name="actual-entity" value="none" />
            <input type="hidden" id="actual-field" name="actual-field" value="none" />

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

        window.localStorage.setItem("string_HTML", html);
    }
    function undo_highlight(){
    
        console.log('Undo');
        spans= document.getElementsByTagName("span");
        for (let span of spans){
            span.style.disabled= true;
            entity= span.getAttribute('entity');
            color= span.getAttribute('color');
            if (entity !=  'none')
               span.style.setProperty("background-color", color);
            if (color == 'orange')
                span.style.setProperty("background-color", color);
        }
    }
    function showLegend(){
    
        var _selected= document.getElementById("leyenda");
        console.log(_selected.selectedOptions[0]);
        color= _selected.selectedOptions[0].getAttribute('encolor');
        _selected.style.setProperty('background-color', color);
    }

    function highlight(){
    
        var _selected= document.getElementById("leyenda");
        field= _selected.selectedOptions[0].value;
        entity= _selected.selectedOptions[0].parentElement.label;
        
        if (field != 'without field'  ){
            
            spans= document.getElementsByTagName("span");
            for (let span of spans){
                span.style.disabled= true;
                span_field= span.getAttribute('field');
                span_second_field= span.getAttribute('second_field');
                
                //if (span_field !=  field)
                if ((span_field !=  field) && (span_second_field != field))
                    span.style.setProperty("background-color", "white");
            }
        }else{
            spans= document.getElementsByTagName("span");
            for (let span of spans){
                span.style.disabled= true;
                span_entity= span.getAttribute('entity');
                span_field= span.getAttribute('field');
                span_second_field= span.getAttribute('second_field');

                if (span_entity != entity)
                    span.style.setProperty("background-color", "white");

                if ((span_entity == entity) && (span_field != 'none'))
                    span.style.setProperty("background-color", "white");           
            }
        }
    }
    function removeAccents(str){
    //function removeAccents = (str) => {
        result= str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");  
        for (var i= 0; i< str.length; i++)
            if (str.charAt(i) == 'ñ')
                result= result.substring(0,i) + 'ñ' + result.substring(i+1);
            if (str.charAt(i) == 'Ñ')
                result= result.substring(0,i) + 'Ñ' + result.substring(i+1);
        return result;
    }
    function removeAll(){
        console.log('Remove all');

        last_text= document.getElementById('actual-text').value;
        spans= document.getElementsByTagName("span");
        for (let span of spans){
            
            span_text= span.textContent;
            
            if (removeAccents(span.textContent.toLowerCase()) == removeAccents(last_text.toLowerCase())){
               span.style.setProperty('background-color', "white");
                span.setAttribute('entity', 'none');
               span.setAttribute('field', 'none');
                span.setAttribute('second_field', 'none');

                span.setAttribute('second_entity', 'none');
                span.setAttribute('third_field', 'none');
                span.setAttribute('fourth_field', 'none');
            }    

            //span.parentNode.replaceChild(document.createTextNode(span_text), span);
            
        }
        spans= $("span[entity |= 'none']");
        
        $.each(spans, function(index, value){
            console.log(index);
            //console.log(value);
            parentNode= value.parentNode;
            if (removeAccents(value.textContent.toLowerCase()) == removeAccents(last_text.toLowerCase())) 
                value.replaceWith(document.createTextNode(value.textContent));

        });
    }
    function setEntity(entity, color){
    
        
        elem= document.getElementById("actual-entity");
        
        elem.setAttribute('value', entity)

        elem= document.getElementById("actual-color");
        elem.setAttribute('value', color)

        last_text= document.getElementById('actual-text').value;
        regex_word = new RegExp("\\\\b"+last_text+"\\\\b","g");
        let span= "<span style='"+color+"';>"+last_text+"</span>";
        
        spans= document.getElementsByTagName("span");

        if (toggleField)
            actual_field= document.getElementById('actual-field').value;
        else
            actual_field= 'none';

        console.log("ACTUAL ENTITY: ", entity);
        console.log("ACTUAL FIELD: ", actual_field);

        for (let span of spans){
            
            str1= span.textContent.toLowerCase();
            str2= last_text.toLowerCase();
            str1= removeAccents(str1);
            str2= removeAccents(str2);
            var entidad='';
            var campo='';

            if (str1 == str2){
                span.style.setProperty('background-color', color);
                span.setAttribute('color', color);  
                entity1= span.getAttribute('entity');
                entity2= span.getAttribute('second_entity');
                
                if (entity1 == 'none'){
                
                    span.setAttribute('entity', entity);
                    span.setAttribute('field', actual_field);
                    span.setAttribute('second_field', 'none');

                }
                else
                {
                   if (entity1 == entity){ 
                      if (field == 'none'){
                         
                         span.setAttribute('field', actual_field);
                         span.setAttribute('second_field', 'none');

                      }
                      else
                         span.setAttribute('second_field', actual_field);
                    }else
                      if (entity2 == 'none'){
                         span.setAttribute('second_entity', entity);
                         span.setAttribute('third_field', actual_field);
                         span.setAttribute('fourth_field', 'none');
                      }
                      else
                        if (entity2 == entity){
                            if (third_field == 'none'){
                                span.setAttribute('third_field', actual_field);
                                span.setAttribute('fourth_field', 'none');
                            }
                            else
                                span.setAttribute('fourth_field', actual_field);
                        }
                }
            }    
        }
        toggleField= false;
        elem= document.getElementById("actual-field");
        elem.setAttribute('value', 'none');
    }
    function setField(field){
        
        elem= document.getElementById("actual-field");
        value= elem.getAttribute("")
        elem.setAttribute('value', field);
        toggleField= true;
    }

    function clear_entities(){

        last_text= document.getElementById('actual-text').value;
        regex_word = new RegExp("\\\\b"+last_text+"\\\\b","g");
        
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
                if (txtValue != 'Remove all' && txtValue !='Reload' && txtValue != 'Download')
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
  
    function replaceAt(str, index, ch){
        return str.replace(/./g, (c, i) => i == index ? ch : c);
    }

    function auxiliar(string){
         
        string= string.toLowerCase();
        copia= string;

        const result= [];
        console.log(string.length);
        for (var i=0 ; i< string.length; i++){ 
         
            if (string[i] == 'a'){
              string= replaceAt(string, i, 'á');
              result.push(string);
            }
            if (string[i] == 'e'){
              string= replaceAt(string, i, 'é');
              result.push(string);
            }
            if (string[i] == 'i'){
              string= replaceAt(string, i, 'í');
              result.push(string);
            }
            if (string[i] == 'o'){
              string= replaceAt(string, i, 'ó');
              result.push(string);
            }
            if (string[i] == 'u'){
              string= replaceAt(string, i, 'ú');
              result.push(string);
            }
            string= copia;
        }
        return result;
    }
    
    function marcar_seleccion(){
                
        var elem;
        var actual_color;
        elem= document.getElementById('actual-color');
        actual_color= elem.value;
        elem= document.getElementById('actual-entity');
        actual_entity= elem.value;
        elem= document.getElementById('actual-field');
        actual_field= elem.value;

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
            //console.log(range);
            if (span_element.tagName == 'SPAN'){
                    
                    // <MARCADO>
                    background_color= span_element.style.getPropertyValue('background-color');  
                     
                    if (background_color == 'white'){
                    // Si no está marcada, entonces añado la entidad, color y field
                        span_element.style.setProperty('background-color', actual_color);
                        span_element.setAttribute('entity', actual_entity);
                        span_element.setAttribute('field', actual_field);
                        span_element.setAttribute('color', actual_color);

                        span_element.setAttribute('second_entity', 'none');
                        span_element.setAttribute('third_field', 'none');
                        span_element.setAttribute('fourth_field', 'none');
                    } 
                    else{
                    //Ya estaba marcada, entonces la desmarco
                        span_element.style.setProperty('background-color', 'white');
                        span_element.setAttribute('entity', 'none');
                        span_element.setAttribute('field', 'none');
                        span_element.setAttribute('second_field', 'none');
                        span_element.setAttribute('color', 'white');

                        span_element.setAttribute('second_entity', 'none');
                        span_element.setAttribute('third_field', 'none');
                        span_element.setAttribute('fourth_field', 'none');
                    }
            }
            else
            {
                    // <NO MARCADO> => <MARCAR CON 'actual-color'>
                    
                    cleared= removeAccents(cadena_texto);
                    console.log(cleared);
                    
                    //regex_word = new RegExp(cadena_texto, "gi"); // Global and Case Insensitive Match

                    
                    modificador= "[^A-Za-záéíóú]"
                    modificador= "[^áéíóú]"
                    
                    regex_word = new RegExp("\\\\b"+cleared+"\\\\b", "gi");
                    console.log("\\\\")

                    console.log('Regular Expression: ', regex_word)

                    background_color = "background-color:"+actual_color;
                    let span= "<span style='"+background_color;
                    span+= "'";
                    span+= " entity=" + "'" + actual_entity + "'";
                    span+= " field=" + "'" + actual_field + "'";
                    span+= " color=" + "'" + actual_color + "'";
                    span+= " second_field='none'" ;

                    span+= " second_entity='none'" ;
                    span+= " third_field='none'" ;
                    span+= " fourth_field='none'" ;

                    //span+= ";>"+cadena_texto+"</span>";
                    span+= ">$&</span>"; // Inserts the matched substring
                    
                    window.getSelection().anchorNode.parentElement.innerHTML =
                    window.getSelection().anchorNode.parentElement.innerHTML.replace(regex_word, span)
                    
                    //const split= window.getSelection().anchorNode.parentElement.innerHTML.split(' ')

                    console.log(cleared);
                    cleared_all_accents= auxiliar(cleared); 
                    parent= document.getElementById("texto_anotacion");
                    for (var i= 0; i< cleared_all_accents.length; i++){
                       word= cleared_all_accents[i];
                       console.log(word); 
                       
                       
                       regex_word = new RegExp("\\\\b"+word+"\\\\b", "gi"); 
                       console.log(regex_word)

                       parent.innerHTML = parent.innerHTML.replace(regex_word, span);
                    }
            }

        }
    }

    
        
    </script> '''
    
        
        
        
        col1 ,col2= st.columns([1, 4])
        with col1:
            if st.button("Save & Log File"):
                if uploaded_file:
                    owner= st.session_state['name']
                    if os.path.getsize('file_logs.csv') != 0:
                        df= pd.read_csv('file_logs.csv', usecols=['Filename', 'Status', 'Owner'])
                        df.loc[len(df.index)]= [uploaded_file.name, 'Pending', owner]
                    else:
                        df= pd.DataFrame([[uploaded_file.name, 'Pending', owner]], columns= ['Filename', 'Status', 'Owner'])
                    print(df)
                    df.to_csv('file_logs.csv', encoding= 'utf-8', index= True)
                    st.session_state['file_logs']= df
                    print('File saved')
        with col2:
           if  st.button('Clear text', help="If loaded, the press in :negative_squared_cross_mark:") and 'annot_file' in st.session_state:
               del st.session_state['annot_file']
               html_string=""

        components.html(html_string, height=1200, scrolling=True)
        
    
    