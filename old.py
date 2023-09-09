from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask_cors import CORS
from hashlib import sha256
import json
import datetime
import sqlite3

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

today = datetime.date.today()
app = Flask(__name__, static_folder="build/static", template_folder="build")
CORS(app)

def signin(username, password):
    try:
        api = Garmin(username, password)
        api.login()
        return api
    except:
        print("Error authenitcating Email and Password")

def add_healthinfo_to_db(steps, step_goal, current_hr, avg_resting_hr):
    try:
        db = sqlite3.connect("pfit.db")
        cursor = db.cursor()

        q = "SELECT * FROM healthinfo"
        cursor.execute(q)
        records = cursor.fetchall()

        last = None
        for r in records:
            last = r

        (last_id,_,_,_,_,_) = last

        q = """
        INSERT INTO healthinfo VALUES({},{},{},{},{},\"{}\")
        """.format(last_id+1, steps, step_goal, current_hr, avg_resting_hr, str(today))

        cursor.execute(q)
        db.commit()
    except:
        print("ERROR ADDING TO DATABASE")

 

@app.route("/")
@app.route("/login")
@app.route("/signup")
@app.route("/dashboard")
@app.route("/healthinfo")
@app.route("/workout")
@app.route("/progress")
@app.route("/social")
def progressionFit():
    return render_template("index.html")

@app.route("/validate_login", methods=["POST"])
def validate_login():
    credentials = json.loads(request.json)
    username = credentials["username"]
    password = sha256(credentials["password"].encode('utf-8')).hexdigest()
    session_id = 0

    db = sqlite3.connect("pfit.db") 
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE username = \"" + username + "\" AND password = \"" + password + "\"")

    try:
        (session_id, _, _) = c.fetchall()[0]
    except:
        session_id = -1

    print("SessionID: " + str(session_id))

    response = jsonify({
        "sessionId" : session_id,
        "username" : username
    })

    return response

@app.route("/garminapi", methods=["POST"])
def garminapi():
    login_info = json.loads(request.json)
    username = login_info["username"]
    password = login_info["password"]

    api = signin(username, password)
    try:
        api_steps = api.get_daily_steps(today.isoformat(), today.isoformat())
        api_hr_data = api.get_heart_rates(today.isoformat())

        response = jsonify([api_steps, api_hr_data])
        print(response)

        # steps = api_steps[0]['totalSteps']
        # step_goal = api_steps[0]['stepGoal']
        # current_hr = api_hr_data['heartRateValues'][len(api_hr_data['heartRateValues'])-1][1]
        # avg_resting_hr = api_hr_data['restingHeartRate']
        
        # add_healthinfo_to_db(steps, step_goal, current_hr, avg_resting_hr)

        return response
    except:
        print("Error in API Call. Too many requests")
        return jsonify({})

if __name__ == "__main__":
    app.run()
