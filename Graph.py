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

        dates = []
        lift = []
        for log in history:
            dates.append(log[3])
            lift.append(log[6])

        x = np.array(dates)
        y = np.array(lift)
        
        plt.plot(x, y)
        plt.show()

        return history


    # Private Members

    def __get_history(self):
        return self.db.get_workout_history_by_name(self.uid, self.ename)


g = Graph(1, "Deadlift")
print(g.generate_graph())