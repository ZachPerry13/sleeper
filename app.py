import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, send_file, request, redirect, url_for
from team_mapping import fetch_team_names
from fetch_players import  fetch_players, players_data
import requests

#Intialize
app = Flask(__name__)
fetch_players()
players_data = players_data
roster_id_to_team_name = fetch_team_names()

@app.route('/', methods=['GET', 'POST'])
def home():
    
    # Default to week 1 if no week is selected
    week = request.args.get('week', 1, type=int)

    # Fetch league matchups data for the selected week
    url = f"https://api.sleeper.app/v1/league/1117487595728089088/matchups/{week}"
    response = requests.get(url)
    data = response.json()

    # Group data by matchup_id
    matchup_groups = {}

    for matchup in data:
        roster_id = matchup['roster_id']
        points = matchup['points']
        matchup_id = matchup['matchup_id']
        team_name = roster_id_to_team_name.get(roster_id, "Unknown Team")

        if matchup_id not in matchup_groups:
            matchup_groups[matchup_id] = []

        matchup_groups[matchup_id].append((team_name, points))

    # Prepare data for the graph
    team_names = []
    scores = []
    matchup_ids = []

    for matchup_id, teams in matchup_groups.items():
        for team_name, points in teams:
            team_names.append(team_name)
            scores.append(points)
            matchup_ids.append(matchup_id)

    # Pass data to the template
    return render_template(
        'index.html',
        team_names=team_names,
        scoress=scores,
        matchup_ids=matchup_ids,
        week=week
    )



@app.route('/change_week', methods=['POST'])
def change_week():
    # Fetch the selected week from the form
    selected_week = request.form.get('week')
    return redirect(f"/?week={selected_week}")

@app.route('/breakdown', methods=['GET'])
def breakdown():
    team = request.args.get('team')
    matchup_id = request.args.get('matchup')
    week = request.args.get('week', 1, type=int)  # Default to week 1 if not provided

    if not matchup_id or not team:
        return "Invalid matchup or team", 400  # Return a 400 error if invalid parameters

    # Convert matchup_id to int safely
    try:
        matchup_id = int(matchup_id)
    except ValueError:
        return "Invalid matchup ID format", 400

    # Fetch league matchups data for the selected week
    url = f"https://api.sleeper.app/v1/league/1117487595728089088/matchups/{week}"
    response = requests.get(url)
    matchups = response.json()

    # Find the relevant matchup and starters
    starters = []
    for matchup in matchups:
        if matchup.get('matchup_id') == matchup_id and roster_id_to_team_name.get(matchup['roster_id']) == team:
            starters = matchup.get('starters', [])
            starters_points = matchup.get('starters_points', [])  # Get the points for starters
            break

    # Fetch player details for starters using players_data
    starter_details = []
    for idx, player_id in enumerate(starters):  # Using 'enumerate' to get the index of each starter
        player = players_data.get(str(player_id), {})  # Ensure player_id is a string
        points = starters_points[idx] if idx < len(starters_points) else 0  # Get points for the current player
        
        starter_details.append({
            'name': player.get('full_name', 'Unknown'),
            'position': player.get('position', 'Unknown'),
            'team': player.get('team', 'Unknown'),
            'points': points  # Add the points here
        })


    return render_template(
        'breakdown.html',
        team=team,
        week=week,
        matchup_id=matchup_id,
        starter_details=starter_details
    )




if __name__ == '__main__':
    app.run(debug=True)
