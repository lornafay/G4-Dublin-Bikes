from flask import Flask, render_template, request, jsonify, json
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
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


# route when "Stations" seleceted from menu
@app.route('/stations.html')
def stations():
    return render_template("stations.html")


@app.route('/stations')
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
