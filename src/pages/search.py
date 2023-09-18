import streamlit as st
import pandas as pd
import numpy as np
import snowflake_connexion
import requests


st.set_page_config(
	page_title="Rechercher un film",
    initial_sidebar_state="collapsed"
	)

no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

st.markdown('<a href="/home_page" target="_self"><button style="border-radius: 10px;">Accueil</button></a>', unsafe_allow_html=True)

st.title("Rechercher un film")



df_film = snowflake_connexion.df_film.fillna(0)
df_genre = snowflake_connexion.df_genre
df_casting = snowflake_connexion.df_casting
df_real = snowflake_connexion.df_realisateur
df_pop = snowflake_connexion.df_popularite
df_date = snowflake_connexion.df_date_sortie
df_perd = snowflake_connexion.df_saison


# UTILISATEUR
with open('user_id.txt', 'r') as file:
    ID_USER = int(file.read())

df_utilisateur = snowflake_connexion.df_utilisateur

df_utilisateur_login = df_utilisateur[df_utilisateur['ID'] == ID_USER]

df_rating = snowflake_connexion.df_rating
df_ratings_login = df_rating[df_rating["USERID"]==ID_USER]

#merging film and genre dataframe
df_film['IDGENRE'] = df_film['IDGENRE'].astype(int)
film_genre = df_genre.join(df_film.set_index('IDGENRE'), how='inner', on="ID",  lsuffix='_left', rsuffix='_right')

film_genre['IDACTEUR'] = film_genre['IDACTEUR'].astype(int)
film_genre_cast = df_casting.join(film_genre.set_index('IDACTEUR'), how='inner', on="ID",
                               lsuffix='_casting', rsuffix='_genre')

result_join = df_real.join(film_genre_cast.set_index('IDREALISATEUR'),
                                    how='inner', on="ID",
                                    lsuffix='_real', rsuffix='_film_genre_cast')


result_join['IDPOPULARITE'] = result_join['IDPOPULARITE'].astype(int)
result = df_pop.join(result_join.set_index('IDPOPULARITE'),
                                    how='inner', on="ID",
                                    lsuffix='_pop', rsuffix='_result_join')
result['IDDATESORTIE'] = result['IDDATESORTIE'].astype(int)
result_date = df_date.join(result.set_index('IDDATESORTIE'),
                                    how='inner', on="ID",
                                    lsuffix='_date', rsuffix='_result')
result_date['IDPERIODE'] = result_date['IDPERIODE'].astype(int)
result_final = df_perd.join(result_date.set_index('IDPERIODE'),
                                    how='inner', on="ID",
                                    lsuffix='_perd', rsuffix='_result_date')



#  search bar
col1, col2, col3 = st.columns(3)
with col2:
    # add_checkbox2 = st.checkbox('Filtrage Avancé', label_visibility="collapsed", disabled=True)
    st.write(" ")
    st.write(" ")
    add_checkbox = st.checkbox('Filtrage Avancé', key='advance')

with col1:
    if add_checkbox:
        text_search = st.text_input("Recherche", value="", disabled=True)
    else:
        text_search = st.text_input("Recherche par titre de films ", value="")



# text_search = text_search.replace(" ", "-")
# Filter the dataframe using masks
m1 = result_final["PAYS"].str.contains(text_search)
m2 = result_final["TITLE"].str.contains(text_search)
m3 = result_final["GENRE1"].str.contains(text_search)
df_search = result_final[m1 | m2 | m3]




# is_click_var = False

#def is_click():
    # global is_click_var
    # is_click_var = True
    # st.write(is_click_var)
    # print(is_click_var)


