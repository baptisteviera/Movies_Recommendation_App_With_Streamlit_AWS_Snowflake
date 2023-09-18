import streamlit as st
import pandas as pd
import random
import datetime 
from PIL import Image
import snowflake_connexion
import ast
import requests
import re

###########################################################################################


st.set_page_config(
	page_title="Page d'accueil",
    initial_sidebar_state="collapsed"
	)

no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# Create a cursor object.
# cur = ctx.cursor()

# LOGIN USER
# ID_USER = log_in.ID_USER
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.write(' ')
with col2:
    st.write(' ')
with col3:
    st.write(' ')
with col4:
    st.write(' ')
with col5:
    st.markdown('<a href="../main" target="_self"><button style="border-radius: 10px;">Se déconnecter</button></a>', unsafe_allow_html=True)



with open('user_id.txt', 'r') as file:
    ID_USER = int(file.read())

# UTILISATEUR
df_utilisateur = snowflake_connexion.df_utilisateur

df_utilisateur_login = df_utilisateur[df_utilisateur['ID'] == ID_USER]

# GENRE PREFERENCE
df_pref = snowflake_connexion.df_pref

# RECOMMENDATION
df_recommendation = snowflake_connexion.df_recommendation

# DATE NAISSANCE
df_date_naissance = snowflake_connexion.df_date_naissance
df_date_naissance_login = df_date_naissance[df_date_naissance["ID"]==df_utilisateur_login["IDDATENAISSANCE"].iloc[0]]


st.title("Bonjour" + " " + df_utilisateur_login["PRENOM"].iloc[0]+",")

st.write(" ")
st.write(" ")

st.markdown('<a href="/search" target="_self"><button style="border-radius: 10px;">  Rechercher des films...  </button></a>', unsafe_allow_html=True)


# FILM
df_film = snowflake_connexion.df_film

df_movies = snowflake_connexion.df_movies

df_match_movies_id = snowflake_connexion.df_match_movies_id

# GENRE
df_genre = snowflake_connexion.df_genre


jointure_genre = df_genre.join(df_film.set_index('IDGENRE'),
                               how='inner',
                               on="ID",
                               lsuffix='_left',
                               rsuffix='_right')
jointure_pref = df_pref.join(df_utilisateur_login.set_index('IDGENREPREFERE'),
                             how='inner',
                             on="ID",
                             lsuffix='_left',
                             rsuffix='_right')


# st.image(df_film_temp["POSTER_LEFT"].iloc[0], width=90)
      # API endpoint for movie poster search
url = "http://www.omdbapi.com/"

# TO DO
# API key for OMDb (get one by registering on their website)
api_key = "<to_complete>"

#####################################################

#TODO ajouter mon algorithme de recommendation

# Réentrainement du modèle ML : il suffit de faire ces commandes

# sql = "select train_and_get_recommendations('MOVIELENS.PUBLIC.ratings_train_data','MOVIELENS.PUBLIC.user_movie_recommendations');"
# snowflake_connexion.cur.execute(sql)
# le training se fait à partir de ratings_train_data (10 000 rows) 
# l'output se trouve ici user_movie_recommendations (TOP 10 recommendation pour chaque user)


st.header("Top 5 des films recommendés pour toi")

top10 = df_recommendation[df_recommendation["USERID"] == ID_USER]
# st.write(top10)
list_top10_str = top10["TOP_10_RECOMMENDATIONS"].iloc[0]
list_top10 = ast.literal_eval(list_top10_str)
# st.write(list_top10[0])
cols = st.columns(5)

