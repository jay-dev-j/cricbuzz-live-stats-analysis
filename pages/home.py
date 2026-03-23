import streamlit as st

def show():

    st.markdown(
    "<h1 style='color: green; font-size: 30px;'>Home</h1>",unsafe_allow_html=True,)

    st.write("Welcome to the Cricbuzz Live Stats Project")

    st.write("""
    This project shows:

    - Live Cricket Matches  
    - Player Statistics  
    - SQL Queries  
    - CRUD Database Operations  

    Built using:
    - Python
    - Streamlit
    - Cricbuzz API
    - MySQL
    """)
    
    st.subheader("Project Description")

    st.write("""
    This project is a Cricket Live Statistics Dashboard built using Python and Streamlit.
    It fetches live cricket data from the Cricbuzz API and displays match information,
    player statistics, and database operations in an interactive dashboard.
    """)
    
    st.subheader(" Features")

    st.markdown("""
    -  View **Live Cricket Matches**
    -  Search and view **Player Statistics**
    -  Execute **SQL Queries**
    -  Perform **CRUD Database Operations**
    """)
    
    st.subheader(":hammer_and_pick: Tools & Technologies Used")

    st.markdown("""
    - **Python** :heavy_minus_sign: Backend programming  
    - **Streamlit** :heavy_minus_sign: Web application framework  
    - **Cricbuzz API** :heavy_minus_sign: Live cricket data source  
    - **MySQL** :heavy_minus_sign: Database management  
    """)
    
    st.subheader(" Navigation Guide")

    st.write("""
    Use the sidebar menu to navigate between different pages of the application:

    - **Home** :heavy_minus_sign: Overview of the project  
    - **Live Matches** :heavy_minus_sign: Displays current cricket matches and scores  
    - **Player Stats** :heavy_minus_sign: Search and view player statistics  
    - **SQL Queries** :heavy_minus_sign: Run database queries  
    - **CRUD Operations** :heavy_minus_sign: Manage database records  
    """)
    
    st.caption("Developed using Streamlit :streamlit: by Jayadev J" )