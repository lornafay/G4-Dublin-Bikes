import mysql.connector

dataBase = mysql.connector.connect(
    host="dublinbikes.c1gwxsai8wyx.eu-west-1.rds.amazonaws.com",
    user="colum",
    passwd="dubbikes22",
    database="dublinbikes"
)

cursorObject = dataBase.cursor()

query = "SELECT number, address, bike_stands FROM dublinbikes.static;"
cursorObject.execute(query)

myresult = cursorObject.fetchall()

for row in myresult:
    print(row)

dataBase.close()