for i in range(5): # ON FAIT JUSTE LE TOP 5

  with cols[i]:
    try:
      df_match_movies_i = df_match_movies_id[df_match_movies_id["MOVIEID"]==list_top10[i]]

      df_film_temp = df_film[df_film["ID"] == df_match_movies_i["FILMID"].iloc[0]]
      # st.write(df_film_temp)

      title = df_film_temp["TITLE"].iloc[0]

      # Use regex to remove the pattern "(****)"

      pattern = re.compile(r'\([^)]*\)')
      title_temp = re.sub(pattern, '', title)

      if "," in df_film_temp["TITLE"].iloc[0]:
        ma_chaine_sep = df_film_temp["TITLE"].iloc[0].split(",", 1)
        title_temp = ma_chaine_sep[0]

      st.write(title)
      

                    # Movie title to search for
      # title = df_film_temp["TITLE"].iloc[0]

                    # Build the query parameters for the API request
      params = {
                        "apikey": api_key,
                        "t": title_temp,
                        "plot": "full",
                        "r": "json"
                    }

                    # Send the API request and get the response
      response = requests.get(url, params=params)
                    # Parse the JSON data from the response
      data = response.json()
                    # Extract the poster URL from the data
      poster_url = data["Poster"]
      st.image(poster_url)
    except:
      # API endpoint for movie poster search
      st.image('https://i0.wp.com/authormarystone.com/wp-content/uploads/2019/01/comingsoon.jpg?resize=576%2C864', width=90)
    
#####################################
pref2 = jointure_pref["GENRE3"].iloc[0]

st.header("Des films " + str(pref2) + " pour toi")

# print(pref2)
# IL S'AGIT DE LA TABLE DES GENRES DES FILMS
jointure_genre_pref = jointure_genre[jointure_genre["GENRE1"] == pref2]
#print(jointure_genre_pref.info())
#print(jointure_genre_pref.iloc[0,5])
cols = st.columns(5)
for i in range(5):
  with cols[i]:
    k = random.randrange(len(jointure_genre_pref))
    st.write(jointure_genre_pref.iloc[k, 5])
    try:

                          # Movie title to search for
      title = jointure_genre_pref.iloc[k, 5]

                    # Build the query parameters for the API request
      params = {
                        "apikey": api_key,
                        "t": title,
                        "plot": "full",
                        "r": "json"
                    }

                    # Send the API request and get the response
      response = requests.get(url, params=params)
                    # Parse the JSON data from the response
      data = response.json()
                    # Extract the poster URL from the data
      poster_url = data["Poster"]
      st.image(poster_url)
    except:
      try:
        st.image(jointure_genre_pref.iloc[k, 16], width=100)
      except:
        st.image("https://i0.wp.com/authormarystone.com/wp-content/uploads/2019/01/comingsoon.jpg?resize=576%2C864", width=90)

##################################################################################

pref2 = jointure_pref["GENRE1"].iloc[0]

st.header("Des films " + str(pref2) + " pour toi")

# print(pref2)
# IL S'AGIT DE LA TABLE DES GENRES DES FILMS
jointure_genre_pref = jointure_genre[jointure_genre["GENRE1"] == pref2]
#print(jointure_genre_pref.info())
#print(jointure_genre_pref.iloc[0,5])
cols = st.columns(5)
for i in range(5):
  with cols[i]:
    k = random.randrange(len(jointure_genre_pref))
    st.write(jointure_genre_pref.iloc[k, 5])
    try:
      # st.image(jointure_genre_pref.iloc[k, 16], width=100)
      title = jointure_genre_pref.iloc[k, 5]

                    # Build the query parameters for the API request
      params = {
                        "apikey": api_key,
                        "t": title,
                        "plot": "full",
                        "r": "json"
                    }

                    # Send the API request and get the response
      response = requests.get(url, params=params)
                    # Parse the JSON data from the response
      data = response.json()
                    # Extract the poster URL from the data
      poster_url = data["Poster"]
      st.image(poster_url)
    except:
      try:
        st.image(jointure_genre_pref.iloc[k, 16], width=100)
      except:
        st.image("https://i0.wp.com/authormarystone.com/wp-content/uploads/2019/01/comingsoon.jpg?resize=576%2C864", width=90)
