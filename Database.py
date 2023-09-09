import sqlite3
from hashlib import sha256

class Database:
    def __init__(self, conn):
        self.conn = sqlite3.connect(conn)
        self.curs = self.conn.cursor()

    def get_session_id(self, username, password):
        self.curs.execute(
            "SELECT uid FROM users WHERE username = ? AND password = ?",
            [username, self.__hash_password(password)]
        )
        try:
            uid = self.curs.fetchone()[0]
            return uid
        except TypeError:
            return 0

    # END get_session_id()

    def __hash_password(self, password):
        return sha256(password.encode('utf-8')).hexdigest()
    
    # END __hash_password()

# db = Database("pfit.db")
# print(db.get_session_id("testuser1", "password")) 