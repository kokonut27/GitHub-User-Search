import git_api
from flask import Flask, render_template, request, session, url_for, redirect, flash, send_from_directory
import json
import os
from flask_session import Session
import requests
import shutil

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')
app.config["SECRET_KEY"] = os.environ["key"]
app.config["SESSION_PERMANENT"] = False
app.config["REPL_USER"] = os.environ["REPL_OWNER"]
app.config["SESSION_TYPE"] = "filesystem"
app.config["static"] = 'static/'
git_api.Token(os.environ["token"])
Session(app)


@app.route('/')
def index():
  return render_template(
    "index.html",
  )

@app.route('/search')
def search():
  return render_template(
    "search.html",
    usernick = session.get("usernick"),
    username = session.get("username"),
    avatar = session.get("avatar"),
    userurl = session.get("userurl"),
    bio = session.get("bio"),
  )

@app.route('/nouser')
def nouser():
  return render_template("nouser.html")

@app.route('/searchvalue', methods=["POST", "GET"])
def searchvalue():
  # global name
  if request.method == "POST":
    session["usernick"] = "No User Exists!"
    session["username"] = "NoUserExists"
    session["avatar"] = 'nothing.jpg'
    session["userurl"] = "https://github.com/404"
    session["bio"] = "This user does not have a bio"
    session["avatarYN"] = "True"
    data2 = request.form["data"]
    """url = "https://github.com/"+data2
    userexist = requests.get(url)
    status = userexist.status_code
    
    if status == 200:
      pass
    else:
      return redirect(url_for("nouser"))"""
    url = f"https://github.com/{data2}"
    userurl = url
    userdata2 = git_api.User(data2).User()
    data = json.loads(userdata2)
    name = data["data"]["user"]["name"]
    bio = data["data"]["user"]["bio"]
    username = data2

    image_url = data["data"]["user"]["avatarLink"]
    filename = image_url.split("/")[-1]
    res = requests.get(image_url, stream = True)
    if res.status_code == 200:
      res.raw.decode_content = True
        
      with open("static/"+filename, 'wb') as f:
        shutil.copyfileobj(res.raw, f)
      
      avatar = filename

      """if session.get("avatarYN") == "True":
        if avatar != None:
          session["avatarYN"] = "False"
          return send_from_directory(
            app.config['static'], filename, as_attachment=True
          )"""
          
      f.close()
    else:
      pass # add something here - error

    session["usernick"] = name
    if session.get("usernick") == None:
      session["usernick"] = "No Nickname!"
    session["username"] = username
    session["avatar"] = avatar
    session["userurl"] = userurl
    session["bio"] = bio
    if session.get("bio") == None:
      session["bio"] = "This user does not have a bio"
    session["avatarYN"] = "False"
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

@app.errorhandler(500)
def page_not_found2(e):
  return render_template("505.html") 
# The most likely outcome is because the user doesn't exist, so we're assuming that because of that, it will always be a no user error. We could be wrong though!
  
app.run(host="0.0.0.0", port=8080)