##################################################################################

st.header("Ils ont rencontré le succès ou Blockbuster")

# GENRE POPULARITE
df_popularite = snowflake_connexion.df_popularite


jointure_pop = df_popularite.join(df_film.set_index('IDPOPULARITE'),
                                  how='inner',
                                  on="ID",
                                  lsuffix='_left',
                                  rsuffix='_right')
print(jointure_pop.info())
blockbuster = jointure_pop[jointure_pop["BLOCKBUSTER"] == 1]
cols = st.columns(5)
for i in range(5):
  with cols[i]:
    k = random.randrange(len(blockbuster))
    st.write(blockbuster.iloc[k, 5])
    try:
      # st.image(blockbuster.iloc[k, 16], width=90)
      title = blockbuster.iloc[k, 5]

                    # Build the query parameters for the API request
      params = {
                        "apikey": api_key,
                        "t": title,
                        "plot": "full",
                        "r": "json"
                    }

                    # Send the API request and get the response
      response = requests.get(url, params=params)
                    # Parse the JSON data from the response
      data = response.json()
                    # Extract the poster URL from the data
      poster_url = data["Poster"]
      st.image(poster_url)
    except:
      try:
        st.image(blockbuster.iloc[k, 16], width=90)

      except:
        st.image('https://i0.wp.com/authormarystone.com/wp-content/uploads/2019/01/comingsoon.jpg?resize=576%2C864', width=90)


########################################################################################

ajd = datetime.date.today()
if(ajd.month==12 or True):
  st.header("Films pour Noel")

  # PERIODE
  df_saison = snowflake_connexion.df_saison


  jointure_saison = df_saison.join(df_film.set_index('IDPERIODE'),
                                    how='inner',
                                    on="ID",
                                    lsuffix='_left',
                                    rsuffix='_right')
  # print(jointure_saison.info())


  Noel = jointure_saison[jointure_saison["NOEL"] == 1]
  cols = st.columns(5)
  for i in range(5):
    with cols[i]:
      k = random.randrange(len(Noel))
      st.write(Noel.iloc[k, 10])
      try:
        # st.image(Noel.iloc[k, 21], width=90)
        title = Noel.iloc[k, 10]

                      # Build the query parameters for the API request
        params = {
                          "apikey": api_key,
                          "t": title,
                          "plot": "full",
                          "r": "json"
                      }

                      # Send the API request and get the response
        response = requests.get(url, params=params)
                      # Parse the JSON data from the response
        data = response.json()
                      # Extract the poster URL from the data
        poster_url = data["Poster"]
        st.image(poster_url)
      except:
        try:
          st.image(Noel.iloc[k, 21], width=90)
        except:
          st.image('https://i0.wp.com/authormarystone.com/wp-content/uploads/2019/01/comingsoon.jpg?resize=576%2C864', width=90)


####################################################################################

if(ajd.month==10 and ajd.day>11):

  st.header("Films pour Halloween")

  Halloween = jointure_saison[jointure_saison["HALLOWEEN"] == 1]
  cols = st.columns(5)
  for i in range(5):
    with cols[i]:
      k = random.randrange(len(Halloween))
      st.write(Halloween.iloc[k, 10])
      try:
        # st.image(Halloween.iloc[k, 21], width=90)
        # st.image(Noel.iloc[k, 21], width=90)
        title = Halloween.iloc[k, 10]

                      # Build the query parameters for the API request
        params = {
                          "apikey": api_key,
                          "t": title,
                          "plot": "full",
                          "r": "json"
                      }

                      # Send the API request and get the response
        response = requests.get(url, params=params)
                      # Parse the JSON data from the response
        data = response.json()
                      # Extract the poster URL from the data
        poster_url = data["Poster"]
        st.image(poster_url)
      except:
        try:
          st.image(Halloween.iloc[k, 21], width=90)
        except:
          st.image('https://i0.wp.com/authormarystone.com/wp-content/uploads/2019/01/comingsoon.jpg?resize=576%2C864', width=90)



