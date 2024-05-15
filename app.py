from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import uuid
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

load_dotenv()

# Create flask app
app = Flask(__name__)

def create_db_connection():
    # Create DB connection
    cnx = mysql.connector.connect(user=os.getenv('DB_USER'), password=os.getenv("DB_PASSWORD"), host=os.getenv('DB_HOST'), port=3306, database=os.getenv('DB_DATABASE'), ssl_disabled=True)
    # Create a cursor object to execute SQL queries
    cursor = cnx.cursor()

    # Check if the table images already exists
    cursor.execute("SHOW TABLES LIKE 'images'")
    result = cursor.fetchone()
    if result:
        print("Table 'images' already exists.")
    else:
        create_table(cursor)

    return cnx, cursor

def create_table(cursor):
    cursor.execute("""
        CREATE TABLE images (
            id INT AUTO_INCREMENT PRIMARY KEY,
            file TEXT,
            description TEXT,
            tags TEXT,
            confidence FLOAT
        )
    """)

@app.route('/', methods=['GET'])
def home():
    return 'Bienvenue sur l\'api de Fayel et Milan.', 200

@app.route('/images', methods=['POST'])
def upload_images():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    file.save(os.path.join('uploads', file.filename))
    upload_file_path = os.path.join('uploads', file.filename)

    # Create clientblob
    conn_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # Generate a unique id for the filename
    unique_id = str(uuid.uuid4())
    filename = f"{unique_id}_{file.filename}"

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)

    # Create a blob client using the generated filename as the name for the blob
    blob_client = blob_service_client.get_blob_client(container="images", blob=filename)

    # Upload the created file
    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)

    # Get the URL of the uploaded blob
    uploaded_blob_url = blob_client.url

    # Get the description and tags from azure computer vision

    # Create the Computer Vision client
    region = os.getenv('ACCOUNT_REGION')
    key = os.getenv('ACCOUNT_KEY')

    credentials = CognitiveServicesCredentials(key)
    client = ComputerVisionClient(
        endpoint="https://" + region + ".api.cognitive.microsoft.com/",
        credentials=credentials
    )

    language = "en"
    max_descriptions = 15

    analysis = client.describe_image(uploaded_blob_url, max_descriptions, language)

    # Get tags 
    tags = analysis.tags
    for tag in tags:
        print(tag)
        

    for caption in analysis.captions:
        print(caption.text)
        print(caption.confidence)
    

    # Create connection to the db
    cnx, cursor = create_db_connection()

    # Insert the link to the image, the description and the tags in the database
    query = "INSERT INTO images (file, description, tags, confidence) VALUES (%s, %s, %s, %s)"

    # Execute the query
    print(uploaded_blob_url)
    cursor.execute(query, (uploaded_blob_url, caption.text, str(tags), caption.confidence))

    # Commit the transaction
    cnx.commit()
    cursor.close()
    cnx.close()

    # Delete the image from the local storage
    os.remove(upload_file_path)
    
    return 'Image uploaded successfully', 200

@app.route('/images', methods=['GET'])
def hello():
    # Execute a SELECT query to fetch all data from a table
    cnx, cursor = create_db_connection()
    cursor.execute("SELECT * FROM images")
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()
    
    # Create a list to store the results
    results = []
    print(rows)
    for row in rows:
        results.append({
            "file" : row[1],
            "description": row[2],
            "tags": row[3],
            "confidence": row[4]
        })
    return jsonify(results), 200

# Route to get image by description
@app.route('/images/description', methods=['POST'])
def get_image_by_description():
    # Get the description from the request body
    data = request.get_json()
    description = data.get('description')

    # Create connection to the db
    cnx, cursor = create_db_connection()

    # Execute a SELECT query to fetch all data from a table
    cursor.execute("SELECT * FROM images WHERE description LIKE %s", (f"%{description}%",))
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    # Create a list to store the results
    results = []
    for row in rows:
        results.append({
            "file" : row[1],
            "description": row[2],
            "tags": row[3],
            "confidence": row[4]
        })
    return jsonify(results), 200

# Route to find image by tags
@app.route('/images/<tag>', methods=['GET'])
def get_image_by_tag(tag):
    # Create connection to the db
    cnx, cursor = create_db_connection()

    # Execute a SELECT query to fetch all data from a table
    cursor.execute("SELECT * FROM images WHERE tags LIKE %s", (f"%{tag}%",))
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    # Create a list to store the results
    results = []
    for row in rows:
        results.append({
            "file" : row[1],
            "description": row[2],
            "tags": row[3],
            "confidence": row[4]
        })
    return jsonify(results), 200

# Route to get all the tags of the images
@app.route('/tags', methods=['GET'])
def get_tags():
    # Create connection to the db
    cnx, cursor = create_db_connection()

    # Execute a SELECT query to fetch all data from a table
    cursor.execute("SELECT tags FROM images")
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    # Create a list to store the results
    results = []
    for row in rows:
        results.append(row[0])
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)