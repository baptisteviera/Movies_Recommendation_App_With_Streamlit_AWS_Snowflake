import streamlit as st
import csv
import urllib.request
import hashlib
import os
import random
import snowflake_connexion


st.set_page_config(
	page_title="Se connecter",
    initial_sidebar_state="collapsed"
	)

no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# TODO faire la connexion avec snowlfake

df_utilisateur = snowflake_connexion.df_utilisateur

# Define a function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Define a function to check if the login credentials are correct
def check_credentials(username, password):
    for index, row in df_utilisateur.iterrows():
        if row["PSEUDO"]== username and row["HASHMOTDEPASSE"] == hash_password(password):
            # Open the file in write mode
            with open('user_id.txt', 'w') as f:
                # st.write("dans le fichier")
                f.write(str(row["ID"]))
            return True
    return False

def main():
    # Add user input fields for username and password
    # st.session_state
    st.markdown('<a href="../main" target="_self"><button style="border-radius: 10px;">Retour</button></a>', unsafe_allow_html=True)
    st.title("Connectes-toi !")
    with st.form(key="log_in_form"):
        username = st.text_input("Nom d'utilisateur", key="stored_username")
        password = st.text_input("Mot de passe", type="password")
        submit_button = st.form_submit_button(label="Se connecter")
        
        if submit_button :
 #           st.session_state
            if check_credentials(username, password):
                st.success("Connecté en temps que {}".format(username))
                st.markdown('<a href="/home_page" target="_self"><button style="border-radius: 10px;">Accéder à votre espace</button></a>', unsafe_allow_html=True)
            else:
                st.error("Nom d'utilisateur et/ou mot de passe incorrect(s).")
            
if __name__ == '__main__':
    main()