##########################################################################

if(ajd.month==9 and ajd.day>25 or ajd.month==10 and ajd.day<12):
  st.header("Films pour Action de Grâce")


  # print(jointure_actiongr.info())
  Grace = jointure_saison[jointure_saison["THANKSGIVING"] == 1]

  if ajd.year - df_date_naissance_login["ANNEE"].iloc[0] < 18 :
    Grace = Grace[Grace["ADULT"] == "FAUX"]

  cols = st.columns(5)
  for i in range(5):
    with cols[i]:
      k = random.randrange(len(Grace))
      st.write(Grace.iloc[k, 10])
      try:
        # st.image(Grace.iloc[k, 21], width=90)
        # st.image(Noel.iloc[k, 21], width=90)
        title = Grace.iloc[k, 10]

                      # Build the query parameters for the API request
        params = {
                          "apikey": api_key,
                          "t": title,
                          "plot": "full",
                          "r": "json"
                      }

                      # Send the API request and get the response
        response = requests.get(url, params=params)
                      # Parse the JSON data from the response
        data = response.json()
                      # Extract the poster URL from the data
        poster_url = data["Poster"]
        st.image(poster_url)
      except:
        try:
          st.image(Grace.iloc[k, 21], width=90)
        except:
          st.image('https://i0.wp.com/authormarystone.com/wp-content/uploads/2019/01/comingsoon.jpg?resize=576%2C864', width=90)



################################################################################################


if(ajd.month==7 or ajd.month==8):

  st.header("Films pour les vacances d'été")


  Ete = jointure_saison[jointure_saison["VACANCEETE"] == 1]
  cols = st.columns(5)
  for i in range(5):
    with cols[i]:
      k = random.randrange(len(Ete))
      st.write(Ete.iloc[k, 10])
      try:
        # st.image(Ete.iloc[k, 21], width=90)
        # st.image(Noel.iloc[k, 21], width=90)
        title = Ete.iloc[k, 10]

                      # Build the query parameters for the API request
        params = {
                          "apikey": api_key,
                          "t": title,
                          "plot": "full",
                          "r": "json"
                      }

                      # Send the API request and get the response
        response = requests.get(url, params=params)
                      # Parse the JSON data from the response
        data = response.json()
                      # Extract the poster URL from the data
        poster_url = data["Poster"]
        st.image(poster_url)
      except:
        try:
          st.image(Ete.iloc[k, 21], width=90)
        except:
          st.image("https://i0.wp.com/authormarystone.com/wp-content/uploads/2019/01/comingsoon.jpg?resize=576%2C864", width=90)




#######################################################################################################

if(ajd.month==2 and ajd.day>5 and ajd.day<16):

  st.header("Films pour Saint Valentin")

  Valentin= jointure_saison[jointure_saison["SAINTVALENTIN"] == 1]
  
  # INTERDI AU MINEUR

  if ajd.year - df_date_naissance_login["ANNEE"].iloc[0] < 18 :
    Valentin = Valentin[Valentin["ADULT"] == "FAUX"]



  cols = st.columns(5)
  for i in range(5):
    with cols[i]:
      k = random.randrange(len(Valentin))
      st.write(Valentin.iloc[k, 10])
      try:
        # st.image(Valentin.iloc[k, 21], width=90)
        # st.image(Noel.iloc[k, 21], width=90)
        title = Valentin.iloc[k, 10]

                      # Build the query parameters for the API request
        params = {
                          "apikey": api_key,
                          "t": title,
                          "plot": "full",
                          "r": "json"
                      }

                      # Send the API request and get the response
        response = requests.get(url, params=params)
                      # Parse the JSON data from the response
        data = response.json()
                      # Extract the poster URL from the data
        poster_url = data["Poster"]
        st.image(poster_url)
      except:
        try :
          st.image(Valentin.iloc[k, 21], width=90)
        except:  
          st.image("https://i0.wp.com/authormarystone.com/wp-content/uploads/2019/01/comingsoon.jpg?resize=576%2C864", width=90)


