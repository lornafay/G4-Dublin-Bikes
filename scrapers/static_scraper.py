#!/home/ubuntu/miniconda3/envs/comp30830/bin/python
"""
Scraper for static station data from JCDecaux. Does not use sqlalchemy.

import packages
initialise variables for API request
define scrape function
define time function
try:
    initialise connection to database in variable
    initialise row count
    initialise endless loop
        store scraped json data in python list
        initialise for loop (range length of scraped list)
            initialise table entries as variables by accessing list
            create cursor object
            prepare sql statement
            execute sql command
            commit sql command
            increment row count
        wait 1 week
    close connection
except:
    print error
"""


import os
import requests
from datetime import datetime
import time
from mysql.connector import connect, Error

# API key, DB username and password stored as env variables
API_KEY = os.environ.get('JCD_API')
CONTRACT = 'dublin'
STATIONS = f'https://api.jcdecaux.com/vls/v1/stations?contract={CONTRACT}&apiKey={API_KEY}'

rds_host = os.environ.get("RDS_HOST")
rds_user = os.environ.get('RDS_USER')
rds_passwd = os.environ.get('RDS_PASSWD')


def scrape():
    """Fetches station JSON data from JCDecaux API."""

    # request json data
    r = requests.get(STATIONS)
    # return json object converted to python object
    return r.json()


# don't think this is needed for this table but keeping the function here for now in case this changes
def get_time():
    """Returns a datetime object at the time of function call."""

    # get current timestamp
    timestamp = time.time()
    # convert to datetime object and return
    dt_object = datetime.fromtimestamp(timestamp)

    return dt_object


try:
    # create connection to DB host
    connection = connect(
        host=rds_host,
        port=3306,
        user=rds_user,
        passwd=rds_passwd,
        database="dublinbikes"
    )

    # if no error connecting to host
    print("Connection successful")

    # initialise cursor object
    cursor = connection.cursor()

    while True:
        # clear table
        cursor.execute("DELETE FROM static;")

        # assign scraped data to new list
        stations = scrape()

        for i in range(len(stations) - 1):
            number = stations[i]["number"]
            name = stations[i]["name"]
            address = stations[i]["address"]
            latitude = stations[i]["position"]["lat"]
            longitude = stations[i]["position"]["lng"]
            bike_stands = stations[i]["bike_stands"]

            # prepare sql statement
            sql = f'INSERT INTO static (`number`, `name`, `address`, `latitude`, `longitude`,' \
                  f' `bike_stands`) VALUES (%s, %s, %s, %s, %s, %s);'

            # prepare entries
            items = [number, name, address, latitude, longitude, bike_stands]

            # execute and apply sql command
            cursor.execute(sql, items)
            connection.commit()

        # wait 1 week
        time.sleep(604800)

    connection.close()

except Error as e:
    print(e)
