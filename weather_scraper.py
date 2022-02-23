#!/Users/Lorna/opt/anaconda3/envs/comp30830/bin/python

"""
Scraper for dynamic station data from M. Does not use sqlalchemy.

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

WEATHER_USER = os.environ.get("WEATHER_USER")
WEATHER_PASSWD = os.environ.get("WEATHER_PASSWD")

WEATHER = f'https://{WEATHER_USER}:{WEATHER_PASSWD}@api.meteomatics.com/2022-02-21T00:00:00.000+00:00--2022-02-27T00:00:00.000+00:00:PT10M/' \
           f'wind_speed_10m:kmh,wind_dir_10m:d,wind_gusts_10m_1h:bft,t_2m:C,t_max_2m_24h:C,precip_1h:mm,' \
           f'weather_symbol_1h:idx,uv:idx,sunrise:dn,sunset:dn/53.4064939,-6.2870606/json?model=mix'


def scrape():
    """Fetches station JSON data from JCDecaux API."""

    # request json data
    r = requests.get(WEATHER)
    # return json object converted to python object
    return r.json()


def get_time():
    """Returns a datetime object at the time of function call."""

    # get current timestamp
    timestamp = time.time()
    # convert to datetime object and return
    dt_object = datetime.fromtimestamp(timestamp)

    return dt_object


rds_host = os.environ.get("RDS_HOST")
rds_user = os.environ.get('RDS_USER')
rds_passwd = os.environ.get('RDS_PASSWD')

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

    # enter infinite loop
    while True:

        # call scraper and store in new list
        weather = scrape()

        # initialise a row count to act as the index/primary key as all other values will duplicate
        row_count = 0

        # clear table
        cursor.execute("DELETE FROM dynamic;")

        # for every station
        for i in range(len(weather) - 1):
            # fetch dynamic values for the station entry
            index = row_count
            number = weather[i]["number"]
            stands_available = weather[i]["available_bike_stands"]
            bikes_available = weather[i]["available_bikes"]
            status = weather[i]["status"]
            timeOfRequest = get_time()

            # prepare sql statement
            sql = f"INSERT INTO dynamic (`index`, `number`, `stands_available`, " \
                  f"`bikes_available`, `status`, `time`) VALUES (%s, %s, %s, %s, %s, %s);"

            # prepare entries
            items = [index, number, stands_available, bikes_available, status, timeOfRequest]

            # execute and apply new sql command
            cursor.execute(sql, items)
            connection.commit()

            # increment row count
            row_count += 1

        # wait 5 minutes
        time.sleep(10)

    # close connection if loop ever ends
    connection.close()

# handle exception
except Error as e:
    print(e)
