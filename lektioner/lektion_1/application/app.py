from flask import Flask
import json
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

adress = {"name": "Dennis", "lastname": "Rudin", "class": "5a"}
@app.route("/api")
def api():
    return json.dumps(adress)



@app.route("/login")
def login():
    return "Hej, välkommen!!"