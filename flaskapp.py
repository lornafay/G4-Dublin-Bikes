from flask import Flask 
from flask_mysqldb import MySQL 

app = Flask(__name__)

app.config['MYSQL_USER'] = 'colum'
app.config['MYSQL_PASSWORD'] = 'dubbikes22'
app.config['MYSQL_HOST'] = 'dublinbikes.c1gwxsai8wyx.eu-west-1.rds.amazonaws.com'
app.config['MYSQL_DB'] = 'dublinbikes'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    #cur.execute('''CREATE TABLE example (id INTEGER, name VARCHAR(20))''')

    #cur.execute('''INSERT INTO example VALUES (1, 'Anthony')''')
    #cur.execute('''INSERT INTO example VALUES (2, 'Billy')''')
    #mysql.connection.commit()

    cur.execute('''SELECT * FROM static''')
    results = cur.fetchall()
    print(results)
    return 'Done!'