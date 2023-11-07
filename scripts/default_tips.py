import sqlite3

db = sqlite3.connect("pfit.db")
cursor = db.cursor()

# Add exercises here
tips = [
    "Drink a lot of water!",
    "Stretch before you workout!",
    "Sleep at least 8 hours a night!",
]

def get_next_uid():
    cursor.execute("SELECT * FROM tips")
    data = cursor.fetchall()
    if bool(data):
        return data[-1][0] + 1
    return 1

for t in tips:
    try:
        cursor.execute(
            "INSERT INTO tips VALUES (?,?,?)",
            [get_next_uid(), -1, t]
        )
        db.commit()
    except:
        continue
    