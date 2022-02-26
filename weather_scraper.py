#!/home/ubuntu/miniconda3/envs/comp30830/bin/python

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

WEATHER_KEY = os.environ.get("WEATHER_KEY")

WEATHER = f'https://api.openweathermap.org/data/2.5/onecall?lat=53.350140&lon=-6.266155' \
          f'&units=metric&exclude=daily&appid={WEATHER_KEY}'


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

        # call scraper and store current weather data in new list
        current = scrape()["current"]

        # initialise a row count to act as the index/primary key as all other values will duplicate
        row_count = 0

        # for every station
        for i in range(len(current)):

            # fetch dynamic values for the station entry
            index = row_count
            time = current["dt"]
            sunrise = current["sunrise"]
            sunset = current["sunset"]
            temp = current["status"]
            feels_like = current["feels_like"]
            pressure = current["pressure"]
            humidity = current["humidity"]
            uvi = current["uvi"]
            clouds = current["clouds"]
            wind_speed = current["wind_speed"]
            wind_gusts = current["wind_gusts"]
            wind_dir = current["wind_dir"]
            rain = current["rain"]
            snow = current["snow"]
            description = current["description"]
            icon = current["icon"]

            # prepare sql statement
            sql = f"INSERT INTO current_weather (`index`, `time`, `sunrise`, " \
                  f"`sunset`, `temp`, `feels_like`, `pressure`, `humidity`, `uvi`, " \
                  f"`clouds`, `wind_speed`, `wind_gusts`, `wind_dir`, `rain`, `snow`, " \
                  f"`description`, `icon`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                  f" %s, %s, %s, %s, %s, %s, %s);"

            # prepare entries
            items = [index, time, sunrise, sunset, temp, feels_like, pressure, humidity, uvi,
                     clouds, wind_speed, wind_gusts, wind_dir, rain, snow, description, icon]

            # execute and apply new sql command
            cursor.execute(sql, items)
            connection.commit()

            # increment row count
            row_count += 1

        # wait 5 minutes
        time.sleep(300)

    # close connection if loop ever ends
    connection.close()

# handle exception
except Error as e:
    print(e)
