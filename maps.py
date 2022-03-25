from flask import Flask, render_template, abort

app = Flask(__name__)

class Station:
    def __init__(self, key, name, lat, lng):
        self.key  = key
        self.name = name
        self.lat  = lat
        self.lng  = lng

stations = (
    Station('blessst', 'Blessington Street',     53.3568, -6.26814),
   Station('boltonst', 'Bolton Streer',     53.3512, -6.26986),
   Station('greekst', 'Greek Street',    53.3469, -6.27298)
)

stations_by_key = {station.key: station for station in stations}

@app.route("/")
def station():
    return render_template('index.html', stations=stations)

@app.route("/<station_code>") 
def show_station(station_code):
    station = stations_by_key.get(station_code)
    if station:
        #map file
        return render_template('map.html', station=station)
    else:
        abort(404)

app.run(host='localhost', debug=True)