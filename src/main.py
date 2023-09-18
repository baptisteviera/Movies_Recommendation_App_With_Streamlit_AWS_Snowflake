import streamlit as st

st.set_page_config(
	page_title="Bienvenue sur Metflix",
    initial_sidebar_state="collapsed"
	)

no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)


st.title("Bienvenue sur Metflix !")


st.image("https://i.pinimg.com/564x/4a/2e/9d/4a2e9d0f036879ed9ce109d818200718.jpg")


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.write(' ')

with col2:
    st.markdown('<font size="5"><a href="/log_in" target="_self"><button style="border-radius: 10px;">Connexion</button></a></font> ', unsafe_allow_html=True)

with col3:
    st.markdown('<font size="5"><a href="/sign_in" target="_self"><button style="border-radius: 10px;" >Inscription</button></a></font>', unsafe_allow_html=True)

with col4:
    st.write(' ')