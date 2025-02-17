from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Allow frontend to call API

# Function to fetch data from SQLite database
def query_db(query, args=(), one=False):
    conn = sqlite3.connect("cricket.db")
    cursor = conn.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
    conn.close()
    return (result[0] if result else None) if one else result

# 1. API to Get All Matches
@app.route('/api/matches', methods=['GET'])
def get_matches():
    matches = query_db("""
        SELECT matches.match_id, match_date, venue, 
               team1.team_name AS team1, team2.team_name AS team2, 
               winner_team.team_name AS winner
        FROM matches
        JOIN teams AS team1 ON matches.team1 = team1.team_id
        JOIN teams AS team2 ON matches.team2 = team2.team_id
        JOIN teams AS winner_team ON matches.winner = winner_team.team_id;
    """)
    
    return jsonify([
        {"match_id": m[0], "date": m[1], "venue": m[2], "team1": m[3], "team2": m[4], "winner": m[5]}
        for m in matches
    ])

# 2. API to Get Top 5 Batsmen
@app.route('/api/top_batsmen', methods=['GET'])
def get_top_batsmen():
    batsmen = query_db("""
        SELECT players.player_name, SUM(deliveries.runs) AS total_runs
        FROM deliveries
        JOIN players ON deliveries.batsman = players.player_id
        GROUP BY players.player_name
        ORDER BY total_runs DESC
        LIMIT 5;
    """)
    
    return jsonify([{"player_name": b[0], "total_runs": b[1]} for b in batsmen])

# 3. API to Get Top 5 Bowlers
@app.route('/api/top_bowlers', methods=['GET'])
def get_top_bowlers():
    bowlers = query_db("""
        SELECT players.player_name, COUNT(deliveries.wicket) AS total_wickets
        FROM deliveries
        JOIN players ON deliveries.bowler = players.player_id
        WHERE deliveries.wicket = 1
        GROUP BY players.player_name
        ORDER BY total_wickets DESC
        LIMIT 5;
    """)
    
    return jsonify([{"player_name": b[0], "total_wickets": b[1]} for b in bowlers])

# 4. AI Query System
@app.route('/api/ask', methods=['POST'])
def ask_ai():
    user_question = request.json.get("question", "").lower()

    query_map = {
        "highest boundary count": """
            SELECT player_name, SUM(runs) AS boundaries 
            FROM deliveries 
            JOIN players ON deliveries.batsman = players.player_id 
            WHERE runs IN (4,6) 
            GROUP BY player_name 
            ORDER BY boundaries DESC LIMIT 1;
        """,
        "best strike rate bowler": """
            SELECT player_name, (SUM(runs) * 100.0 / COUNT(delivery_id)) AS strike_rate 
            FROM deliveries 
            JOIN players ON deliveries.bowler = players.player_id 
            WHERE COUNT(delivery_id) > 300 
            GROUP BY player_name 
            ORDER BY strike_rate ASC LIMIT 1;
        """
    }

    query = query_map.get(user_question, None)

    if query:
        result = query_db(query, one=True)
        return jsonify({"answer": result})
    else:
        return jsonify({"error": "I don't understand the question"}), 400

# Run Flask App (ALWAYS at the end)
if __name__ == '__main__':
    app.run(debug=True)
