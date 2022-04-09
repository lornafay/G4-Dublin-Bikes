#!/home/ubuntu/miniconda3/envs/comp30830/bin/python
from crypt import methods
from nis import maps
from unittest import result
from flask import Flask, redirect, render_template, request, jsonify, json, url_for
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
import time
import os
from math import radians, cos, sin, asin, sqrt
from numpy import source
import googlemaps
import requests

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get('RDS_HOST')
app.config['MYSQL_USER'] = os.environ.get('RDS_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('RDS_PASSWD')
app.config['MYSQL_DB'] = 'dublinbikes'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
MAPS_API = os.environ.get("MAPS_API")
WEATHER_API = os.environ.get("WEATHER_KEY")

mysql = MySQL(app)


# route for index page (Live Map)
@app.route('/')
def index():

    return render_template("index.html", maps_api=MAPS_API, weather_api=WEATHER_API)


def getStationObj():
    '''to be used for markers and prediction routes'''

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
    stations_json = jsonify(stations=rows)

    return rows, stations_json


@app.route('/predict', methods=["POST"])
def predict():
    # handles form data and returns a prediction

    rows, js = getStationObj()

    # harversine formula taken from Stack Overflow user @Michael Dunn
    # https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    def haversine(lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance in kilometers between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        # Radius of earth in kilometers. Determines return value units.
        r = 6371
        return c * r

    def availability(station, action):
        """Returns True if station availability is sufficient.

        Sufficiency based on where bike/stand availability is
        at least 30% of station capacity."""

        # determine need of user
        if action == "take":
            need = "bikes_available"
        else:
            need = "stands_available"

        # find availability
        if (station[need] / station["bike_stands"]) * 100 > 29.0:
            return True
        else:
            return False

    # capture form inputs
    bike_action = request.form["take_leave"]
    source_location = request.form["current_custom"]
    if request.form["time"] == "":
        action_time = time.strftime('%H:%M')
    else:
        action_time = request.form["time"]
    dist_range = request.form["within"]

    # the value taken from the "current_custom" part will be split in format ["current"][lat][lng] if a current location was chosen
    split_location = source_location.split(",")
    if split_location[0] == "current":
        # sample current location = TCD Hamilton building (Comp Sci school)
        user_lat = float(split_location[1])
        user_long = float(split_location[2])

    # the splitting condition will not apply if a custom location was chosen so we just geocode the unprocessed input value
    else:
        gmaps = googlemaps.Client(
            key=MAPS_API)

        # Geocoding the address into lat and lng values
        geocode_result = gmaps.geocode(f"{source_location}, Dublin, Ireland")
        user_lat = geocode_result[0]["geometry"]["location"]["lat"]
        user_long = geocode_result[0]["geometry"]["location"]["lng"]

    # now use haversine to find nearest station
    distance_dict = {}
    for row in rows:
        # if station is open and bike/stand availability is sufficient
        if (row["status"] == "OPEN") and (availability(row, bike_action)):
            # apply haversine formula to each station
            distance_from_user = haversine(
                user_lat, user_long, row["latitude"], row["longitude"])
            # add to distances dict if it is within chosen distance
            if distance_from_user <= float(dist_range):
                distance_dict[row["name"]] = distance_from_user

    # if dictionary length is greater than 1
    if len(distance_dict) > 1:
        # sort the dictionary by distance from user
        sorted_distances = sorted(distance_dict.values())  # Sort the values
        sorted_distance_dict = {}

        for i in sorted_distances:
            for k in distance_dict.keys():
                if distance_dict[k] == i:
                    sorted_distance_dict[k] = distance_dict[k]
                    break

        # closest station to user
        nearest_station = list(sorted_distance_dict)[0]

        # return back to index page
        results = f"Recommended station to {bike_action} a bike: {nearest_station}"

    # else if dict had only one element
    elif len(distance_dict) == 1:
        results = f"Recommended station to {bike_action} a bike: {list(distance_dict.keys())[0]}"

    # if no items in distance dict
    else:
        if bike_action == "take":
            message = "bikes"
        else:
            message = "stands"

        results = f"Sorry, no stations available with at least 30% availability of {message}."

    return render_template("index.html", results=results, maps_api=MAPS_API)


# route when "Stations" seleceted from menu
@app.route('/stations')
def stations():
    return render_template("stations.html")


# fetch station data
@app.route('/station_fetch')
def get_stations():
    py, js = getStationObj()
    return js


# route when "Weather" seleceted from menu
@app.route('/weather')
def weather():
    return render_template("weather.html")


# fetch weather data
@app.route('/weather_fetch')
def get_weather():
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/onecall?lat=53.350140&lon=-6.266155&units=metric&exclude=daily&appid={WEATHER_API}")
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error {response.status_code}. There was a problem with the fetch."


if __name__ == "__main__":
    app.run(debug=True)
