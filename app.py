from flask import Flask, request
import requests
from PIL import Image
from io import BytesIO
import mysql.connector
from werkzeug.utils import secure_filename
import os
from flask import jsonify
import os

app = Flask(__name__)

@app.route('/image', methods=['POST'])
def upload_images():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join('uploads', filename))
    return 'Image uploaded successfully', 200

# Connect to the MySQL database
cnx = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_DATABASE'),
    ssl_ca="DigiCertGlobalRootCA.crt.pem",
    ssl_disabled=False
)

# Create a cursor object to execute SQL queries
cursor = cnx.cursor()

@app.route('/', methods=['GET'])
def hello():
    # Execute a SELECT query to fetch all data from a table
    query = "SELECT * FROM your_table"
    cursor.execute(query)
    
    # Fetch all rows from the result set
    rows = cursor.fetchall()

    print(rows)
    
    data = []

    # Iterate over the rows and create a JSON object
    for row in rows:
        obj = {
            'id': row[0],
            'file': row[1],
            'description': row[2],
            'tags': row[3]
        }
        data.append(obj)

    
    # Return the JSON object
    return jsonify(data), 200

# Close the cursor and the database connection
cursor.close()
cnx.close()

if __name__ == '__main__':
    app.run(debug=True)