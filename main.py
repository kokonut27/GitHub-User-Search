import git_api
from flask import Flask, render_template, request, session, url_for, redirect, flash
import json
import os
from flask_session import Session
import requests

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.config["SECRET_KEY"] = os.environ["key"]
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
  return render_template(
    "index.html",
  )

git_api.Token(os.environ["token"])

@app.route('/search')
def search():
  return render_template(
    "search.html",
    usernick = session.get("usernick"),
  )


@app.route('/search', methods=["POST", "GET"])
def searchvalue():
  if request.method == "POST":
    data = request.form["data"]
    userdata2 = git_api.User(data).User()
    username2 = git_api.User(data).Name()
    data = json.loads(username2)
    name = data["data"]["user"]["name"]

    data = json.loads(userdata2)
    data2 = data["data"]["user"]
    userdata = ""
    for i in data2:
      pass

    
    session["usernick"] = name
    print(session.get("usernick"))

    return render_template(
      "search.html"
    )

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html')
  
app.run(host="0.0.0.0", port=8080)