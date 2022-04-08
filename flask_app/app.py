from crypt import methods
from flask import Flask, redirect, render_template, request, jsonify, json, url_for
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
from wtforms.validators import DataRequired
import time
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get('RDS_HOST')
app.config['MYSQL_USER'] = os.environ.get('RDS_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('RDS_PASSWD')
app.config['MYSQL_DB'] = 'dublinbikes'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)


# route for index page (Live Map)
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/predict', methods=["POST"])
def predict():
    # handles form data and returns a prediction
    # capture form inputs
    bike_action = request.form["take_leave"]
    source_location = request.form["current_custom"]
    if request.form["time"] == "":
        action_time = time.strftime('%H:%M')
    else:
        action_time = request.form["time"]

    # return back to index page
    selections = [bike_action, source_location, action_time]
    results = f"Recommended station to {bike_action} a bike: [station]"
    return render_template('index.html', results=results)


# route when "Stations" seleceted from menu
@app.route('/stations')
def stations():
    return render_template("stations.html")


@app.route('/station_fetch')
def get_stations():

    # get current time minus 5 mins
    # IMPORTANT remove the hours argument once daylight savings registers with datetime
    timerange = datetime.now() - timedelta(hours=1, minutes=5)
    query = f"SELECT * FROM dublinbikes.dynamic d JOIN dublinbikes.static s ON d.number = s.number WHERE d.time > '{timerange}' ORDER BY s.number;"

    # create query
    cur = mysql.connection.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    mysql.connection.commit()
    # handle results
    stations = jsonify(stations=rows)

    return stations


# route when "Weather" seleceted from menu
@app.route('/weather')
def weather():
    return render_template("weather.html")


if __name__ == "__main__":
    app.run(debug=True)
