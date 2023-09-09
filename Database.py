import sqlite3
from hashlib import sha256

class Database:
    def __init__(self, conn):
        self.conn = sqlite3.connect(conn)
        self.curs = self.conn.cursor()

    # END __init__

    def get_user_id(self, username, password):
        self.curs.execute(
            "SELECT uid FROM users WHERE username = ? AND password = ?",
            [username, self.__hash_password(password)]
        )
        try:
            uid = self.curs.fetchone()[0]
            return uid
        except TypeError:
            return 0

    # END get_session_id

    def add_user(self, username, password):
        uid = self.__get_next_uid()
        self.curs.execute(
            "INSERT INTO users VALUES (?,?,?)",
            [uid, username, self.__hash_password(password)]
        )
        self.conn.commit()
        return uid

    # END add_user

    def __hash_password(self, password):
        return sha256(password.encode('utf-8')).hexdigest()

    def __get_next_uid(self):
        self.curs.execute(
            "SELECT * FROM users"
        )
        data = self.curs.fetchall()
        if bool(data):
            return data[-1][0] + 1
        return 1
    
    # END __hash_password

# END Database Class
