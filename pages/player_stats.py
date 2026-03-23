import streamlit as st
import requests
import pandas as pd



def show():
    key="211a4cb2c7mshef258cdb418b086p116d87jsnd08701bab594"
    st.header("Player Statistics")

    player_name = st.text_input("Enter Player Name")

    search = st.button("Search Player")
    if search:
        st.session_state["player_name"] = player_name
    if search or "player_name" in st.session_state:
        player_name = st.session_state["player_name"]
        st.write("Searching for:", player_name)
       
        url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"

        querystring = {"plrN":player_name}

        headers = {
            "x-rapidapi-key": key,
            "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers, params=querystring)

        data = response.json()

        if "player" not in data or len(data["player"]) == 0:
            st.error("Player is not there!!")
            return

        players = data["player"]

        # Createing player_options list comp for dropdown options
        player_options = [f"{p['name']} ({p['teamName']})" for p in players]

        selected_player = st.selectbox("Select Player", player_options)

        # Get selected player index
        selected_index = player_options.index(selected_player)

        player = players[selected_index]


        player_id = player["id"]
        name = player["name"]
        team = player["teamName"]
        dob = player["dob"]
        image_id = player["faceImageId"]
        image_url = f"https://static.cricbuzz.com/a/img/v1/152x152/i1/c{image_id}/player.jpg"
        st.image(image_url, width=150)
        st.subheader(name)
        st.write("Player ID:", player_id)
        st.write("Country:", team)
        st.write("Date of Birth:", dob)
        st.header("Full carrer Statistics")

        url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"

        headers = {
            "x-rapidapi-key": key,
            "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)

        player_info=response.json()
        batting_style = player_info.get("bat", "NA")
        bowling_style = player_info.get("bowl", "NA")
        height = player_info.get("height", "NA")
        role = player_info.get("role", "NA")
        birthPlace = player_info.get("birthPlace", "NA")
        realteam = player_info.get("intlTeam", "NA")
        teams = player_info.get("teams", "NA")
        DoB = player_info.get("DoB", "NA")
        col1,col2=st.columns(2)
        with col1:
            st.write("**Batting Style:**", batting_style)
            st.write("**Bowling Style:**", bowling_style)
            st.write("**Role:**", role)
            st.write("**Height:**", height)
        with col2:
                st.write("**Born:**", DoB)
                st.write("**Birth Place:**", birthPlace)
                st.write("**International Team:**", realteam)
                
        st.subheader("Teams")

        teams_value = player_info.get("teams", "NA")

        teamlist = teams_value.split(",")

        for t in teamlist:
            st.write("-", t.strip())


        st.subheader("Rankings")

        rankings = player_info.get("rankings", {})
        batrank = rankings.get("bat", {})

        test_rank = batrank.get("testRank", "NA")
        test_best_rank = batrank.get("testBestRank", "NA")
        odi_best_rank = batrank.get("odiBestRank", "NA")
        t20_best_rank = batrank.get("t20BestRank", "NA")

        st.write("Test Rank:", test_rank)
        st.write("Best Test Rank:", test_best_rank)
        st.write("Best ODI Rank:", odi_best_rank)
        st.write("Best T20 Rank:", t20_best_rank)


        recent_bowl = player_info.get("recentBowling", {})
        rows = recent_bowl.get("rows", [])

        bowlingrows = []

        for r in rows:

            values = r.get("values", [])

            wickets = values[1] if len(values) > 1 else "NA"
            opponent = values[2] if len(values) > 2 else "NA"
            format_type = values[3] if len(values) > 3 else "NA"
            date = values[4] if len(values) > 4 else "NA"

            bowlingrows.append({
                "Wickets": wickets,
                "Opponent": opponent,
                "Format": format_type,
                "Date": date
            })

        bowl_df = pd.DataFrame(bowlingrows)

        st.subheader("Recent Bowling")

        st.dataframe(bowl_df, width="stretch")
        
        get_batting =  st.button("Show Batting_Stats")
        if get_batting:
            url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/batting"

            headers = {
                "x-rapidapi-key": key,
                "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
                "Content-Type": "application/json"
            }

            response = requests.get(url, headers=headers)

            batting_info = response.json()

            headers = batting_info.get("headers", [])
            values = batting_info.get("values", [])

            rows = []

            for v in values:
                rows.append(v.get("values", []))

            df = pd.DataFrame(rows, columns=headers)

            st.subheader("Batting Career Statistics")

            st.dataframe(df, width="stretch")
        bowling_in=st.button("Show Bowling_Stats")
        if bowling_in:
            url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/bowling"

            headers = {
                "x-rapidapi-key": key,
                "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
                "Content-Type": "application/json"
            }

            response = requests.get(url, headers=headers)

            bowling_info = response.json()
            headers = bowling_info.get("headers", [])
            values = bowling_info.get("values", [])

            rows = []

            for v in values:
                rows.append(v.get("values", []))

            df = pd.DataFrame(rows, columns=headers)

            st.subheader("Bowling Career Statistics")

            st.dataframe(df, width="stretch")