import streamlit as st
import mysql.connector
import pandas as pd
import datetime
def show():

    st.title("CRUD Operations")
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cricbuzz_livestats_project"
    )

    cursor = conn.cursor()
    operation = st.selectbox("Select Operation",["Create", "Read", "Update", "Delete"])
    table = st.selectbox("Select Table",["players", "teams", "venues"])
    # CREATE
    
    if operation == "Create":
        st.subheader(f"Insert Data into {table}")
        if table == "players":
            player_id = st.number_input("Player ID")
            name = st.text_input("Player Name")
            nickname = st.text_input("Nickname")
            role = st.text_input("Role")
            batting = st.text_input("Batting Style")
            bowling = st.text_input("Bowling Style")
            birthplace = st.text_input("Birth Place")
            dob = st.date_input("Select a date",min_value=datetime.date(1900, 1, 1),max_value=datetime.date.today())
            team = st.text_input("International Team")
            if st.button("Insert Player"):

                query = """
                INSERT INTO players
                (player_id,name,nickname,role,batting_style,bowling_style,
                birth_place,date_of_birth,international_team)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """

                cursor.execute(query,
                               (player_id,name,nickname,role,batting,
                                bowling,birthplace,dob,team))

                conn.commit()

                st.success("Player inserted successfully")

        elif table == "teams":

            team_id = st.number_input("Team ID")
            team_name = st.text_input("Team Name")
            short = st.text_input("Short Name")
            country = st.text_input("Country")
            category = st.text_input("Category")

            if st.button("Insert Team"):

                query = """
                INSERT INTO teams
                (team_id,team_name,short_name,country_name,category)
                VALUES (%s,%s,%s,%s,%s)
                """
                cursor.execute(query,(team_id,team_name,short,country,category))
                conn.commit()
                st.success("Team inserted successfully")

        elif table == "venues":
            venue_id = st.number_input("Venue ID")
            ground = st.text_input("Ground Name")
            city = st.text_input("City")
            country = st.text_input("Country")
            timezone = st.text_input("Timezone")
            capacity = st.number_input("Capacity")
            ends = st.text_input("Ends")
            home = st.text_input("Home Team")

            if st.button("Insert Venue"):

                query = """
                INSERT INTO venues
                (venueId,ground,city,country,timezone,capacity,ends,home_team)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """

                cursor.execute(query,
                               (venue_id,ground,city,country,timezone,
                                capacity,ends,home))

                conn.commit()

                st.success("Venue inserted successfully")
    # READ
    elif operation == "Read":
        st.subheader(f"View Data from {table}")
        query = f"SELECT * FROM {table}"
        df = pd.read_sql(query, conn)
        st.dataframe(df, width="stretch")
    #UPDATE
    elif operation=="Update":
        st.subheader(f"Update Data in {table}")
        if table == "players":
            
            player_id = st.number_input("Enter Player ID to Update")
            name = st.text_input("New Name")
            nickname = st.text_input("New Nickname")
            role = st.text_input("New Role")
            batting = st.text_input("New Batting Style")
            bowling = st.text_input("New Bowling Style")
            birthplace = st.text_input("New Birth Place")
            dob = str(st.date_input("Select a date"))
            team = st.text_input("New International Team")

            if st.button("Update Player"):
                check_query = "SELECT COUNT(*) FROM players WHERE player_id=%s"
                cursor.execute(check_query, (player_id,))
                result = cursor.fetchone()

                if result[0] == 0:
                    st.error(":warning: Player ID does not exist")

                else:
                    query = """
                    UPDATE players
                    SET name=%s,
                        nickname=%s,
                        role=%s,
                        batting_style=%s,
                        bowling_style=%s,
                        birth_place=%s,
                        date_of_birth=%s,
                        international_team=%s
                    WHERE player_id=%s
                    """

                    cursor.execute(query, (
                        name, nickname, role, batting, bowling,
                        birthplace, dob, team, player_id
                    ))

                    conn.commit()

                    st.success("Player updated successfully")
        
        elif table == "teams":
            team_id = st.number_input("Team ID")
            team_name = st.text_input("Team Name")
            short_name = st.text_input("Short Name")
            country_name = st.text_input("Country Name")
            category = st.text_input("Category")
            if st.button("Update Team"):
                check_query = "SELECT COUNT(*) FROM teams WHERE team_id=%s"
                cursor.execute(check_query, (team_id,))
                result = cursor.fetchone()

                if result[0] == 0:
                    st.error(":warning: Team ID does not exist")
                else:
                    query = """
                    UPDATE teams
                    SET team_name=%s,
                        short_name=%s,
                        country_name=%s,
                        category=%s
                    WHERE team_id=%s
                    """
                    cursor.execute(query, (team_name, short_name, country_name, category, team_id))
                    conn.commit()
                    st.success("Team updated successfully")
        elif table == "venues":
            venue_id = st.number_input("Venue ID")
            ground = st.text_input("Ground Name")
            city = st.text_input("City")
            country = st.text_input("Country")
            timezone = st.text_input("Timezone")
            capacity = st.number_input("Capacity")
            ends = st.text_input("Ends")
            home_team = st.text_input("Home Team")
            if st.button("Update Venue"):
                check_query = "SELECT COUNT(*) FROM venues WHERE venueId=%s"
                cursor.execute(check_query, (venue_id,))
                result = cursor.fetchone()

                if result[0] == 0:
                    st.error(":warning: Venue ID does not exist")
                else:
                    query = """
                    UPDATE venues
                    SET ground=%s,
                        city=%s,
                        country=%s,
                        timezone=%s,
                        capacity=%s,
                        ends=%s,
                        home_team=%s
                    WHERE venueId=%s
                    """

                    cursor.execute(query, (ground, city, country, timezone, capacity, ends, home_team, venue_id))
                    conn.commit()
                    st.success("Venue updated successfully")
    # DELETE           
    elif operation == "Delete":

        st.subheader(f"Delete Data from {table}")

        if table == "players":

            player_id = st.number_input("Player ID")

            if st.button("Delete Player"):
                check_query = "SELECT COUNT(*) FROM players WHERE player_id=%s"
                cursor.execute(check_query, (player_id,))
                result = cursor.fetchone()

                if result[0] == 0:
                    st.error(":warning: Player ID does not exist")
                else:
                    query = "DELETE FROM players WHERE player_id=%s"
                    cursor.execute(query, (player_id,))
                    conn.commit()
                    st.success("Player deleted successfully")

        elif table == "teams":

            team_id = st.number_input("Team ID")

            if st.button("Delete Team"):
                check_query = "SELECT COUNT(*) FROM teams WHERE team_id=%s"
                cursor.execute(check_query, (team_id,))
                result = cursor.fetchone()

                if result[0] == 0:
                    st.error(":warning: Team ID does not exist")
                else:
                    query = "DELETE FROM teams WHERE team_id=%s"
                    cursor.execute(query, (team_id,))
                    conn.commit()
                    st.success("Team deleted successfully")

        elif table == "venues":

            venue_id = st.number_input("Venue ID")

            if st.button("Delete Venue"):
                check_query = "SELECT COUNT(*) FROM venues WHERE venueId=%s"
                cursor.execute(check_query, (venue_id,))
                result = cursor.fetchone()

                if result[0] == 0:
                    st.error(":warning: Venue ID does not exist")
                else:
                    query = "DELETE FROM venues WHERE venueId=%s"
                    cursor.execute(query, (venue_id,))
                    conn.commit()
                    st.success("Venue deleted successfully")

    cursor.close()
    conn.close()