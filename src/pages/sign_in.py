import itertools
import streamlit as st
import csv
import urllib.request
import hashlib
import os
import random
import datetime
import snowflake_connexion



st.set_page_config(
	page_title="S'inscrire",
    initial_sidebar_state="collapsed"
	)

no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)



df_utilisateur = snowflake_connexion.df_utilisateur
df_date_naissance = snowflake_connexion.df_date_naissance
df_genre_pref = snowflake_connexion.df_pref



# Define the variables and the path to the user storage file
Countries = ["-- Selectionner un pays parmi la liste --", "Afghanistan", "Afrique du Sud", "Albanie", "Algerie", "Allemagne", "Andorre", "Angola", "Antigua-et-Barbuda", "Arabie saoudite", "Argentine", "Armenie", "Australie", "Autriche", "Azerbaidjan", "Bahamas", "Bahrein", "Bangladesh", "Barbade", "Belarus", "Belgique", "Belize", "Benin", "Bhoutan", "Bolivie", "Bosnie-Herzegovine", "Botswana", "Bresil", "Brunei", "Bulgarie", "Burkina Faso", "Burundi", "Cambodge", "Cameroun", "Canada", "Cap-Vert", "Chili", "Chine", "Chypre", "Colombie", "Comores", "Congo, Republique democratique du", "Congo, Republique du", "Coree du Nord", "Coree du Sud", "Costa Rica", "Cote d'Ivoire", "Croatie", "Cuba", "Danemark", "Djibouti", "Dominique", "Republique dominicaine", "egypte", "emirats arabes unis", "equateur", "erythree", "Espagne", "Estonie", "etats-Unis", "ethiopie", "Fidji", "Finlande", "France", "Gabon", "Gambie", "Georgie", "Ghana", "Grece", "Grenade", "Guatemala", "Guinee", "Guinee equatoriale", "Guinee-Bissau", "Guyana", "Haiti", "Honduras", "Hongrie", "Inde", "Indonesie", "Irak", "Iran", "Irlande", "Islande", "Israël", "Italie", "Jamaique", "Japon", "Jordanie", "Kazakhstan", "Kenya", "Kirghizistan", "Kiribati", "Koweit", "Laos", "Lesotho", "Lettonie", "Liban", "Liberia", "Libye", "Liechtenstein", "Lituanie", "Luxembourg", "Macedoine du Nord", "Madagascar", "Malaisie", "Malawi", "Maldives", "Mali", "Malte", "Maroc", "iles Marshall", "Maurice", "Mauritanie", "Mexique", "Micronesie", "Moldavie", "Monaco", "Mongolie", "Montenegro", "Mozambique", "Myanmar", "Namibie", "Nauru", "Nepal", "Nicaragua", "Niger", "Nigeria", "Niue", "Norvege", "Nouvelle-Zelande", "Oman", "Ouganda", "Ouzbekistan", "Pakistan", "Palaos", "Panama", "Papouasie-Nouvelle-Guinee", "Paraguay", "Pays-Bas", "Perou", "Philippines", "Pologne", "Portugal", "Qatar", "Roumanie", "Royaume-Uni", "Russie", "Rwanda", "Saint-Christophe-et-Nieves", "Saint-Marin", "Saint-Vincent-et-les-Grenadines", "Sainte-Lucie", "Salomon, iles", "Salvador", "Samoa", "Sao Tome-et-Principe", "Senegal", "Serbie", "Seychelles", "Sierra Leone", "Singapour", "Slovaquie", "Slovenie", "Somalie", "Soudan", "Soudan du Sud", "Sri Lanka", "Suede", "Suisse", "Suriname", "Swaziland", "Syrie", "Tadjikistan", "Tanzanie", "Tchad", "Republique tcheque", "Thailande", "Timor-Leste", "Togo", "Tonga", "Trinite-et-Tobago", "Tunisie", "Turkmenistan", "Turquie", "Tuvalu", "Ukraine", "Uruguay", "Vanuatu", "Vatican, cite du", "Venezuela", "Viet Nam", "Yemen", "Zambie", "Zimbabwe"]
country_codes = {"-- Selectionner un pays parmi la liste --": "Null",
                 'Afghanistan': 'AF', 'Afrique du Sud': 'ZA', 'Albanie': 'AL', 'Algerie': 'DZ', 'Allemagne': 'DE', 'Andorre': 'AD', 'Angola': 'AO', 'Antigua-et-Barbuda': 'AG', 'Arabie saoudite': 'SA', 'Argentine': 'AR', 'Armenie': 'AM', 'Australie': 'AU', 'Autriche': 'AT', 'Azerbaidjan': 'AZ', 'Bahamas': 'BS', 'Bahrein': 'BH', 'Bangladesh': 'BD', 'Barbade': 'BB', 'Belarus': 'BY', 'Belgique': 'BE', 'Belize': 'BZ', 'Benin': 'BJ', 'Bhoutan': 'BT', 'Bolivie': 'BO', 'Bosnie-Herzegovine': 'BA', 'Botswana': 'BW', 'Bresil': 'BR', 'Brunei': 'BN', 'Bulgarie': 'BG', 'Burkina Faso': 'BF', 'Burundi': 'BI', 'Cambodge': 'KH', 'Cameroun': 'CM', 'Canada': 'CA', 
                 'Cap-Vert': 'CV', 'Chili': 'CL', 'Chine': 'CN', 'Chypre': 'CY', 'Colombie': 'CO', 
                 'Comores': 'KM', 'Congo, Republique democratique du': 'CD', 'Congo, Republique du': 'CG', 
                 'Coree du Nord': 'KP', 'Coree du Sud': 'KR', 'Costa Rica': 'CR', 'Cote d\'Ivoire': 'CI', 
                 'Croatie': 'HR', 'Cuba': 'CU', 'Danemark': 'DK', 'Djibouti': 'DJ', 'Dominique': 'DM', 
                 'Republique dominicaine': 'DO', 'egypte': 'EG', 'emirats arabes unis': 'AE', 'equateur': 'EC', 
                 'erythree': 'ER', 'Espagne': 'ES', 'Estonie': 'EE', 'etats-Unis': 'US', 'ethiopie': 'ET', 
                 'Fidji': 'FJ', 'Finlande': 'FI', 'France': 'FR', 'Gabon': 'GA', 'Gambie': 'GM', 'Georgie': 'GE', 
                 'Ghana': 'GH', 'Grece': 'GR', 'Grenade': 'GD', 'Guatemala': 'GT', 'Guinee': 'GN', 
                 'Guinee equatoriale': 'GQ', 'Guinee-Bissau': 'GW', 'Guyana': 'GY', 'Haiti': 'HT', 'Honduras': 'HN', 
                 'Hongrie': 'HU', 'Inde': 'IN', 'Indonesie': 'ID', 'Irak': 'IQ', 'Iran': 'IR', 'Irlande': 'IE', 
                 'Islande': 'IS', 'Israël': 'IL', 'Italie': 'IT', 'Jamaique': 'JM', "Japon": "JP", "Jordanie": "JO", "Kazakhstan": "KZ", "Kenya": "KE", "Kirghizistan": "KG", "Kiribati": "KI", "Koweit": "KW", "Laos": "LA", "Lesotho": "LS", "Lettonie": "LV", "Liban": "LB", "Liberia": "LR", "Libye": "LY", "Liechtenstein": "LI", "Lituanie": "LT", "Luxembourg": "LU", "Macedoine du Nord": "MK", "Madagascar": "MG", "Malaisie": "MY", "Malawi": "MW", "Maldives": "MV", "Mali": "ML", "Malte": "MT", "Maroc": "MA", "iles Marshall": "MH", "Maurice": "MU", "Mauritanie": "MR", "Mexique": "MX", "Micronesie": "FM", "Moldavie": "MD", "Monaco": "MC", "Mongolie": "MN", "Montenegro": "ME", "Mozambique": "MZ", "Myanmar": "MM", "Namibie": "NA", "Nauru": "NR", "Nepal": "NP", "Nicaragua": "NI", "Niger": "NE", "Nigeria": "NG", "Niue": "NU", "Norvege": "NO", "Nouvelle-Zelande": "NZ", "Oman": "OM", "Ouganda": "UG", "Ouzbekistan": "UZ", "Pakistan": "PK", "Palaos": "PW", "Panama": "PA", "Papouasie-Nouvelle-Guinee": "PG", "Paraguay": "PY", "Pays-Bas": "NL", "Perou": "PE", "Philippines": "PH", "Pologne": "PL", "Portugal": "PT", "Qatar": "QA", "Roumanie": "RO", "Royaume-Uni": "GB", "Russie": "RU", "Rwanda": "RW", "Saint-Christophe-et-Nieves": "KN", "Saint-Marin": "SM", "Saint-Vincent-et-les-Grenadines": "VC", "Sainte-Lucie": "LC", "Salomon, iles": "SB", "Salvador": "SV", "Samoa": "WS", "Sao Tome-et-Principe": "ST", "Senegal": "SN", "Serbie": "RS", "Seychelles": "SC", "Sierra Leone": "SL", "Singapour": "SG", "Slovaquie": "SK", "Slovenie": "SI", "Somalie": "SO", "Soudan": "SD", "Soudan du Sud": "SS", "Sri Lanka": "LK", "Suede": "SE", "Suisse": "CH", "Suriname": "SR", "Swaziland": "SZ", "Syrie": "SY", "Tadjikistan": "TJ", "Tanzanie": "TZ", "Tchad": "TD", "Republique tcheque": "CZ", "Thailande": "TH", "Timor-Leste": "TL", "Togo": "TG", "Tonga": "TO",
                 "Trinite-et-Tobago": "TT", "Tunisie": "TN", "Turkmenistan": "TM", "Turquie": "TR", "Tuvalu": "TV", "Ukraine": "UA", "Uruguay": "UY", "Vanuatu": "VU", "Vatican, cite du": "VA", "Venezuela": "VE", "Viet Nam": "VN", "Yemen": "YE", "Zambie": "ZM", "Zimbabwe": "ZW"
                }