N_cards_per_row = 5
def display_search(data_frame,page_size):
    
    # Calculate the number of pages
    num_pages = int(np.ceil(len(data_frame) / page_size))
    # Add a selectbox to the sidebar for page navigation
    page_num = st.sidebar.selectbox("Page", range(num_pages))
    # Calculate the start and end index of the current page
    start_idx = page_num * page_size
    end_idx = min((page_num + 1) * page_size, len(data_frame))
    # Display the results for the current page
    data_frame2 = data_frame.iloc[start_idx:end_idx]
    for n_row, row in data_frame2.reset_index().iterrows():
        i = n_row%N_cards_per_row
        if i==0:
            st.write("---")
            cols = st.columns(N_cards_per_row, gap="medium")
        # draw the card

        with cols[n_row%N_cards_per_row]:

            st.caption(f"MOY : {str(row['MOYENNEVOTE']).strip()} - NB : {str(row['TOTALVOTE']).strip()}")
            st.markdown(f"**{row['PAYS'].strip()}-{int(row['ANNEE'])}**")
            st.markdown(f"*{row['TITLE'].strip()}*")

            try:

                find = False

                # st.image(row['POSTER_RIGHT'])
        # API endpoint for movie poster search

                url = "http://www.omdbapi.com/"

                # API key for OMDb (get one by registering on their website)
                api_key = "<to_complete>"

                # Movie title to search for
                title = row["TITLE"]

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
 
               
                for index, row_rating in df_ratings_login.iterrows():
                    if row_rating["MOVIEID"] == row["ID"]:
                        st.write("Ma Note : ", row_rating["RATING"])
                        find = True

                if find == False:
                    
                    ID_MOVIE = row["ID"]
                    # st.markdown(f"""<button onclick="note_estimated({ID_USER}, {ID_MOVIE})">Note Estimée</button>""", unsafe_allow_html=True)
                    note_estimee = st.button("Note Estim ", ID_MOVIE , use_container_width=True)
                    # st.markdown("<button onclick='is_click()'>Note Estimée</button>", unsafe_allow_html=True)
                    # st.write(is_click_var)
                    if note_estimee :
                        sql = "truncate no_ratings"
                        snowflake_connexion.cur.execute(sql)

                        sql = "insert into no_ratings (USERID, MOVIEID) values (%s, %s)"
                        snowflake_connexion.cur.execute(sql, (ID_USER, ID_MOVIE))
                        # TODO # do it once on snowflake terminal
                        # select deploy_model('movielens-model-v1', '<S3_MODEL_ARTIFACT>'); 
                        sql = "select nr.USERID, nr.MOVIEID, m.title, invoke_model('movielens-model-v1', nr.USERID, nr.MOVIEID) as rating_prediction from no_ratings nr, movies m where nr.movieid = m.movieid"
                        snowflake_connexion.cur.execute(sql)
                        results = snowflake_connexion.cur.fetchall()
                        for row in results:
                            value = row[3]
                            st.write(value)

            except AttributeError as e:
                    
                    # Print the poster URL (or do whatever else you want with it)
                    # print("Poster URL:", poster_url)
                    st.image('https://i0.wp.com/authormarystone.com/wp-content/uploads/2019/01/comingsoon.jpg?resize=576%2C864')
                

        # Add a pagination wIDget to the bottom of the page
    st.sidebar.write("Page", page_num + 1, "of", num_pages)




if text_search:
    try :
        display_search(df_search.head(100),20)
    except :
        pass
        #st.warning("UNE ERREURE TRES MYSTERIEURSE EST SURVENUE",  icon="🚨")
elif add_checkbox:
        # Add a selectbox to the sidebar:
        add_selectbox = st.sidebar.multiselect(
            'Choisissez votre genre de Film',
            result_final['GENRE1'].unique()
        )
        add_selectbox2 = st.sidebar.selectbox(
            'Choisissez le realisateur',
            result_final['NOM'].unique()
        )
        # Add a slider to the sidebar:
        start, end = st.sidebar.slider(
            'Choisissez un intervalle de score',
            0.0, 10.0, (5.0, 7.0)
        )
        start2, end2 = st.sidebar.slider(
            'Choisissez une période',
            1950, 2018, (1960, 2010)
        )
        add_button = st.sidebar.button('Appliquer')
        if add_button:
            # convert 'MOYENNEVOTE' column to numeric type
            result_final['MOYENNEVOTE'] = pd.to_numeric(result_final['MOYENNEVOTE'], errors='coerce')
            result_list = result_final.loc[(result_final['MOYENNEVOTE'].between(start, end, inclusive=True)&
                                            result_final['ANNEE'].between(start2, end2, inclusive=True)), :]
            if not add_selectbox:
                final_result = result_list.loc[result_list['NOM'] == add_selectbox2, :]
            else:
                final_result = result_list.loc[
                               result_list['GENRE1'].isin(add_selectbox) & (result_list['NOM'] == add_selectbox2), :]

            for n_row, row in final_result.reset_index().iterrows():
                i = n_row % N_cards_per_row
                if i == 0:
                    st.write("---")
                    cols = st.columns(N_cards_per_row, gap="medium")
                # draw the card
                with cols[n_row % N_cards_per_row]:
                    st.caption(f"MOY : {str(row['MOYENNEVOTE']).strip()} - NB : {str(row['TOTALVOTE']).strip()}")
                    st.markdown(f"**{row['PAYS'].strip()}-{int(row['ANNEE'])}**")
                    st.markdown(f"*{row['TITLE'].strip()}*")
                    try:
                        st.image(row['POSTER_RIGHT'])
                    except:
                        st.image('https://i0.wp.com/authormarystone.com/wp-content/uploads/2019/01/comingsoon.jpg?resize=576%2C864')



