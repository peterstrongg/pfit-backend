import sqlite3
from hashlib import sha256
from datetime import datetime

class Database:
    def __init__(self, conn):
        self.conn = sqlite3.connect(conn)
        self.curs = self.conn.cursor()

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

    def add_user(self, username, password):
        uid = self.__get_next_uid("users")
        self.curs.execute(
            "INSERT INTO users VALUES (?,?,?)",
            [uid, username, self.__hash_password(password)]
        )
        self.conn.commit()
        return uid

    def get_exercises(self):
        self.curs.execute(
            "SELECT * FROM workout"
        )
        return self.curs.fetchall()
    
    def log_workout(self, exercise_name, user_id, sets, reps, weight, duration):
        lid = self.__get_next_uid("logging")
        eid = self.__get_eid_by_name(exercise_name)
        today = datetime.today().strftime("%Y-%m-%d")

        self.curs.execute(
            "INSERT INTO logging VALUES(?,?,?,?,?,?,?,?)",
            [lid, eid, user_id, today, sets, reps, weight, duration]
        )
        self.conn.commit()

        return lid
    
    def get_workout_history(self, user_id):
        self.curs.execute(
            "SELECT * FROM logging WHERE user_id = ?",
            [user_id]
        )
        data = self.curs.fetchall()

        history = []
        for workout in data:
            history.append([
                self.__get_exercise_name_by_eid(workout[1]),    # Exercise name
                workout[3],     # date
                workout[4],     # sets
                workout[5],     # reps
                workout[6],     # weight
                workout[7]      # duration
            ])

        return history
    # Private members

    def __hash_password(self, password):
        return sha256(password.encode('utf-8')).hexdigest()

    def __get_next_uid(self, table_name):
        self.curs.execute(
            "SELECT * FROM " + table_name
        )
        data = self.curs.fetchall()
        if bool(data):
            return data[-1][0] + 1
        return 1
    
    def __get_eid_by_name(self, exercise_name):
        self.curs.execute(
            "SELECT exercise_id FROM workout WHERE exercise_name = ?",
            [exercise_name]
        )
        data = self.curs.fetchall()
        return data[0][0]
    
    def __get_exercise_name_by_eid(self, eid):
        self.curs.execute(
            "SELECT exercise_name FROM workout WHERE exercise_id = ?",
            [eid]
        )
        data = self.curs.fetchall()
        return data[0][0]
