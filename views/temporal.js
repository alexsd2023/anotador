/*
        var range= selection.getRangeAt(0); 
        var parent= range.startContainer;
        var copy= range.cloneContents();
        nodes= copy.childNodes;
        flag= false;
        color= 'orange';

        for (i=0; i< nodes.length; i++)
            if (nodes[i] instanceof HTMLSpanElement){
               flag= true;
               if (nodes[i].style.getPropertyValue('background-color') == 'orange')
                 color= 'white';
               else
                  color= 'orange';

            }
        if (cadena_texto != ''){
            var selectedText= range.extractContents();
            var span= document.createElement("span");
            span.style.setProperty('background-color', color);
            span.appendChild(selectedText);
            range.insertNode(span);

            if (flag)
                span.parentNode.remove;   
            var abc= span.cloneNode(true);
            span.parentElement.parentElement.insertBefore(abc, span.parentElement);
            span.parentNode.remove();
        }

        let span= document.createElement("span")
        span.style.setProperty('background-color', 'orange');
        range.surroundContents(span);
        
        if (parent.tagName == 'SPAN'){ 
            bkcolor= parent.style.getPropertyValue('background-color');
            if (bkcolor == 'white')
                parent.style.setProperty('background-color', actual_color);
            else{
                parent.style.setProperty('background-color', 'white');
                bkcolor= 'white';
            }
        }
        else
           bkcolor='';

       
        startIndex= range.startOffset;
        endIndex= range.endOffset;
        
        if (cadena_texto != '' && bkcolor == ''){
        
            regex_word = new RegExp(cadena_texto, "g");
            background_color = "background-color:"+actual_color
            let span= "<span style='"+background_color+"';>"+window.getSelection().toString()+"</span>";
            window.getSelection().anchorNode.parentElement.innerHTML =
            window.getSelection().anchorNode.parentElement.innerHTML.replace(regex_word, span);
            
            //Almacenar la selección: String, startIndex, endIndex
            elem_selection= document.getElementById('actual-text');
            elem_selection.setAttribute('value', cadena_texto);

            elem_selection= document.getElementById('last-startIndex');
            elem_selection.setAttribute('value', startIndex);

            elem_selection= document.getElementById('last-endIndex');
            elem_selection.setAttribute('value', endIndex);
                
        }
        
        */