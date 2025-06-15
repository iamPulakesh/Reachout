from flask import Flask, render_template, request
import boto3
import time
import os
import mysql.connector
from datetime import datetime

app = Flask(__name__)
s3 = boto3.client('s3')
BUCKET = 's3_bucket_name'  # S3 bucket name

# RDS DB connection config
DB_HOST = 'your_rds_endpoint'
DB_USER = 'username'
DB_PASSWORD = 'password'
DB_NAME = 'db_name'

@app.route("/all-reports")
def all_reports():
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM reports")
    rows = cursor.fetchall()

    formatted_rows = []
    for row in rows:
        new_row = list(row)
        new_row[6] = datetime.utcfromtimestamp(int(row[6])).strftime('%Y-%m-%d %H:%M:%S')
        formatted_rows.append(new_row)

    return render_template("view_reports.html", rows=formatted_rows)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        address = request.form['address']
        lat = request.form['lat']
        lng = request.form['lng']
        incident_type = request.form['type']
        timestamp = int(time.time())
        filename = f"{incident_type}_{timestamp}.jpg"

        s3.upload_fileobj(file, BUCKET, filename)

        # Storing in the rds
        try:
            db = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = db.cursor()
            insert_query = '''
                INSERT INTO reports (incident_type, address, lat, lng, image_name, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (incident_type, address, lat, lng, filename, timestamp))
            db.commit()
            cursor.close()
            db.close()
        except Exception as e:
            return f"Error saving to DB: {e}"

        return "Incident Reported Successfully!"

    return render_template('index.html')

if __name__ == "__main__":
    # Create table if not exists it will run only once
    try:
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                incident_type VARCHAR(100),
                address VARCHAR(255),
                lat FLOAT,
                lng FLOAT,
                image_name VARCHAR(255),
                timestamp BIGINT
            )
        ''')
        db.commit()
        cursor.close()
        db.close()
        print("Table created or already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")

    app.run(host="0.0.0.0", port=80)
