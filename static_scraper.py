"""
Scraper for static station data from JCDecaux. Does not use sqlalchemy.

import packages
initialise variables for API request
define scrape function
define time function
initialise connection to database in variable
try:
    initialise row count
    store scraped json data in python list
        initialise for loop (range length of scraped list)
            initialise table entries as variables by accessing list
            create cursor object
            prepare sql statement
            execute sql command
            commit sql command
            increment row count
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
STATION_NUM = '{42}'
STATIONS = f'https://api.jcdecaux.com/vls/v1/stations?contract={CONTRACT}&apiKey={API_KEY}'

db_user = os.environ.get('LOCAL_WORKBENCH_USER')
db_passwd = os.environ.get('LOCAL_WORKBENCH_PASSWD')


def scrape():
    """Fetches station JSON data from JCDecaux API."""

    # request json data
    r = requests.get(STATIONS)
    # return json object converted to python object
    return r.json()


# don't think this function is needed for the static data
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
        host="127.0.0.1",
        user=db_user,
        passwd=db_passwd,
        database="dublin_bikes"
    )

    # if no error connecting to host
    print("Connection successful")

    # initialise a row count to act as the index/primary key
    row_count = 0

    # assign scraped data to new list
    stations = scrape()

    for i in range(len(stations) - 1):
        index = row_count
        number = stations[i]["number"]
        name = stations[i]["name"]
        latitude = stations[i]["position"]["lat"]
        longitude = stations[i]["position"]["lng"]
        timeOfRequest = get_time()

        cursor = connection.cursor()

        # prepare sql statement
        sql = f'INSERT INTO static (`index`, `number`, `name`, `latitude`, `longitude`) ' \
             f'VALUES (%s, %s, %s, %s, %s);'

        # prepare entries
        items = [index, number, name, latitude, longitude]

        # execute and apply sql command
        cursor.execute(sql, items)
        connection.commit()

        # increment row count
        row_count += 1

    connection.close()

except Error as e:
    print(e)
