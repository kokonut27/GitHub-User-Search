import git_api
from flask import Flask, render_template, request, session, url_for, redirect, send_from_directory
import json
import os
import shutil
from flask_session import Session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config["SECRET_KEY"] = os.environ["key"]
app.config["SESSION_PERMANENT"] = False
try:
    app.config["REPL_USER"] = os.environ["REPL_OWNER"]
except KeyError:
    app.config["REPL_USER"] = "DillonB07"
app.config["SESSION_TYPE"] = "filesystem"
app.config["static"] = 'static/'
git_api.Token(os.environ["token"])
Session(app) # The sessions are created here


@app.route('/')
def index():
    # Reset flask_session folder
    shutil.rmtree('flask_session')
    os.mkdir("flask_session")
    return render_template("index.html")

@app.route('/nouser')
def nouser():
    return render_template("nouser.html")


@app.route('/search')
def search():
    return render_template("search.html",
                           usernick=session.get("usernick"),
                           username=session.get("username"),
                           avatar=session.get("avatar"),
                           userurl=session.get("userurl"),
                           bio=session.get("bio"))


@app.route('/searchvalue', methods=["POST", "GET"])
def searchvalue():
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

        """filename = image_url.split("/")[-1].split('?')[0]
        res = requests.get(image_url, stream=True)
        if res.status_code == 200:
            res.raw.decode_content = True
            with open(f"static/avatars/{filename}", 'wb') as f:
                shutil.copyfileobj(res.raw, f)

            # avatar = f'{app.config["static"]}avatars/{filename}'
            avatar = f'avatars/{filename}'"""
        """if session.get("avatarYN") == "True":
        if avatar != None:
          session["avatarYN"] = "False"
          return send_from_directory(
            app.config['static'], filename, as_attachment=True
          )"""
        avatar = image_url


        session["usernick"] = name
        if session.get("usernick") is None:
            session["usernick"] = "No Nickname!"
        session["username"] = username
        session["avatar"] = avatar
        session["userurl"] = userurl
        session["bio"] = bio
        if session.get("bio") is None:
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
    return send_from_directory('static/',
                               session["avatar"],
                               as_attachment=True)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def page_not_found2(e):
  return render_template("500.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
