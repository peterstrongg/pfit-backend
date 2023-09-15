import sqlite3

db = sqlite3.connect("pfit.db")
cursor = db.cursor()

del_table = "DROP TABLE IF EXISTS users"
cursor.execute(del_table)

create_users_table = '''
CREATE TABLE IF NOT EXISTS users (
    uid INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)
'''
cursor.execute(create_users_table)
