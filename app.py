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
    shots=shotData[(shotData['player']==playerSelect) & (shotData['is_shot']=='1')]
    goals=shots[shots['is_goal']=='1']
    missed=shots[shots['is_goal']!='1']
    totalGoals=goals.shape[0]
    totalShots=shots.shape[0]
    converionRate=(totalGoals/totalShots)*100
    pitch=VerticalPitch(half=True,pitch_type='opta',pitch_color='grass',line_color='black')
    fig,ax=pitch.draw(figsize=(5,10))
    
    pitch.scatter(goals['x'],goals['y'],ax=ax,color='red',edgecolors='black',label='goal')
    pitch.scatter(missed['x'],missed['y'],ax=ax,color='blue',edgecolors='blue',label='miss',alpha=0.2)
    
    ax.legend(loc='upper right')
    st.pyplot(fig)
    
    st.markdown(f"### Goal Conversion Rate")
    st.markdown(f"- Total Shots: **{totalShots}**")
    st.markdown(f"- Goals: **{totalGoals}**")
    st.markdown(f"- Conversion Rate: **{converionRate:.2f}%**")
    
    
def passNetwork(passData,playerSelect):
    passes=passData[(passData['type']=='Pass') & (passData['player']==playerSelect)]
    successPass=passes[passes['outcome_type']=='Successful']
    unsuccessPass=passes[passes['outcome_type']=='Unsuccessful']
    totalPass=passes.shape[0]
    completePass=successPass.shape[0]
    passingAccuracy=(completePass/totalPass)*100
    
    pitch=Pitch(pitch_type='opta',pitch_color='grass',line_color='black')
    fig,ax=pitch.draw()
    
    pitch1=Pitch(pitch_type='opta',pitch_color='grass',line_color='black')
    fig1,ax1=pitch1.draw()
    
    #success pass
    pitch.scatter(successPass['x'],successPass['y'],color='red',edgecolors='black',label='Successful pass',ax=ax, s=10)
    pitch.lines(successPass['x'],successPass['y'],successPass['end_x'],successPass['end_y'],ax=ax,color='red',lw=0.5)
    
    #unsuccess pass
    pitch.scatter(unsuccessPass['x'],unsuccessPass['y'],color='blue',edgecolors='blue',label='Unsuccessful pass',ax=ax1, s=10,alpha=0.2)
    pitch.lines(unsuccessPass['x'],unsuccessPass['y'],unsuccessPass['end_x'],unsuccessPass['end_y'],ax=ax1,color='blue',lw=0.5)
    
    ax.legend(loc='upper right')
    st.pyplot(fig)
    
    ax1.legend(loc='upper right')
    st.pyplot(fig1)
    st.markdown(f"### Passing Accuracy")
    st.markdown(f"- Total Passes: **{totalPass}**")
    st.markdown(f"- Successful Passes: **{completePass}**")
    st.markdown(f"- Accuracy: **{passingAccuracy:.2f}%**")



teamsDF=pd.read_csv('data/PL_teams.csv')
data=pd.read_parquet('data\ENG_match_events.parquet')
# Incomplete Data
# shotData=pd.read_csv('data\epl_team_season_shots.csv')


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
    st.title(f"{playerSelect}'s HeatMap")
    playerHeatMap(data,playerSelect)
    st.title(f"{playerSelect}'s Shots")
    shotMap(data,playerSelect)
    st.title(f"{playerSelect}'s Pass Network")
    passNetwork(data,playerSelect)