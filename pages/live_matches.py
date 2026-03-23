import streamlit as st
import requests
import pandas as pd



def show():

    st.header("Live Match Dashboard")
    key="211a4cb2c7mshef258cdb418b086p116d87jsnd08701bab594"
    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

    response = requests.get(url, headers=headers)
    data = response.json()

    match_names = []
    match_details = {}

    # Extract matches
    for typeMatch in data["typeMatches"]:

        for seriesMatch in typeMatch["seriesMatches"]:

            if "seriesAdWrapper" in seriesMatch:

                series = seriesMatch["seriesAdWrapper"]
                series_name = series["seriesName"]

                for match in series["matches"]:

                    info = match["matchInfo"]

                    team1 = info["team1"]["teamName"]
                    team2 = info["team2"]["teamName"]

                    match_name = f"{team1} vs {team2}"

                    match_names.append(match_name)

                    match_details[match_name] = {
                        "matchId": info["matchId"],
                        "matchDesc": info["matchDesc"],
                        "matchFormat": info["matchFormat"],
                        "status": info["status"],
                        "venue": info["venueInfo"]["ground"],
                        "city": info["venueInfo"]["city"],
                        "series": series_name
                    }

    # Dropdown to select match
    selected_match = st.selectbox(" Select Match", match_names)

    # Display details
    if selected_match:

        details = match_details[selected_match]

        st.subheader(selected_match)

        col1, col2 = st.columns(2)

        with col1:
            st.write(f" Match ID: {details['matchId']}")
            st.write(f" **Match:** {details['matchDesc']}")
            st.write(f" **Format:** {details['matchFormat']}")
            st.write(f" **Venue:** {details['venue']}")
            st.write(f" **City:** {details['city']}")
            st.write(f" **Status:** {details['status']}")

        with col2:
            st.info(f"Series: {details['series']}")

        st.divider()

        st.subheader(" Scorecard")
        button_res=(st.button("View Full Scorecard"))
        if button_res:
            url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{details['matchId']}/scard"

            headers = {
                "x-rapidapi-key": key,
                "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
                "Content-Type": "application/json"
            }

            response = requests.get(url, headers=headers)
            score_data=response.json()

            scorecard = score_data.get("scorecard", [])

            if len(scorecard) == 0:
                st.warning("Scorecard not available for this match yet.")
                return

            innings = scorecard[0]
            st.markdown("###  Innings Summary")

            st.write(
                f"**Team:** {innings['batteamname']}  \n"
                f"**Score:** {innings['score']}/{innings['wickets']}  \n"
                f"**Overs:** {innings['overs']}  \n"
                f"**Run Rate:** {innings['runrate']}"
            )
            
            # Batting dataframe
            st.markdown("### :bat: Batting")

            batsmen = []

            for player in innings["batsman"]:
                batsmen.append({
                    "Batsman Name": player["name"],
                    "Runs": player["runs"],
                    "Balls": player["balls"],
                    "4's": player["fours"],
                    "6's": player["sixes"],
                    "Strike Rate": player["strkrate"],
                    "outdec": player["outdec"]
                })

            batsman_df = pd.DataFrame(batsmen)

            st.dataframe(batsman_df, width='stretch')
            
            st.markdown("### Bowling")

            bowlers = []

            for bowler in innings["bowler"]:
                bowlers.append({
                    "Bowler": bowler["name"],
                    "Overs": bowler["overs"],
                    "Runs": bowler["runs"],
                    "Wickets": bowler["wickets"],
                    "Economy": bowler["economy"]
                })

            bowler_df = pd.DataFrame(bowlers)

            st.dataframe(bowler_df, width='stretch')
            
            extras = innings["extras"]

            st.markdown("### Extras")

            st.text(
                f"Wides: {extras['wides']}\n "
                f"No Balls: {extras['noballs']}\n "
                f"Leg Byes: {extras['legbyes']}\n "
                f"Byes: {extras['byes']}"
            )
            
            