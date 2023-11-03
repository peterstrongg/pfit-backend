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
    
    def log_garmin(self, user_id, steps, step_goal, current_hr, avg_hr):
        gid = self.__get_next_uid("garmin")
        today = datetime.today().strftime("%Y-%m-%d")

        self.curs.execute(
            "INSERT INTO garmin VALUES(?,?,?,?,?,?,?)",
            [gid, user_id, today, steps, step_goal, current_hr, avg_hr]
        )
        self.conn.commit()

        return gid
    
    def share_workout(self, uid, wid, comment):
        gid = self.__get_next_uid("share_workout")

        self.curs.execute(
            "INSERT INTO share_workout VALUES(?,?,?,?)",
            [gid, uid, wid, comment]  
        )
        self.conn.commit()

        return gid
    
    def share_tip(self, uid, tip):
        tid = self.__get_next_uid("tips")

        self.curs.execute(
            "INSERT INTO tips VALUES(?,?,?)",
            [tid, uid, tip]
        )
        self.conn.commit()

        return tid

    def get_workout_history(self, user_id):
        self.curs.execute(
            "SELECT * FROM logging WHERE user_id = ?",
            [user_id]
        )
        data = self.curs.fetchall()

        history = []
        for workout in data:
            history.append({
                "logId" : workout[0],
                "exerciseName" : self.__get_exercise_name_by_eid(workout[1]),    # Exercise name
                "date" : workout[3],     # date
                "sets" : workout[4],     # sets
                "reps" : workout[5],     # reps
                "weight" : workout[6],     # weight
                "duration" : workout[7]      # duration
            })

        return history
    
    def get_workout_history_by_name(self, user_id, ename):
        eid = self.__get_eid_by_name(ename)
        self.curs.execute(
            "SELECT * FROM logging WHERE user_id = ? AND exercise_id = ?",
            [user_id, eid]
        )
        data = self.curs.fetchall()

        return data
    
    def get_shared_workouts(self):
        self.curs.execute("SELECT * FROM share_workout")
        sw_data = self.curs.fetchall()

        sw_final = []        
        for row in sw_data:
            log = self.__get_log_by_lid(row[2])
            sw_final.append([
                self.__get_uname_by_uid(row[1]),            # Username
                log[0][3],                                  # Date
                self.__get_exercise_name_by_eid(log[0][1]), # Exercise Name
                log[0][4],                                  # Sets
                log[0][5],                                  # Reps
                log[0][6],                                  # Weight
                row[3],                                     # Comment
            ])

        return sw_final
    
    def get_tips(self):
        self.curs.execute("SELECT * FROM tips")
        tips = self.curs.fetchall()
        return tips
      
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
    
    def __get_uname_by_uid(self, uid):
        self.curs.execute(
            "SELECT username FROM users WHERE uid = ?",
            [uid]
        )
        data = self.curs.fetchall()
        return data[0][0]

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
    
    def __get_log_by_lid(self, lid):
        self.curs.execute(
            "SELECT * FROM logging WHERE logging_id = ?",
            [lid]
        )
        data = self.curs.fetchall()
        return data
    
# db = Database("pfit.db")
# db.share_tip(2, "Test tip")
