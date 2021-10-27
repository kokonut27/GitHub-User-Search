import git_api
from flask import Flask, render_template, request, session, url_for, redirect, flash, send_from_directory
import json
import os
from flask_session import Session
import requests
import shutil
# import wget

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
    username = session.get("username"),
    avatar = session.get("avatar"),
  )


@app.route('/searchvalue', methods=["POST", "GET"])
def searchvalue():
  if request.method == "POST":
    data2 = request.form["data"]
    url = "https://github.com/"+data2
    userexist = requests.get(url)
    status = userexist.status_code
    
    if status != 200:
      return render_template(
        "nouser.html"
      )
    userdata2 = git_api.User(data2).User()
    data = json.loads(userdata2)
    name = data["data"]["user"]["name"]
    username = data2

    image_url = data["data"]["user"]["avatarLink"]
    filename = image_url.split("/")[-1]
    res = requests.get(image_url, stream = True)
    if res.status_code == 200:
      res.raw.decode_content = True
        
      with open("static/"+filename, 'wb') as f:
        shutil.copyfileobj(res.raw, f)
      
      avatar = filename
      f.close()
      
    else:
      avatar = "Image can't be opened!"

    session["usernick"] = name
    session["username"] = username
    session["avatar"] = avatar
  return redirect(url_for('search'))

'''@app.route('/delete_session')
def delete_session():
  try:
    session.pop("avatar")
    session.pop("usernick")
    session.pop("username")
  except:
    return redirect(url_for('index'))
  return render_template("index.html")'''

@app.route('/avatar')
def avatar():
  return send_from_directory(
    'static/', session["avatar"], as_attachment=True
  )


@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html')
  
app.run(host="0.0.0.0", port=8080)