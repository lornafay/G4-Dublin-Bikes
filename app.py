from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'dublinbikes.c1gwxsai8wyx.eu-west-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'colum'
app.config['MYSQL_PASSWORD'] = 'dubbikes22'
app.config['MYSQL_DB'] = 'dublinbikes'

mysql = MySQL(app)

# route for index page (Live Map)


@app.route('/')
def index():
    return render_template("index.html")


# route when "Stations" seleceted from menu
@app.route('/stations.html', methods=['GET', 'POST'])
def stations():
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE test (ok INT NOT NULL);")
    mysql.connection.commit()
    cur.close()

    return render_template("stations.html")


# route when "Weather" seleceted from menu
@app.route('/weather.html')
def weather():
    return render_template("weather.html")


if __name__ == "__main__":
    app.run(debug=True)
