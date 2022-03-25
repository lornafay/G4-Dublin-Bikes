#!/home/ubuntu/miniconda3/envs/comp30830/bin/python

"""
Python file to create necessary tables for database.

import packages
access RDS credentials
try:
    initialise connection to database in variable
    create static table
    create dynamic table
    create current weather table
    create minutely forecast table
    create hourly forcast table
    execute queries
    commit queries
    close connection
except:
    print error
"""

import os
from mysql.connector import connect, Error

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

    # if no error connecting to host
    print("Connection successful")

    cursor = connection.cursor()

    # prepare sql statement
    sql_static = f'CREATE TABLE IF NOT EXISTS static (' \
                 f'`number` FLOAT,' \
                 f'`name` VARCHAR(50),' \
                 f'`address` VARCHAR(50),' \
                 f'`latitude` FLOAT,' \
                 f'`longitude` FLOAT,' \
                 f'`bike_stands` FLOAT);'

    sql_dynamic = f'CREATE TABLE IF NOT EXISTS dynamic (' \
                  f'`time` DATETIME,' \
                  f'`number` FLOAT,' \
                  f'`stands_available` FLOAT,' \
                  f'`bikes_available` FLOAT,' \
                  f'`status` VARCHAR(50));'

    sql_current_weather = f'CREATE TABLE IF NOT EXISTS current_weather (' \
                          f'`time` DATETIME,' \
                          f'`sunrise` DATETIME,' \
                          f'`sunset` DATETIME,' \
                          f'`temp` FLOAT,' \
                          f'`feels_like` FLOAT,' \
                          f'`pressure` FLOAT,' \
                          f'`humidity` FLOAT,' \
                          f'`uvi` FLOAT,' \
                          f'`clouds` FLOAT,' \
                          f'`wind_speed` FLOAT,' \
                          f'`wind_gusts` FLOAT,' \
                          f'`wind_dir` FLOAT,' \
                          f'`rain` FLOAT,' \
                          f'`snow` FLOAT,' \
                          f'`description` VARCHAR(50),' \
                          f'`icon` VARCHAR(50));'

    sql_minutely_forecast = f'CREATE TABLE IF NOT EXISTS minutely_forecast (' \
                            f'`time` DATETIME,' \
                            f'`precipitation` FLOAT);'

    sql_hourly_forecast = f'CREATE TABLE IF NOT EXISTS hourly_forecast (' \
                          f'`time` DATETIME,' \
                          f'`temp` FLOAT,' \
                          f'`feels_like` FLOAT,' \
                          f'`pressure` FLOAT,' \
                          f'`humidity` FLOAT,' \
                          f'`uvi` FLOAT,' \
                          f'`clouds` FLOAT,' \
                          f'`wind_speed` FLOAT,' \
                          f'`wind_gusts` FLOAT,' \
                          f'`wind_dir` FLOAT,' \
                          f'`probability_precip` FLOAT,' \
                          f'`rain` FLOAT,' \
                          f'`snow` FLOAT,' \
                          f'`description` VARCHAR(50),' \
                          f'`icon` VARCHAR(50));'

    # execute and apply sql command
    cursor.execute(sql_static)
    cursor.execute(sql_dynamic)
    cursor.execute(sql_current_weather)
    cursor.execute(sql_minutely_forecast)
    cursor.execute(sql_hourly_forecast)
    connection.commit()

    connection.close()

except Error as e:
    print(e)
