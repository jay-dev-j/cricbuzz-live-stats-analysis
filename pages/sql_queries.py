import streamlit as st
import pandas as pd
import mysql.connector

def show():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cricbuzz_livestats_project"
    )
    query_titles = [
    "Q1 - Indian International Players with Batting and Bowling Style",
    "Q2 - Recent Completed Matches with Teams, Venue and Date",
    "Q3 - Top 10 ODI Run Scorers with Batting Average and Centuries",
    "Q4 - Cricket Venues with Capacity Greater Than 25,000",
    "Q5 - Teams Ranked by Total Match Wins",
    "Q6 - Distribution of Players by Playing Role",
    "Q7 - Total Runs Scored Across Different Cricket Formats",
    "Q8 - Series Hosted in 2024 with Match Format and Total Matches",
    "Q9 - All-Rounders with More Than 1000 Runs and 50 Wickets",
    "Q10 - Recent Completed Matches with Winning Team and Venue",
    "Q11 - Players with Runs in Multiple Formats and Overall Batting Average",
    "Q12 - Team Performance Comparison: Home Wins vs Away Wins",
    "Q13 - Batting Partnerships with More Than 100 Runs",
    "Q14 - Bowler Performance at Specific Venues (Economy and Wickets)",
    "Q15 - Player Performance in Close Matches",
    "Q16 - Year-wise Batting Performance of Players Since 2020",
    "Q17 - Impact of Toss Decision on Match Winning Percentage",
    "Q18 - Best Economy Bowlers in ODI and T20 Matches",
    "Q19 - Most Consistent Batsmen Based on Run Standard Deviation",
    "Q20 - Player Batting Performance Across Test, ODI and T20 Formats",
    "Q21 - Comprehensive Player Performance Score (Batting + Bowling)",
    "Q22 - Head-to-Head Team Performance in the Last 3 Years",
    "Q23 - Recent Player Form Analysis Based on Last 5 and 10 Matches",
    "Q24 - Top Batting Partnerships with Success Rate",
    "Q25 - Quarterly Player Performance Trend Analysis"
    ]
    
    query_map = {

    "Q1 - Indian International Players with Batting and Bowling Style":
    """
    select name, role as Playing_Role,batting_style,bowling_style from players where international_team="India"
    """,

    "Q2 - Recent Completed Matches with Teams, Venue and Date":
    """
    select m.matchDesc as Match_description , t1.team_name as Team_1, t2.team_name as Team_2, v.ground as Venue_name, v.city as City, FROM_UNIXTIME(m.startDate/1000) AS matchDate
    from matches m join teams t1 on m.team1Id=t1.team_id
    join teams t2 on m.team2Id=t2.team_id
    join venues v on m.venueId=v.venueId
    where FROM_UNIXTIME(m.startDate/1000) <= CURDATE() order by matchDate desc limit 7
    """,

    "Q3 - Top 10 ODI Run Scorers with Batting Average and Centuries":
    """
    select p.name as Player_name, pcb.runs AS total_runs, pcb.average AS batting_average,pcb.hundreds AS centuries
    from player_career_batting pcb JOIN players p ON pcb.player_id = p.player_id WHERE pcb.format = 'ODI'
    ORDER BY pcb.runs DESC LIMIT 10
    """,

    "Q4 - Cricket Venues with Capacity Greater Than 25,000":
    """
    select ground as Venue_name,city,country,capacity from venues where capacity > 25000 order by capacity desc

    """,

    "Q5 - Teams Ranked by Total Match Wins":
    """
    SELECT winningTeamName AS team_name,COUNT(*) AS total_wins FROM matches
    WHERE winningTeamName NOT IN ('Match Postponed','No Result','Draw','Tie','Mathch Postponed')
    GROUP BY winningTeamName ORDER BY total_wins DESC
    """,

    "Q6 - Distribution of Players by Playing Role":
    """
    select role as playing_role,count(*) as total_count from players group by role
    """,

    "Q7 - Total Runs Scored Across Different Cricket Formats":
    """
    select format as Cricket_format, sum(runs) as Total_runs from player_career_batting group by format
    """,

    "Q8 - Series Hosted in 2024 with Match Format and Total Matches":
    """
    select s.series_name, v.country as host_country, m.matchformat,
    from_unixtime(s.start_date/1000) as start_date, count(m.matchid) as total_matches_planned 
    from series s join matches m on s.series_id = m.seriesid
    join venues v on m.venueid = v.venueid
    where year(from_unixtime(s.start_date/1000)) = 2024
    group by s.series_name, v.country, m.matchformat, start_date order by start_date 
    """,

    "Q9 - All-Rounders with More Than 1000 Runs and 50 Wickets":
    """
    select p.name, sum(pcbt.runs) as total_runs,sum(pcb.wickets) as total_wickets, pcb.format as Cricket_format from 
    players p join player_career_batting pcbt on p.player_id=pcbt.player_id
    join player_career_bowling pcb on p.player_id=pcb.player_id
    where p.role in('Bowling Allrounder','Batting Allrounder')
    group by p.player_id,p.name,pcb.format
    having sum(pcbt.runs) > 1000 and sum(pcb.wickets) > 50
    """,

    "Q10 - Recent Completed Matches with Winning Team and Venue":
    """
    select m.matchDesc as Match_description,t1.team_name as Team1,t2.team_name as Team2,m.winningTeamName as Winning_team_name,m.victoryMargin,m.victoryType,v.ground from 
    matches m join teams t1 on m.team1Id=t1.team_id
    join teams t2 on m.team2Id=t2.team_id
    join venues v on m.venueId=v.venueId
    where m.state="complete" order by from_unixtime(m.endDate/1000) desc limit 20
    """,

    "Q11 - Players with Runs in Multiple Formats and Overall Batting Average":
    """
    select p.name as player_name, 
    sum(case when pcb.format = 'test' then pcb.runs else 0 end) as test_runs,
    sum(case when pcb.format = 'odi' then pcb.runs else 0 end) as odi_runs,
    sum(case when pcb.format = 't20i' then pcb.runs else 0 end) as t20i_runs,
    avg(pcb.average) as overall_batting_average
    from players p join player_career_batting pcb on p.player_id = pcb.player_id
    group by p.player_id, p.name having count(distinct pcb.format) >= 2
    """,

    "Q12 - Team Performance Comparison: Home Wins vs Away Wins":
    """
    select t.team_name,
    sum(case when t.country_name = v.country and m.winningTeamName = t.team_name then 1 else 0 end) as home_wins,
    sum(case when t.country_name != v.country and m.winningTeamName = t.team_name then 1 else 0 end) as away_wins
    from matches m join venues v on m.venueId = v.venueId 
    join teams t on m.team1Id = t.team_id or m.team2Id = t.team_id 
    where m.state = 'complete'
    group by t.team_name order by home_wins desc
    """,

    "Q13 - Batting Partnerships with More Than 100 Runs":
    """
    select bat1name as player1,bat2name as player2,
    totalruns as partnership_runs,inningsid
    from partnerships where totalruns >= 100
    """,

    "Q14 - Bowler Performance at Specific Venues (Economy and Wickets)":
    """
    select b.bowlername,v.ground as venue_name,avg(b.economy) as avg_economy_rate,sum(b.wickets) as total_wickets,
    count(distinct b.matchId) as matches_played 
    from bowler_scores b join matches m on b.matchId = m.matchId
    join venues v on m.venueId = v.venueId where b.overs >= 4
    group by b.bowlername, v.ground having count(distinct b.matchId) >= 3
    """,

    "Q15 - Player Performance in Close Matches":
    """
    select p.name as player_name,avg(bs.runs) as average_runs,count(bs.matchId) as close_matches_played
    from batsman_scores bs
    join matches m on bs.matchId = m.matchId
    join players p on bs.batsmanId = p.player_id
    where 
    (m.victoryMargin < 50 and m.victoryType = 'runs')
    or
    (m.victoryMargin < 5 and m.victoryType = 'wickets')
    group by p.name
    order by average_runs desc
    """,

    "Q16 - Year-wise Batting Performance of Players Since 2020":
    """
    select p.name as player_name,
    year(from_unixtime(m.startDate/1000)) as year,
    avg(bs.runs) as avg_runs_per_match,
    avg(bs.strikeRate) as avg_strike_rate,
    count(bs.matchId) as matches_played
    from matches m join batsman_scores bs on m.matchId = bs.matchId
    join players p on bs.batsmanId = p.player_id
    where year(from_unixtime(m.startDate/1000)) >= 2020
    group by p.player_id, year
    having count(bs.matchId) >= 5
    order by year, avg_runs_per_match desc
    """,

    "Q17 - Impact of Toss Decision on Match Winning Percentage":
    """
    select
    case when tossStatus like "%bat%" then "bat first" 
    when tossStatus like "%bowl%"then "bowl first" end
    as toss_status,
    count(*) as total_matches,
    sum(case when tossStatus like concat(winningTeamName,"%")then 1 else 0 end) as toss_winner_won,
    (sum(case when tossStatus like concat(winningTeamName,"%")then 1 else 0 end)*100)/count(*) as winning_percentage
    from matches 
    where tossStatus!='Not Available'
    and tossStatus is not null 
    group by toss_Status
    """,

    "Q18 - Best Economy Bowlers in ODI and T20 Matches":
    """
    select b.bowlerName, avg(b.economy) as average_economy,sum(b.wickets) as total_wickets,avg(b.overs) as avg_overs_per_match,count(m.matchId) as total_matches 
    from matches m join bowler_scores b on m.matchId=b.matchId
    where m.matchFormat in ("ODI","T20")
    group by b.bowlerId, b.bowlerName
    having count(m.matchId)>=10 and avg(b.overs)>=2
    order by average_economy asc
    """,

    "Q19 - Most Consistent Batsmen Based on Run Standard Deviation":
    """
    select b.batsmanName, avg(b.runs) as average_runs,stddev(b.runs) as standard_deviation_runs 
    from batsman_scores b join matches m on b.matchId = m.matchId
    where year(from_unixtime(m.startDate/1000))>=2022 and b.balls>=10
    group by b.batsmanId,b.batsmanName
    order by standard_deviation_runs asc
    """,

    "Q20 - Player Batting Performance Across Test, ODI and T20 Formats":
    """
    select b.batsmanName,
    count(case when m.matchFormat='TEST' then 1 end) as test_matches,
    count(case when m.matchFormat='ODI' then 1 end) as odi_matches,
    count(case when m.matchFormat='T20I' then 1 end) as t20_matches,
    avg(case when m.matchFormat='TEST' then b.runs end) as test_avg,
    avg(case when m.matchFormat='ODI' then b.runs end) as odi_avg,
    avg(case when m.matchFormat='T20I' then b.runs end) as t20_avg
    from batsman_scores b join matches m on b.matchId = m.matchId
    group by b.batsmanId,b.batsmanName
    having count(b.matchId) >= 20
    """,

    "Q21 - Comprehensive Player Performance Score (Batting + Bowling)":
    """
    select
	p.name,m.matchFormat,
	sum(b.runs) as runs_scored,
	avg(b.runs) as batting_average,
	sum(b.strikeRate) as strike_rate,
	sum(bo.wickets) as wickets_scored,
	sum(bo.runs)/nullif(sum(bo.wickets),0) as average_bowling,
	sum(bo.economy) as total_economy,
	((sum(b.runs) * 0.01) + (avg(b.runs) * 0.5) + (sum(b.strikeRate) * 0.3)) as batting_point,
	((sum(bo.wickets) * 2) + (50 - sum(bo.runs)/nullif(sum(bo.wickets),0)) * 0.5) + ((6 - sum(bo.economy)) * 2) as bowling_points,
	((sum(b.runs) * 0.01) + (avg(b.runs) * 0.5) + (sum(b.strikeRate) * 0.3)) + ((sum(bo.wickets) * 2) + (50 - sum(bo.runs)/nullif(sum(bo.wickets),0)) * 0.5) + ((6 - sum(bo.economy)) * 2) as total_scores
	from players p join batsman_scores b on p.player_id = b.batsmanId
	join bowler_scores bo on p.player_id = bo.bowlerId
	join matches m on b.matchId = m.matchId 
	group by p.player_id, p.name, m.matchFormat
	order by total_scores desc
    """,

    "Q22 - Head-to-Head Team Performance in the Last 3 Years":
    """
    select t1.team_name as team_1, t2.team_name as team_2,
    count(*) as total_match,
    sum(case when t1.team_name = m.winningTeamName then 1 else 0 end) as total_match_won_team_1,
    sum(case when t2.team_name = m.winningTeamName then 1 else 0 end) as total_match_won_team_2,
    avg(case when t1.team_name = m.winningTeamName then m.victoryMargin end ) as team1_avg, 
    avg(case when t2.team_name = m.winningTeamName then m.victoryMargin end ) as team2_avg, 
    sum(case when t1.team_name = m.winningTeamName then 1 else 0 end)*100/count(*) as team1_win_percentage,
    sum(case when t2.team_name = m.winningTeamName then 1 else 0 end)*100/count(*) as team2_win_percentage
    from matches m join teams t1 on m.team1Id=t1.team_id
    join teams t2 on m.team2Id=t2.team_id
    where year(from_unixtime(m.startDate/1000))>year(curdate())-3
    group by t1.team_name,t2.team_name
    having count(*)>=5
    order by total_match desc
    """,

    "Q23 - Recent Player Form Analysis Based on Last 5 and 10 Matches":
    """
    with overall_score as (select b.batsmanId,b.batsmanName,b.runs,b.strikeRate,m.startDate,row_number() over(partition by b.batsmanId order by m.startDate desc) as rn
    from batsman_scores b join matches m on b.matchId=m.matchId)
    select batsmanName,
    avg(case when rn<=5 then runs end) as avg_runs_last_5_matches,
    avg(case when rn<=10 then runs end) as avg_runs_last_10_matches,
    avg(strikeRate) as avg_strike_rate,
    sum(case when runs>=50 then 1 else 0 end) as scores_runs_above_50,
    stddev(runs) as consistency_score,
    case
    when avg(runs)>=50 then "Excellent form"
    when avg(runs)>=35 then "good form"
    when avg(runs)>=20 then "average form"
    else "poor form"
    end as player_form

    from overall_score
    where rn<=10
    group by batsmanId, batsmanName
    order by avg(runs) desc
    """,

    "Q24 - Top Batting Partnerships with Success Rate":
    """
    select bat1Name,bat2Name, avg(totalRuns) as avg_runs_of_2batsman,
    sum(case when totalRuns>= 50 then 1 else 0 end) as excedded_50_runs,
    max(totalRuns) as highest_partnership_runs,
    count(*) as total_partnerships,
    (sum(case when totalRuns >= 50 then 1 else 0 end) * 100) / count(*) as success_rate
    from partnerships
    group by bat1Id, bat2Id, bat1Name, bat2Name
    having count(*) >= 5
    order by success_rate desc
    """,

    "Q25 - Quarterly Player Performance Trend Analysis":
    """
    with quarterly_stats as (
    select
    bs.batsmanId,
    bs.batsmanName,
    year(from_unixtime(m.startDate/1000)) as year,
    quarter(from_unixtime(m.startDate/1000)) as quarter,
    avg(bs.runs) as avg_runs,
    avg(bs.strikeRate) as avg_strike_rate,
    count(bs.matchId) as matches_played
    from batsman_scores bs
    join matches m on bs.matchId = m.matchId
    group by bs.batsmanId, bs.batsmanName, year, quarter
    having count(bs.matchId) >= 3
    ),

    quarterly_trend as (
    select
    batsmanId,
    batsmanName,
    year,
    quarter,
    avg_runs,
    avg_strike_rate,
    lag(avg_runs) over(partition by batsmanId order by year, quarter) as prev_runs
    from quarterly_stats
    )

    select
    batsmanName,
    year,
    quarter,
    avg_runs,
    avg_strike_rate,
    case
    when avg_runs > prev_runs then 'improving'
    when avg_runs < prev_runs then 'declining'
    else 'stable'
    end as performance_trend,

    case
    when avg_runs > prev_runs then 'career ascending'
    when avg_runs < prev_runs then 'career declining'
    else 'career stable'
    end as career_phase

    from quarterly_trend
    where batsmanId in (
    select batsmanId
    from quarterly_stats
    group by batsmanId
    having count(distinct concat(year,'-',quarter)) >= 6
    )
    order by batsmanName, year, quarter
    """

    }
    
    selected_query = st.selectbox("Select the query", query_titles)
    if st.button("Run Query"):

        sql = query_map[selected_query]

        df = pd.read_sql(sql, conn)

        st.dataframe(df)
