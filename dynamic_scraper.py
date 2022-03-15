#!/home/ubuntu/miniconda3/envs/comp30830/bin/python

"""
Scraper for dynamic station data from JCDecaux. Does not use sqlalchemy.

import packages
initialise variables for API request
define scrape function
define time function
initialise connection to database in variable
try:
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
        sleep 5 mins
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

    # initialise cursor object
    cursor = connection.cursor()

    # if no error connecting to host
    print("Connection successful")

    while True:

        # call scraper and store in new list
        stations = scrape()

        # for every station
        for i in range(len(stations)):

            # fetch dynamic values for the station entry
            number = stations[i]["number"]
            stands_available = stations[i]["available_bike_stands"]
            bikes_available = stations[i]["available_bikes"]
            status = stations[i]["status"]
            timeOfRequest = get_time()

            # prepare sql statement
            sql = f"INSERT INTO dynamic (`time`, `number`, `stands_available`, " \
                  f"`bikes_available`, `status`) VALUES (%s, %s, %s, %s, %s);"

            # prepare entries
            items = [timeOfRequest, number, stands_available, bikes_available, status]

            # execute and apply new sql command
            cursor.execute(sql, items)
            connection.commit()

        # wait 5 minutes
        time.sleep(300)

    # close connection if loop ever ends
    connection.close()

# handle exception
except Error as e:
    print(e)
