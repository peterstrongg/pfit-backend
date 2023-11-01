import unittest
import sqlite3
from Database import Database

db = Database("pfit.db")

# For cleanup routines after tests complete
conn = sqlite3.connect("pfit.db")
curs = conn.cursor()

# Cleanup routines after tests conclude
def cleanup_users():
    curs.execute(
        "DELETE FROM users WHERE username = ?", 
        ["pfitDemo"]
    )
    conn.commit()

class TestDatabase(unittest.TestCase):
    def test_signup(self):
        self.assertTrue(db.add_user("pfitDemo", "password"))
        cleanup_users()

if __name__ == "__main__":
    unittest.main()
    