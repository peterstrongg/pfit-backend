import sqlite3
import sys

db = sqlite3.connect("pfit.db")
cursor = db.cursor()

table_creation_queries = [
        # Users table
''' 
CREATE TABLE IF NOT EXISTS users (
    uid INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)
''',    # Workout list table
'''
CREATE TABLE IF NOT EXISTS workout (
    exercise_id INTEGER PRIMARY KEY,
    exercise_name TEXT UNIQUE,
    muscle_group TEXT
)
''',    # Logging Table
''' 
CREATE TABLE IF NOT EXISTS logging (
    workout_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    date DATE,
    sets INT,
    reps INT,
    weight DECIMAL(5, 2),
    duration_mins INT
)
'''
]

# delete tables
if len(sys.argv) > 2 and sys.argv[1] == "del":
    for table in sys.argv[2:]:
        print("Deleting", table, "table...")
        cursor.execute("DROP TABLE IF EXISTS " + table)

# create new tables
print("Making new tables...")
for t in table_creation_queries:
    cursor.execute(t)
