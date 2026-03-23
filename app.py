import streamlit as st

# Importing all pages
from pages import home
from pages import live_matches
from pages import player_stats
from pages import sql_queries
from pages import crud_operations

hide_pages = """
<style>
[data-testid="stSidebarNav"] {display: none;}
</style>
"""


st.markdown(hide_pages, unsafe_allow_html=True)

st.set_page_config(page_title="Cricbuzz Live Stats Project", layout="wide")

st.markdown("<h1 style='color: #1f77b4; font-size: 30px;'>Cricket Live Stats Dashboard</h1>",unsafe_allow_html=True,)


st.sidebar.title("Navigation")

page = st.sidebar.selectbox(
    "Go to",
    (
        "Home",
        "Live Matches",
        "Player Statistics",
        "SQL Queries",
        "CRUD Operations"
    )
)

if page == "Home":
    home.show()

elif page == "Live Matches":
    live_matches.show()

elif page == "Player Statistics":
    player_stats.show()

elif page == "SQL Queries":
    sql_queries.show()

elif page == "CRUD Operations":
    crud_operations.show()