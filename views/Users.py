import streamlit as st

def run():
    with st.form("usr_form"):
        activated= st.toggle("Activate")
        name= st.text_input("First Name")
        lastname= st.text_input("Last Name")
        #photo= st.camera_input("Take a profile picture")
        passw1= st.text_input("Enter the password", value="", type="password", max_chars= 8, help="Maximun of 8 characters")
        passw2= st.text_input("Re-enter the password", value="", type="password", max_chars= 8, help="Maximun of 8 characters",\
                       disabled= True)
        submitted= st.form_submit_button("Submit")
        if submitted:
            st.write('New user added')