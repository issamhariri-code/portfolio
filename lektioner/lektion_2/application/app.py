from flask import Flask, render_template, redirect, url_for
from flask import request
import json
import os
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('login.html')

adress = {"name": "Dennis", "lastname": "Rudin", "class": "5a"}
@app.route("/api")
def api():
    return json.dumps(adress)

USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users.json')
users = {}
try:
    with open(USERS_FILE, "r", encoding="utf-8")as f:
        users = json.load(f)
except Exception:
    users = {} 

def save_users():
    with open(USERS_FILE, "w", encoding="utf-8")as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def valid_login(username, password):
    return username in users and users[username] == password

def log_the_user_in(username):
    return redirect(url_for('hello', name=username))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            error = "Missing username or Password"
        elif username in users:
            error = "User already exists"
        else:
            users[username] = password
            save_users()
            return f"Registrerad {username}"
    return render_template('register.html', error=error)


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if valid_login(username, password):
            return log_the_user_in(username)
        else:
            error = 'Invalid username/password'
    
    return render_template('login.html', error=error)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('cv.htm', person=name)

if __name__ == "__main__":
    app.run(debug=True)