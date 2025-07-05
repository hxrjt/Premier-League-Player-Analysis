import streamlit as st
import pandas as pd
from player_img import getPlayerImage
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch, VerticalPitch


def playerHeatMap(data,playerSelect):
    heatData=data[(data['player']==playerSelect) & 
                  (data['x']<=100) & 
                  (data['y']<=100) & 
                  (data['x']>0) & 
                  (data['y']>0)]
    
    pitch = Pitch(pitch_type='opta', pitch_color='grass', line_color='black')
    fig,ax= pitch.draw()
    
    pitch.kdeplot(
    heatData['x'],
    heatData['y'],
    fill=True,
    cmap="Reds",
    alpha=0.8,
    ax=ax
    )

    st.pyplot(fig)


def shotMap(shotData,playerSelect):
    shots=shotData[shotData['player']==playerSelect]
    goals=shots[shots['result']=='Goal']
    missed=shots[shots['result']!='Goal']
    xgGoal=goals['xG']*100
    xgMiss=missed['xG']*100
    totalGoals=goals.shape[0]
    totalMiss=missed.shape[0]
    pitch=VerticalPitch(half=True,pitch_type='metricasports',pitch_color='grass',line_color='black',pitch_length=100,pitch_width=50)
    fig,ax=pitch.draw()
    
    pitch.scatter(goals['X'],goals['Y'],s=xgGoal,ax=ax,color='red',edgecolors='black',label='goal')
    pitch.scatter(missed['X'],missed['Y'],s=xgMiss,ax=ax,color='blue',edgecolors='blue',label='miss',alpha=0.2)
    
    ax.legend(loc='upper right')
    st.pyplot(fig)

teamsDF=pd.read_csv('data/PL_teams.csv')
data=pd.read_parquet('data\ENG_match_events.parquet')
shotData=pd.read_csv('data\epl_team_season_shots.csv')


with st.sidebar:
    
    st.title('Premier League Player Analysis')
    
    teams=data['team'].unique()
    teams.sort()

    teamSelect=st.selectbox("Select Team",teams)
    
    players=data[data['team']==teamSelect]
    players=players['player'].unique()
        
    playerSelect=st.selectbox("Select Player",players)
    
    logo_path = teamsDF[teamsDF["team_name"] == teamSelect]["logo_url"].values[0]
    
    st.image(logo_path)
    analyse=st.button("Analysis")



st.title('Player Analysis 24/25 Season')

imgURL=getPlayerImage(playerSelect)

if analyse:
    st.title(playerSelect)
    if imgURL:
        st.image(imgURL,width=250)
    else:
        st.write("😔 Can't display the fifa card becuase the free api can handle only 100 requests/day")
    st.title(f"{playerSelect} HeatMap 🔥")
    playerHeatMap(data,playerSelect)
    st.title(f"{playerSelect} Shots with xG")
    shotMap(shotData,playerSelect)