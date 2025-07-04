import streamlit as st
import pandas as pd
from player_img import getPlayerImage

teamsDF=pd.read_csv('data/PL_teams.csv')
playersDF=pd.read_csv('data/Player.csv')
with st.sidebar:
    
    st.title('Premier League Player Analysis')

    teamSelect=st.selectbox("Select Team",teamsDF['team_name'])
    players=playersDF[playersDF['Team']==teamSelect]
    playerSelect=st.selectbox("Select Player",players['Player'].unique())
    logo_path = teamsDF[teamsDF["team_name"] == teamSelect]["logo_url"].values[0]
    st.image(logo_path)
    analyse=st.button("Analysis")

playerInfo=playersDF[playersDF['Player']==playerSelect].iloc[0]

st.title('Player Analysis 24/25 Season')
if analyse:
    st.title(playerSelect)
    imgURL=getPlayerImage(playerSelect, teamSelect)
    if imgURL:
        st.image(imgURL,width=250)