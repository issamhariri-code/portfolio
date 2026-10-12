# ...existing code...
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "byt_till_en_säker_hemlig_nyckel"  

@app.route("/")
@app.route("/main")
def main():
    namn = session.get("username") #Returnerar None om en inloggad.
    return render_template("main.htm", namn=namn), 200

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    if username:
        session["username"] = username
    return redirect(url_for("after_login"))

@app.route("/after_login")
def after_login():
    namn = session.get("username", "Okänd")
    return render_template("after_login.htm", namn=namn), 200

if __name__ == "__main__":
    app.run(debug=True)