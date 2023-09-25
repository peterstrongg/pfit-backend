import sqlite3
import sys

db = sqlite3.connect("pfit.db")
cursor = db.cursor()

create_users_table = '''
CREATE TABLE IF NOT EXISTS users (
    uid INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)
'''

create_workout_table = '''
CREATE TABLE IF NOT EXISTS workout (
    exercise_id INTEGER PRIMARY KEY,
    exercise_name TEXT UNIQUE,
    muscle_group TEXT
)
'''

# delete tables
if len(sys.argv) > 2 and sys.argv[1] == "del":
    for table in sys.argv[2:]:
        print("Deleting", table, "table...")
        cursor.execute("DROP TABLE IF EXISTS " + table)

# create new tables
print("Making new tables...")
cursor.execute(create_users_table)
cursor.execute(create_workout_table)
