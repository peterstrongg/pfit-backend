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
app.secret_key = str(os.urandom(12))
app.permanent_session_lifetime = timedelta(days=7)
CORS(app, support_credentials=True)

@app.route("/", methods=["GET","POST"])
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        credentials = json.loads(request.json)
        username = credentials["username"]
        password = credentials["password"]

        db = Database("pfit.db")
        sid = db.get_session_id(username, password)
        session["sid"] = sid

        if sid > 0:
            return redirect("/dashboard")

        return render_template("index.html")

    elif request.method == "GET":
        sid = session.get("sid")
        if sid:
            return redirect("/dashboard")
        return render_template("index.html")

@app.route("/dashboard")
@app.route("/healthinfo")
@app.route("/workout")
@app.route("/progress")
@app.route("/social")
def dashboard():
    return render_template("index.html")

@app.route("/api/validate_session", methods=["GET"])
def validate_session():
    sid = session.get("sid")
    if not sid:
        return redirect("/")

    return render_template("index.html")

if __name__ == "__main__":
    app.run()