import sqlite3

db = sqlite3.connect("pfit.db")
cursor = db.cursor()

def print_table(table_name):
    cursor.execute("SELECT * FROM " + table_name)
    records = cursor.fetchall()
    for r in records:
        print(r)

# Users Table
print_table("users")