#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import base64
from streamlit_option_menu import option_menu
from views import Entities, Annotate, ViewAnnotations, NER, FileLogs, Anotar, Statistics, Users
#from streamlit_extras.app_logo import add_logo
import streamlit_authenticator as stauth
import pickle
st.set_page_config(layout="centered", page_title="Annotation Tool",  menu_items={'About':"Lancaster Annotation Tool. All copyrights reserved"})

#add_logo("https://www.lancaster.ac.uk/media/wdp/style-assets/images/logos/lu-logo.svg")
with st.sidebar:
    #st.image("https://www.lancaster.ac.uk/media/wdp/style-assets/images/logos/lu-logo.svg", width=150)
    st.image("./logo.png", width=150)
    
import yaml
from yaml.loader import SafeLoader

with open('credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)
name, authentication_status, username= authenticator.login()

#def get_base64(bin_file):
#    with open(bin_file, 'rb') as f:
#        data = f.read()
#    return base64.b64encode(data).decode()
#
#def set_background(png_file):
#    bin_str = get_base64(png_file)
#    page_bg_img = '''
#    <style>
#    [data-testid="stAppViewContainer"] {
#    background-image: url("data:image/png;base64,%s") ;
#    background-size: cover;
#    }
#    </style>
#    ''' % bin_str
#    st.markdown(page_bg_img, unsafe_allow_html=True)
    
#usernames= ['asanchez', 'patricia', 'mariana', 'rodrigo']
#names= ['Alexander', 'Patricia', 'Mariana', 'Rodrigo']
#passwords= ['12345' ,'12345', '12345', '12345']
#credentials = {"usernames":{}}
#hashed_passwords = stauth.Hasher(passwords).generate()
#for un, name, pw in zip(usernames, names, hashed_passwords):   
#    user_dict = {"name":name,"password":pw}
#    credentials["usernames"].update({un:user_dict})
#authenticator = stauth.Authenticate(credentials, "lanccookie", "lanckey", cookie_expiry_days=30)


st.session_state['authenticator']= authenticator
name= ''
authentication_status= False
username= ''

#name, authentication_status, username= authenticator.login("Login", "main")
#set_background('./background.png')

if authentication_status:

    authenticator.logout('Logout', 'sidebar')
    
    with st.sidebar:
        columns= st.columns((1,1))
        with columns[0]:
            if st.button("Clear states", use_container_width=True):
                for key in st.session_state.keys():
                    del st.session_state[key]
        with columns[1]:
            if st.button("Clear cache", use_container_width=True):
                st.cache_data.clear()
                

        option= option_menu("Annotation Tool", ["Entities", "Annotate", "View Annotations", "NER", "File Logs", \
                                                'Users', 'Statistics'], icons= ['gear', 'markdown', 'eye', \
                                                                                'house-gear', 'filetype-csv', 'person', 'key'])
        
    if option == "Entities":
        Entities.run()
    elif option  == "Annotate":
        Anotar.run()
    elif option == "View Annotations":
        ViewAnnotations.run()
    elif option == "NER":
        NER.run()
    elif option == "File Logs":
        FileLogs.run()
    elif option == 'Statistics':
        Statistics.run()
    elif option == 'Users':
        Users.run()
    
elif authentication_status == False:
   st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')





