from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    make_response,
    session,
    redirect,
)
from flask_session import Session
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
def dashboard():
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

if __name__ == "__main__":
    app.run()