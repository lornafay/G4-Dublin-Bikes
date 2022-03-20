#!/home/ubuntu/miniconda3/envs/comp30830/bin/python

"""
Scraper for current weather data from Open Weather API. Does not use sqlalchemy.

import packages
access key variable
define scrape function
initialise connection to database in variable
try:
    initialise row count
    initialise endless loop
        store scraped json data in python list
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

        dt = get_time()
        # fetch dynamic values for the weather entry
        sunrise = datetime.fromtimestamp(current["sunrise"])
        sunset = datetime.fromtimestamp(current["sunset"])
        temp = current["temp"]
        feels_like = current["feels_like"]
        pressure = current["pressure"]
        humidity = current["humidity"]
        uvi = current["uvi"]
        clouds = current["clouds"]
        wind_speed = current["wind_speed"]
        wind_dir = current["wind_deg"]
        description = current["weather"][0]["description"]
        icon = current["weather"][0]["icon"]

        # check if the response contains wind gust and precipitation data
        # otherwise add key with value of zero to object so sql query does not break script
        if "wind_gust" not in current.keys():
            current["wind_gust"] = 0.0

        if "rain" not in current.keys():
            current["rain"] = 0.0

        if "snow" not in current.keys():
            current["snow"] = 0.0

        wind_gust = current["wind_gust"]
        rain = current["rain"]
        snow = current["snow"]

        # prepare sql statement
        sql = f"INSERT INTO current_weather (`dt`, `sunrise`, " \
              f"`sunset`, `temp`, `feels_like`, `pressure`, `humidity`, `uvi`, " \
              f"`clouds`, `wind_speed`, `wind_gusts`, `wind_dir`, `rain`, `snow`, " \
              f"`description`, `icon`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s," \
              f" %s, %s, %s, %s, %s, %s, %s);"

        # prepare entries
        items = [dt, sunrise, sunset, temp, feels_like, pressure, humidity, uvi,
                 clouds, wind_speed, wind_gust, wind_dir, rain, snow, description, icon]

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