Genres_Liste = ["Animation","Aventure","Romance","Comedy","Action","Family","Drama","Crime","Fantasy","Science Fiction","Thriller","Music","Horror","Documentary","War"]

# Define a function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def new_id(df):
    id_number = df["ID"].iloc[-1] + 1
    return id_number

# Define a function to check if a username exists in the user storage file
def username_exists(username):
    for index, row in df_utilisateur.iterrows():
        if row["PSEUDO"]== username:
            return True
    return False
    

# Define a function to check if a email is already used in the user storage file
def email_exists(email):
    for index, row in df_utilisateur.iterrows():
        if row["EMAIL"]== str(email):
            return True
    return False


def id_genrepref(genrepref):
    

    # Check if a row with the three genres exists
    matching_row = df_genre_pref[df_genre_pref.apply(lambda row: set(row[['GENRE1', 'GENRE2', 'GENRE3']]) == set(genrepref), axis=1)]
    if not matching_row.empty:
        id_genrepref = matching_row['ID'].iloc[0]
        # st.write(matching_row['ID'])
    
    else :     
        # IF NOT EXIST
        # st.write(new_id(df_genre_pref))
        # st.write(type(genrepref[0]))
        query = "INSERT INTO Genre_Prefere (ID, GENRE1, GENRE2, GENRE3) VALUES (%s, %s,%s,%s);"
        snowflake_connexion.cur.execute(query, (new_id(df_genre_pref), genrepref[0],genrepref[1],genrepref[2]))
        # snowflake_connexion.ctx.commit()

        snowflake_connexion.cur.execute("SELECT MAX(ID) FROM Genre_Prefere;")
        id_genrepref = snowflake_connexion.cur.fetchone()[0]
        # print(f"A row with the three genres already exists with ID {id_genrepref}.")

    return id_genrepref

    # attention, on prend pas en consideration l'ordre d'importance des genres1, genres2, genre3 

