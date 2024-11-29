import requests
#Legit WTF. Why can you not serach Their API by player ID. 
#For compute reasons I will run this function at container startup

# Global dictionary to store player data
players_data = {}

# Fetch player data when the app starts
def fetch_players():
    global players_data
    url = "https://api.sleeper.app/v1/players/nfl"
    response = requests.get(url)
    if response.status_code == 200:
        players_data = response.json()
    else:
        print("Failed to fetch player data")
        
fetch_players()
