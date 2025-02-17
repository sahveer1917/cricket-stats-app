import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("cricket.db")
cursor = conn.cursor()

# Create teams table
cursor.execute("""
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT UNIQUE
);
""")

# Create players table
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT UNIQUE
);
""")

# Create matches table
cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_date TEXT,
    venue TEXT,
    team1 INTEGER,
    team2 INTEGER,
    toss_winner INTEGER,
    toss_decision TEXT,
    winner INTEGER,
    FOREIGN KEY (team1) REFERENCES teams(team_id),
    FOREIGN KEY (team2) REFERENCES teams(team_id),
    FOREIGN KEY (toss_winner) REFERENCES teams(team_id),
    FOREIGN KEY (winner) REFERENCES teams(team_id)
);
""")

# Create innings table
cursor.execute("""
CREATE TABLE IF NOT EXISTS innings (
    inning_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    batting_team INTEGER,
    total_runs INTEGER,
    wickets INTEGER,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (batting_team) REFERENCES teams(team_id)
);
""")

# Create deliveries table
cursor.execute("""
CREATE TABLE IF NOT EXISTS deliveries (
    delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    inning_id INTEGER,
    over_number INTEGER,
    ball_number INTEGER,
    batsman INTEGER,
    bowler INTEGER,
    runs INTEGER,
    wicket INTEGER DEFAULT 0,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (inning_id) REFERENCES innings(inning_id),
    FOREIGN KEY (batsman) REFERENCES players(player_id),
    FOREIGN KEY (bowler) REFERENCES players(player_id)
);
""")

# Commit changes and close connection
conn.commit()
conn.close()

print("Database schema created successfully.")
