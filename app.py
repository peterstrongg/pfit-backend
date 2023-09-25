from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    make_response,
    redirect,
)
from flask_cors import CORS
from datetime import timedelta
from GarminApi import GarminApi
from Database import Database
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

    return response

@app.route("/api/workouts", methods=["GET"])
def get_workouts():
    db = Database("pfit.db")
    exercise_list = db.get_exercises()
    response = []
    for e in exercise_list:
        response.append([e[1], e[2]])

    return response

if __name__ == "__main__":
    app.run()