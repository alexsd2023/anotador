import streamlit as st
import time
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

def run():
    msg= ''
    with open('../credentials.yaml') as file:
      config = yaml.load(file, Loader=SafeLoader)

    with st.expander("Register user"):
        try:
            if st.session_state["authentication_status"]:
                authenticator= st.session_state['authenticator']
                if authenticator.register_user('Register user', preauthorization=False):
                    st.success('User registered successfully')
        except Exception as e:
            st.error(e)

    #with st.expander("Add a new user"):
    #    with st.form("usr_form", clear_on_submit=True):
    #        activated= st.toggle("Activate")
    #        
    #        name= st.text_input("First Name")
    #        
    #        lastname= st.text_input("Last Name")
            #photo= st.camera_input("Take a profile picture")
    #        email= st.text_input("Email:", placeholder="yourname@example.com")
    #        passw1= st.text_input("Enter the password", value="", type="password", max_chars= 8, help="Maximun of 8 characters")
    #        passw2= st.text_input("Re-enter the password", value="", type="password", max_chars= 8, help="Maximun of 8 characters",\
    #                    disabled= True)
    #        submitted= st.form_submit_button("Submit")
    #        if submitted:
    #            msg= st.success('New user added to database')
    #            time.sleep(3)
    #            msg.empty()

    with st.expander("Reset your password"):
            if st.session_state["authentication_status"]:
                try:
                    authenticator= st.session_state['authenticator']
                    if authenticator.reset_password(st.session_state["username"], 'Reset password'):                      
                        st.success('Password modified successfully')
                        with open('../credentials.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                            
                except Exception as e:
                    st.error(e)
    with st.expander("Generate a new random password"):
        st.write ('Under construction')
    with st.expander("Retrieve your forgotten username"):
        st.write('Under construction')
    with st.expander("Update  user details"):
        st.write('Under construction')