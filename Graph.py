import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from Database import Database

class Graph:
    def __init__(self, user_id=-1, exercise_name=""):
        self.uid = user_id
        self.ename = exercise_name
        self.db = Database("pfit.db")

    def set_uid(self, user_id):
        self.uid = user_id

    def set_ename(self, exercise_name):
        self.ename = exercise_name

    def generate_graph(self):
        history = self.__get_history()
        file_name = self.__generate_file_name()

        if os.path.exists(file_name):       # Delete old file before making new graph
            os.remove(file_name)  

        dates = np.array([])                # x-axis
        lift = np.array([])                 # y-axis
        for log in history:
            dates = np.append(dates, log[3])
            lift = np.append(lift, log[6])

        if len(dates) == 0:                 # Return early if no data
            return "assets/defaultimage.png"

        # Generating Graph
        plt.title(self.ename)
        plt.xlabel("Dates")
        plt.ylabel("Weight (lbs)")
        plt.scatter(dates, lift, color='green') # Dots
        plt.plot(dates, lift, 'green')          # Lines
        plt.xticks(rotation=-60)
        plt.subplots_adjust(bottom=0.3)
        plt.savefig(file_name)
        plt.clf()                           # Clears figure

        return file_name


    # Private Members

    def __get_history(self):
        return self.db.get_workout_history_by_name(self.uid, self.ename)
    
    def __generate_file_name(self):
        fname = "graphs/" + str(self.uid) + "_" + self.ename + ".png"
        return fname
