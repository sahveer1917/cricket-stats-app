import json
import sqlite3
import os

# Database connection
conn = sqlite3.connect("cricket.db")
cursor = conn.cursor()

# Folder where all IPL JSON files are stored
ipl_folder = "ipl_matches"

# Function to process multiple IPL matches
def process_ipl_matches():
    for filename in os.listdir(ipl_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(ipl_folder, filename)
            print(f"Processing {file_path}...")

            # Open and load the JSON file
            with open(file_path, "r") as file:
                data = json.load(file)

            # Extract match info
            match_info = data["info"]
            teams = match_info["teams"]

            # Insert teams (if not already present)
            for team in teams:
                cursor.execute("INSERT OR IGNORE INTO teams (team_name) VALUES (?)", (team,))
            conn.commit()

            # Get team IDs
            cursor.execute("SELECT team_id, team_name FROM teams")
            team_map = {name: id for id, name in cursor.fetchall()}

            # Insert match details
            cursor.execute(
                """INSERT INTO matches (match_date, venue, team1, team2, toss_winner, toss_decision, winner)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    match_info["dates"][0],
                    match_info["venue"],
                    team_map[teams[0]],
                    team_map[teams[1]],
                    team_map.get(match_info["toss"]["winner"], None),
                    match_info["toss"]["decision"],
                    team_map.get(match_info["outcome"].get("winner", ""), None),
                ),
            )
            match_id = cursor.lastrowid
            conn.commit()

            # Insert players (if not already present)
            players = {p: None for p in match_info["players"][teams[0]] + match_info["players"][teams[1]]}
            for player in players.keys():
                cursor.execute("INSERT OR IGNORE INTO players (player_name) VALUES (?)", (player,))
            conn.commit()

            # Fetch player IDs
            cursor.execute("SELECT player_id, player_name FROM players")
            player_map = {name: id for id, name in cursor.fetchall()}

            # Insert innings and deliveries
            for inning_data in data["innings"]:
                batting_team = inning_data["team"]
                cursor.execute(
                    """INSERT INTO innings (match_id, batting_team, total_runs, wickets) 
                       VALUES (?, ?, ?, ?)""",
                    (match_id, team_map[batting_team], 0, 0),
                )
                inning_id = cursor.lastrowid
                conn.commit()

                # Insert deliveries
                for over_data in inning_data["overs"]:
                    over_num = over_data["over"]
                    for delivery_index, ball_data in enumerate(over_data["deliveries"], start=1):
                        batsman = player_map.get(ball_data["batter"], None)
                        bowler = player_map.get(ball_data["bowler"], None)
                        runs = ball_data["runs"]["total"]
                        wicket = 1 if "wickets" in ball_data else 0

                        cursor.execute(
                            """INSERT INTO deliveries (match_id, inning_id, over_number, ball_number, batsman, bowler, runs, wicket)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                            (match_id, inning_id, over_num, delivery_index, batsman, bowler, runs, wicket),
                        )

                conn.commit()

# Run the function to process all matches
process_ipl_matches()

# Close the connection
conn.close()
