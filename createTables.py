import mysql.connector
from mysql.connector import errorcode
import os

# Obtain connection string information from the portal

config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE')
}

# Create connection and cursor
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# Create table
cursor.execute("CREATE TABLE images (id serial PRIMARY KEY, file VARCHAR(255), description TEXT, tags TEXT);")
print("Finished creating table.")

# Close cursor and connection
cursor.close()
cnx.close()
