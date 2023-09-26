import sqlite3

db = sqlite3.connect("pfit.db")
cursor = db.cursor()

# Add exercises here
exercises = [
    ["Bench Press", "Chest"],
    ["Incline Bench Press", "Upper Chest"],
    ["Decline Bench Press", "Lower Chest"],
    ["Shoulder Press", "Shoulders"],
    ["Deadlift", "Back"],
    ["Rows", "Back"],
    ["Bicep Curls", "Biceps"],
    ["Lateral Raises","Shoulders"],
    ["Tricep Pushdown", "Triceps"],
    ["Barbell Squats", "Upper Legs"],
    ["Calve Extensions", "Calves"],
    ["Leg Press", "Upper Legs"],
    ["Tricep Extension", "Triceps"],
    ["Lateral Pulldown", "Back"],
]

def get_next_uid():
    cursor.execute("SELECT * FROM workout")
    data = cursor.fetchall()
    if bool(data):
        return data[-1][0] + 1
    return 1

for e in exercises:
    try:
        cursor.execute(
            "INSERT INTO workout VALUES (?,?,?)",
            [get_next_uid(), e[0], e[1]]
        )
        db.commit()
    except:
        continue
    