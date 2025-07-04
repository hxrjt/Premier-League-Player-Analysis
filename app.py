import streamlit as st
import pandas as pd
from player_img_info import getPlayerImage, getPlayerInfo
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch

def playerHeatMap(data,playerSelect):
    heatData=data[(data['player']==playerSelect) & 
                  (data['x']<=100) & 
                  (data['y']<=100) & 
                  (data['x']>0) & 
                  (data['y']>0)]
    
    pitch = Pitch(pitch_type='opta', pitch_color='grass', line_color='black')
    fig,ax= pitch.draw(figsize=(12,10))
    
    pitch.kdeplot(
    heatData['x'],
    heatData['y'],
    fill=True,
    cmap="Reds",
    alpha=0.8,
    ax=ax
    )

    st.pyplot(fig)

teamsDF=pd.read_csv('data/PL_teams.csv')
playersDF=pd.read_csv('data/Player.csv')
data=pd.read_parquet('data\ENG_match_events.parquet')

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

imgURL=getPlayerImage(playerSelect)
info=getPlayerInfo(playerSelect,teamSelect)

if analyse:
    st.title(playerSelect)
    if imgURL:
        st.image(imgURL,width=250)
    else:
        st.write("😔 Can't display the fifa card becuase the free api can handle only 100 requests/day")
    if info:
        st.write(info)
    st.title(f"{playerSelect} Heat Map")
    playerHeatMap(data,playerSelect)