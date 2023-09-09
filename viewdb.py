import sqlite3

db = sqlite3.connect("pfit.db")
cursor = db.cursor()

q = "SELECT * FROM users"
cursor.execute(q)
records = cursor.fetchall()

for r in records:
    print(r)