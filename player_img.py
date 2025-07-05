import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
GOOGLE_CX=os.getenv("GOOGLE_CX_API_KEY")

def getPlayerImage(playerName):
    query=f"{playerName} site:ea.com/games/ea-sports-fc/ratings"
    url=f"https://www.googleapis.com/customsearch/v1"
    param={
        "key":GOOGLE_API_KEY,
        "cx":GOOGLE_CX,
        "q":query,
        "searchType":"image",
        "num":1
    }
    try:
        response=requests.get(url,params=param)
        data=response.json()
        if "items" in data:
            return data['items'][0]['link']
    
    except Exception as e:
        return e
