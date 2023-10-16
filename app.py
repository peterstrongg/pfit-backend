from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    make_response,
    redirect,
    send_file
)
from flask_cors import CORS
from datetime import timedelta
from GarminApi import GarminApi
from Database import Database
from Graph import Graph
import os
import json

app = Flask(__name__, static_folder="build/static", template_folder="build")
CORS(app)

@app.route("/")
@app.route("/login")
@app.route("/signup")
@app.route("/dashboard")
@app.route("/healthinfo")
@app.route("/workout")
@app.route("/progress")
@app.route("/social")
@app.route("/onerepmax")
def render_app():
    return render_template("index.html")

@app.route("/api/login", methods=["POST"])
def login():
    credentials = json.loads(request.json)
    username = credentials["username"]
    password = credentials["password"]

    db = Database("pfit.db")
    uid = db.get_user_id(username, password)

    response = jsonify({
        "sessionId" : uid,
        "username" : username,
    })

    return response

@app.route("/api/signup", methods=["POST"])
def signup():
    credentials = json.loads(request.json)
    username = credentials["username"]
    password = credentials["password"]

    db = Database("pfit.db")
    uid = db.add_user(username, password)
    if uid:
        return make_response(redirect("/login"))
    else:
        return ("", 204)

@app.route("/api/garmin", methods=["POST"])
def garmin():
    credentials = json.loads(request.json)
    username = credentials["username"]
    password = credentials["password"]
    # user_id = credentials["user_id"]

    gmn = GarminApi(username, password)
    step_data = gmn.get_step_data()
    hr_data = gmn.get_hr_data()

    response = jsonify({
        "steps" : step_data["steps"],
        "stepGoal" : step_data["step_goal"],
        "stepsToGoal" : step_data["step_goal"] - step_data["steps"],
        "currentHr" : hr_data["current_hr"],
        "avgRestingHr" : hr_data["avg_resting_hr"], 
    })

    db = Database("pfit.db")

    return response

@app.route("/api/workouts", methods=["GET"])
def get_workouts():
    db = Database("pfit.db")
    exercise_list = db.get_exercises()
    response = []
    for e in exercise_list:
        response.append([e[1], e[2]])

    return response

@app.route("/api/log_workout", methods=["POST"])
def log_workout():
    workout_data = json.loads(json.dumps(request.json))
    exercise_name = workout_data["exercise_name"]
    user_id = workout_data["user_id"]
    sets = workout_data["sets"]
    reps = workout_data["reps"]
    weight = workout_data["weight"]

    db = Database("pfit.db")
    db.log_workout(exercise_name, user_id, sets, reps, weight, 0)

    return ("OK", 200)

@app.route("/api/workout_history", methods=["POST"])
def workout_history():
    data = json.loads(json.dumps(request.json))
    user_id = data["user_id"]

    db = Database("pfit.db")
    history = db.get_workout_history(user_id)
    
    return history

@app.route("/api/monitor_progress", methods=["GET"])
def monitor_progress():
    data = request.args
    user_id = data["user_id"]
    exercise_name = data["exercise_name"]

    g = Graph(user_id, exercise_name)
    file_name = g.generate_graph()

    return send_file(file_name)
    
if __name__ == "__main__":
    app.run()
    