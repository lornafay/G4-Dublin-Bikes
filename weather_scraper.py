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
        print(current)

        # initialise a row count to act as the index/primary key as all other values will duplicate
        row_count = 0

        # fetch dynamic values for the weather entry
        index = row_count
        timestamp = current["dt"]
        sunrise = current["sunrise"]
        sunset = current["sunset"]
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
        # otherwise assign value of zero
        if current["wind_gust"]:
            wind_gust = current["wind_gust"]
        else:
            wind_gust = 0.0

        if current["rain"]:
            rain = current["rain"]["1h"]
        else:
            rain = 0.0

        if current["snow"]:
            snow = current["snow"]
        else:
            snow = 0.0

        # convert timestamp into a more readable object
        dt = datetime.fromtimestamp(timestamp)

        # prepare sql statement
        sql = f"INSERT INTO current_weather (`index`, `dt`, `sunrise`, " \
              f"`sunset`, `temp`, `feels_like`, `pressure`, `humidity`, `uvi`, " \
              f"`clouds`, `wind_speed`, `wind_gusts`, `wind_dir`, `rain`, `snow`, " \
              f"`description`, `icon`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
              f" %s, %s, %s, %s, %s, %s, %s);"

        # prepare entries
        items = [index, dt, sunrise, sunset, temp, feels_like, pressure, humidity, uvi,
                 clouds, wind_speed, wind_gust, wind_dir, rain, snow, description, icon]

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
