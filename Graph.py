import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from Database import Database

class Graph:
    def __init__(self, user_id, exercise_name):
        self.uid = user_id
        self.ename = exercise_name
        self.db = Database("pfit.db")

    def generate_graph(self):
        history = self.__get_history()
        file_name = self.__generate_file_name()

        dates = np.array([])    # x-axis
        lift = np.array([])     # y-axis
        for log in history:
            dates = np.append(dates, log[3])
            lift = np.append(lift, log[6])

        plt.plot(dates, lift)
        plt.savefig(file_name)
        # plt.show()

        return file_name


    # Private Members

    def __get_history(self):
        return self.db.get_workout_history_by_name(self.uid, self.ename)
    
    def __generate_file_name(self):
        fname = "graphs/" + str(self.uid) + "_" + self.ename + ".png"
        return fname


# g = Graph(1, "Deadlift")
# g.generate_graph()