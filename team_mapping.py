# team_mapping.py
# Sleeper has the worst API ever, mapping Roster ID to Team names
import requests

def fetch_team_names():
    # URL for the user and rosters data
    league_id = "1117487595728089088"
    user_url = f"https://api.sleeper.app/v1/league/{league_id}/users"
    roster_url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"

    # Step 1: Fetch the users data
    user_response = requests.get(user_url)
    users = user_response.json()

    # Create a dictionary to map user_id to team_name with error handling
    user_id_to_team = {}
    for user in users:
        try:
            # Ensure 'display_name' exists
            team_name = user['display_name']
            user_id = user['user_id']
            user_id_to_team[user_id] = team_name
        except KeyError:
            # Handle missing 'display_name' gracefully
            print(f"Warning: Missing display_name for user_id {user['user_id']}")

    # Step 2: Fetch the rosters data
    roster_response = requests.get(roster_url)
    rosters = roster_response.json()

    # Step 3: Create a mapping of roster_id to team_name based on owner_id
    roster_id_to_team_name = {}
    for roster in rosters:
        owner_id = roster.get('owner_id')
        if owner_id in user_id_to_team:
            team_name = user_id_to_team[owner_id]
            roster_id = roster.get('roster_id')
            roster_id_to_team_name[roster_id] = team_name

    return roster_id_to_team_name