def id_birthday(birthday):
    # IF EXIST
    # birthday = datetime.datetime.strptime(birthday, "%Y-%m-%d")
    # st.write(birthday)
    for index, row in df_date_naissance.iterrows():
        if row["DATECOMPLETE"]== birthday:
            # la date de naissance existe déjà, un autre utilisateur doit avoir la même date
            id_birthday = row["ID"]
            return id_birthday
        
    # IF NOT EXIST
    query = """
    INSERT INTO DATE_NAISSANCE (ID, ANNEE, MOIS, JOUR, DATECOMPLETE)
    VALUES (%s,%s,%s, %s, %s)
    """
    # Extract the year, month, and day from the date
    year = birthday.year
    month = birthday.month
    day = birthday.day
    # st.write(type(int(new_id(df_date_naissance))))
    # Execute the SQL query with the user data
    snowflake_connexion.cur.execute(query, (new_id(df_date_naissance), year, month, day, birthday))
    # st.write(new_id(df_date_naissance))
    snowflake_connexion.cur.execute("SELECT MAX(ID) FROM DATE_NAISSANCE;")
    id_birthday = snowflake_connexion.cur.fetchone()[0]
    # st.write(id_birthday)
    return id_birthday



# Define a function to add a new user to the user storage file
def add_user(name, surname, username, password, email, location, genrepref, birthday):
    # Define the SQL query to insert a new user
    query = """
    INSERT INTO UTILISATEUR (ID, PRENOM, NOM, PSEUDO, HASHMOTDEPASSE, EMAIL, LOCATION, IDGENREPREFERE, IDDATENAISSANCE)
    VALUES (%s,%s,%s, %s, %s,%s,%s,%s, %s)
    """
    # Execute the SQL query with the user data
    # st.write(type(new_id(df_utilisateur).item()))
    snowflake_connexion.cur.execute(query, (new_id(df_utilisateur), name, surname, username, hash_password(password), email, location, id_genrepref(genrepref), id_birthday(birthday)))
    snowflake_connexion.ctx.commit()