#######################################################################################################


st.header("C'est sortie l'année de votre naissance...")

# DATE SORTIE
df_date_sortie = snowflake_connexion.df_date_sortie

jointure_date_sortie = df_date_sortie.join(df_film.set_index('IDDATESORTIE'),
                             how='inner',
                             on="ID",
                             lsuffix='_left',
                             rsuffix='_right')
# st.write(jointure_date_sortie)

df_date_naissance = snowflake_connexion.df_date_naissance

df_date_naissance_login = df_date_naissance[df_date_naissance["ID"]==df_utilisateur_login["IDDATENAISSANCE"].iloc[0]]
# TODO remplacer le 2000 par la vraie date de naissance

naissance = jointure_date_sortie[jointure_date_sortie["ANNEE"] == df_date_naissance_login["ANNEE"].iloc[0]]
# st.write(naissance)

# INTERDI AU MINEUR
if ajd.year - df_date_naissance_login["ANNEE"].iloc[0] < 18 :
  naissance = naissance[naissance["ADULT"] == "FAUX"]

# st.write(naissance)
# naissance = jointure_date_sortie
# print(naissance.info())
cols = st.columns(5)
for i in range(5):
  with cols[i]:
    k = random.randrange(len(naissance))
    st.write(naissance.iloc[k, 7])
    try:
      # st.image(naissance.iloc[k, 18], width=90)
        title = naissance.iloc[k, 7]
        # st.write(title)
                      # Build the query parameters for the API request
        params = {
                          "apikey": api_key,
                          "t": title,
                          "plot": "full",
                          "r": "json"
                      }

                      # Send the API request and get the response
        response = requests.get(url, params=params)
                      # Parse the JSON data from the response
        data = response.json()
                      # Extract the poster URL from the data
        poster_url = data["Poster"]
        
        st.image(poster_url)

    except:
      try :
        st.image(naissance.iloc[k, 18], width=90)
      except:  
        st.image("https://i0.wp.com/authormarystone.com/wp-content/uploads/2019/01/comingsoon.jpg?resize=576%2C864", width=90)


#######################################################################################################



st.header("Ca vient de chez vous...")
# TODO reparer cela
lieux = df_film[df_film["PAYS"] == "US"]
# lieux = df_film[df_film["PAYS"] == df_utilisateur.iloc[0, 4]]
df_date_naissance_login = df_date_naissance[df_date_naissance["ID"]==df_utilisateur_login["IDDATENAISSANCE"].iloc[0]]

# INTERDI AU MINEUR
if ajd.year - df_date_naissance_login["ANNEE"].iloc[0] < 18 :
  lieux = lieux[lieux["ADULT"] == "FAUX"]

cols = st.columns(5)
print(lieux.info())
for i in range(5):
  with cols[i]:
    k = random.randrange(len(lieux))
    st.write(lieux.iloc[k, 1])
    try:
      # st.image(lieux.iloc[k, 13], width=90)
        title = lieux.iloc[k, 1]

                      # Build the query parameters for the API request
        params = {
                          "apikey": api_key,
                          "t": title,
                          "plot": "full",
                          "r": "json"
                      }

                      # Send the API request and get the response
        response = requests.get(url, params=params)
                      # Parse the JSON data from the response
        data = response.json()
                      # Extract the poster URL from the data
        poster_url = data["Poster"]
        st.image(poster_url)
    except:
      try :
        st.image(lieux.iloc[k, 13], width=90)
      except:  
        st.image("https://i0.wp.com/authormarystone.com/wp-content/uploads/2019/01/comingsoon.jpg?resize=576%2C864", width=90)


#######################################################################################################



