import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from datetime import datetime, timedelta
from utils.api_handler import get_elpriser
from utils.data_tools import create_dataframe

app = Flask(__name__)
app.secret_key = "byt_till_en_hemlig_nyckel"  # behövs för flash och cookies

# Startsida
@app.route("/")
def index():
    last_search = request.cookies.get("last_search", "")
    return render_template("index.html", last_search=last_search)

# Resultatsida
@app.route("/result", methods=["POST", "GET"])
def result():
    try:
        year = int(request.form.get("year"))
        month = int(request.form.get("month"))
        day = int(request.form.get("day"))
        area = request.form.get("area")

        search_date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
        today = datetime.now()
        earliest = datetime(2022, 11, 1)
        max_date = today + timedelta(days=1)

        # Datumkontroll
        if search_date < earliest or search_date > max_date:
            flash("Felaktigt datum! Välj mellan 2022-11-01 och max 1 dag framåt.")
            return redirect(url_for("index"))

        # Hämta data från API
        data = get_elpriser(year, month, day, area)
        if not data:
            flash("Ingen data hittades för detta datum/område.")
            return redirect(url_for("index"))

        # Skapa DataFrame
        df = create_dataframe(data)

        # Spara senaste sökning i cookie
        cookie_value = f"{year}-{month:02d}-{day:02d}_{area}"
        resp = make_response(render_template("result.html", data=df.to_dict(orient="records")))
        resp.set_cookie("last_search", cookie_value)
        return resp
    

    except ValueError:
        flash("Felaktig inmatning!")
        return redirect(url_for("index"))
    


# 404-fel
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404

if __name__ == "__main__":
    app.run(debug=True)


#Starta Flask-appen
#Visa startsida
#Ta emot formulärdata och visa resultat
#Datumkontroll, cookie-sparning, felhantering
""