def main():
    st.markdown('<a href="../main" target="_self"><button style="border-radius: 10px;">Retour</button></a>', unsafe_allow_html=True)
    st.title("Inscris-toi !")
    # Add user input fields for username, password, and email
    input_name = st.text_input("Prenom", value="")
    input_surname = st.text_input("Nom", value="")
    input_username = st.text_input("Nouveau nom d'utilisateur", value="")
    input_password = st.text_input("Nouveau mot de passe", value="", type="password")
    input_email = st.text_input("Adresse courriel", value="")
    input_location = st.selectbox("Pays", Countries)
    input_location_code = country_codes[input_location]
    # input_birthyear = st.number_input("Annee de naissance", value=2000, step=1)
    input_birthday = st.date_input("Anniversaire", None, max_value = datetime.date.today(), min_value=datetime.date(1900,1,1))
    
    input_selected_genres = st.multiselect("Selectionne tes 3 genres préférés", Genres_Liste)
    # st.write(input_selected_genres[0])
    # datetime.date(2000, 7, 6)
    # st.write('Your birthday is:', input_birthyear)
    # Add a button to submit the sign up information

    if st.button("S'inscrire"):
        if input_name=="":
            st.error('Le champ Prenom est vide.')

        else:
            if input_surname=="":
                st.error('Le champ Nom est vide.')

            else:
                if input_username=="":
                    st.error("Le champ Nom d'utilisateur est vide.")

                else:
                    if input_password=="":
                        st.error('Le champ Mot de passe est vide.')

                    else:
                        if input_email=="":
                            st.error('Le champ Adresse courriel est vide.')

                        else:
                            if input_location=="-- Selectionner un pays parmi la liste --":
                                st.error('Veuillez choisir un pays parmi la liste dans le champ Pays')
                        
                            else:
                                if len(input_selected_genres) != 3:
                                    st.error("Veuillez sélectionner 3 genres")

                                else:
                                        if username_exists(input_username):
                                            st.error("Nom d'utilisateur deja utilise. Veuillez en choisir un autre.")

                                        else:
                                            if email_exists(input_email):
                                                st.error("Cette adresse courriel est deja associee a un compte.")
                                            else: 
                                                add_user(input_name, input_surname, input_username, input_password, input_email, input_location_code, input_selected_genres, input_birthday)
                                                st.success("Inscription effectuee avec succes.")
                                                st.markdown('<a href="/log_in" target="_self"> <button style="border-radius: 10px;"> Se Connecter ! </button> </a>', unsafe_allow_html=True)
                                                #st.experimental_rerun()

if __name__ == '__main__':
    main()
