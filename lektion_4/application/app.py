from flask import Flask, render_template, request
import ssl
import json
import urllib
import pandas as pd
import requests

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 ## Inaktivera cache
#Tvingar Flask att läsa om JS och CSS om på nytt varje gång sidan körs. Tar bort 304

@app.route("/", methods=['GET'])
def index():
    ##Plats för kommentarer
    ##
    ##
    return render_template("index.html")

@app.route("/form")
def form():
    """Plats för kommentarer"""
    ###
    #####
    return render_template('form.html')

@app.post("/api")
def api_post():
    """Plats för kommentarer"""
    year = request.form['year']
    country_code = request.form['countrycode']
    data_url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}"
    json_data = requests.get(data_url)
    data = json.loads(json_data.text)
    df = pd.DataFrame(data)
    table_data = df.to_html(columns=["date","localName"], classes="table p-5", justify="left")
    title = f"Helgdagar i {country_code.upper()} år {year}"
    #data = f"Helgdagar i {country_code} år {year}"
    ###
    ####
    return render_template('index.html', data=table_data, title=title)


if __name__ == "__main__":
    app.run(debug=True)
