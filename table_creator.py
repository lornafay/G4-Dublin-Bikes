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
        database="stations"
    )

    # if no error connecting to host
    print("Connection successful")

    cursor = connection.cursor()

    # prepare sql statement
    sql_static = f'CREATE TABLE IF NOT EXISTS static (' \
                 f'index FLOAT,' \
                 f'number FLOAT,' \
                 f'name VARCHAR(50),' \
                 f'address VARCHAR(50),' \
                 f'latitude FLOAT,' \
                 f'longitude FLOAT,' \
                 f'bike_stands FLOAT);'

    sql_dynamic = f'CREATE TABLE IF NOT EXISTS dynamic (' \
                  f'index FLOAT,' \
                  f'number FLOAT,' \
                  f'stands_available FLOAT,' \
                  f'bikes_available FLOAT,' \
                  f'status VARCHAR(50),' \
                  f'time DATETIME);'

    # execute and apply sql command
    cursor.execute(sql_static)
    cursor.execute(sql_dynamic)
    connection.commit()

    connection.close()

except Error as e:
    print(e)
