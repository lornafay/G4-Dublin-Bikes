from flask import Flask, render_template

app = Flask(__name__)


# route for index page (Live Map)
@app.route('/')
def index():
    return render_template("index.html")


# route when "Stations" seleceted from menu
@app.route('/stations.html')
def stations():
    return render_template("stations.html")


if __name__ == "__main__":
    app.run(debug=True)
