import snowflake.connector
import json
import streamlit as st

# Get the credentials
config_location = '<to_complete>'

config = json.loads(open(str(config_location+'\SF_cred.json')).read())

username = config['secrets']['username']
password = config['secrets']['password']
account = config['secrets']['account']
warehouse = config['secrets']['warehouse']
database = config['secrets']['database']
schema = config['secrets']['schema']
role = config['secrets']['role']

# Gets the version
ctx = snowflake.connector.connect(
    user        = username,
    password    = password,
    account     = account,
    warehouse   = warehouse,
    role        = role,
    database    = database,
    schema     = schema
    )

cur = ctx.cursor()

@st.cache_data(ttl=600)
def run_query(query):
    with ctx.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

# TOP RECOMMENDATION
sql = "select * from MACTH_MOVIES_ID"
cur.execute(sql)
df_match_movies_id = cur.fetch_pandas_all()

# TOP RECOMMENDATION
sql = "select * from V1_USER_MOVIE_RECOMMENDATIONS"
cur.execute(sql)
df_recommendation = cur.fetch_pandas_all()

# RATINGS 100K
sql = "select * from RATINGS"
cur.execute(sql)
df_rating = cur.fetch_pandas_all()

# UTILISATEUR
sql = "select * from Utilisateur"
cur.execute(sql)
df_utilisateur = cur.fetch_pandas_all()


# DATE NAISSANCE
sql = "select * from Date_Naissance"
cur.execute(sql)
df_date_naissance = cur.fetch_pandas_all()

# GENRE PREFERENCE
sql = "select * from Genre_Prefere"
cur.execute(sql)
df_pref = cur.fetch_pandas_all()


# FILM
sql = "select * from Film"
cur.execute(sql)
df_film = cur.fetch_pandas_all()

# FILM
sql = "select * from MOVIES"
cur.execute(sql)
df_movies = cur.fetch_pandas_all()


# GENRE
sql = "select * from Genre"
cur.execute(sql)
df_genre = cur.fetch_pandas_all()


# GENRE POPULARITE
sql = "select * from Popularite"
cur.execute(sql)
df_popularite = cur.fetch_pandas_all()


# PERIODE
sql = "select * from Periode"
cur.execute(sql)
df_saison = cur.fetch_pandas_all()


# DATE SORTIE
sql = "select * from Date_Sortie"
cur.execute(sql)
df_date_sortie = cur.fetch_pandas_all()


# CASTING
sql = "select * from Casting"
cur.execute(sql)
df_casting = cur.fetch_pandas_all()

# CASTING
sql = "select * from Realisateur"
cur.execute(sql)
df_realisateur = cur.fetch_pandas_all()