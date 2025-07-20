from flask import Flask, render_template, request
import boto3
import time
import os
import mysql.connector
from datetime import datetime
import pytz

app = Flask(__name__)
s3 = boto3.client('s3')
BUCKET = 'cf-templates-1dif3fweoqwe7-ap-south-1'  # S3 bucket name

def get_ssm_parameter(name, secure=False):
    ssm = boto3.client('ssm', region_name='ap-south-1')
    return ssm.get_parameter(Name=name, WithDecryption=secure)['Parameter']['Value']

# Fetching DB creds and API via ssm
DB_HOST = get_ssm_parameter("/reachout/DB_HOST")
DB_USER = get_ssm_parameter("/reachout/DB_USER")
DB_PASSWORD = get_ssm_parameter("/reachout/DB_PASSWORD", secure=True)
DB_NAME = get_ssm_parameter("/reachout/DB_NAME")
GOOGLE_MAPS_API_KEY = get_ssm_parameter("/reachout/GOOGLE_MAPS_API_KEY", secure=True)
S3_BASE_URL = get_ssm_parameter("/reachout/S3_BASE_URL")

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
    local_tz = pytz.timezone('Asia/Kolkata')
    for row in rows:
        new_row = list(row)
        dt = datetime.fromtimestamp(int(row[6]), tz=pytz.utc).astimezone(local_tz)
        new_row[6] = dt.strftime('%Y-%m-%d %H:%M:%S')
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

        return '''
            <html>
                <head>
                    <title>Success</title>
                    <script>
                        setTimeout(function() {
                            window.location.href = "/";
                        }, 5000);
                    </script>
                </head>
                <body>
                    <h2>Incident Reported Successfully!</h2>
                    <p>You will be redirected to the homepage shortly...</p>
                </body>
            </html>
        '''


    return render_template('index.html', google_maps_key=GOOGLE_MAPS_API_KEY, s3_base_url=S3_BASE_URL )

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