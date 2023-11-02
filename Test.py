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

def cleanup_sw():
    curs.execute(
        "DELETE from share_workout WHERE logging_id = ?",
        [-1]
    )
    conn.commit()

class TestDatabase(unittest.TestCase):
    def test_signup(self):
        self.assertTrue(db.add_user("pfitDemo", "password"))
        cleanup_users()

    def test_share_workout(self):
        self.assertTrue(db.share_workout(1, -1, "Comment"))
        cleanup_sw()

if __name__ == "__main__":
    unittest.main()
    