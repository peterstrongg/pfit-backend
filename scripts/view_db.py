import sqlite3

db = sqlite3.connect("pfit.db")
cursor = db.cursor()

def print_table(table_name):
    print(table_name, "table\n--------------")
    cursor.execute("SELECT * FROM " + table_name)
    records = cursor.fetchall()
    for r in records:
        print(r)
    print("\n")

# print tables
print_table("users")
print_table("workout")
print_table("logging")