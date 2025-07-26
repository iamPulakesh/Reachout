from flask import Flask, render_template, request, redirect, url_for
import boto3
import time
import os
import mysql.connector
from datetime import datetime
import pytz

app = Flask(__name__)

def get_ssm_parameter(name, secure=False):
    ssm = boto3.client('ssm', region_name='ap-south-1')
    return ssm.get_parameter(Name=name, WithDecryption=secure)['Parameter']['Value']

# Fetching DB creds and other secrets from AWS SSM
DB_HOST = get_ssm_parameter("/reachout/DB_HOST")
DB_USER = get_ssm_parameter("/reachout/DB_USER")
DB_PASSWORD = get_ssm_parameter("/reachout/DB_PASSWORD", secure=True)
DB_NAME = get_ssm_parameter("/reachout/DB_NAME")
GOOGLE_MAPS_API_KEY = get_ssm_parameter("/reachout/GOOGLE_MAPS_API_KEY", secure=True)
S3_BASE_URL = get_ssm_parameter("/reachout/S3_BASE_URL")
BUCKET = get_ssm_parameter("/reachout/S3_BUCKET")

s3 = boto3.client('s3', region_name='ap-south-1')

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

        try:
            db = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cursor = db.cursor()
            insert_query = '''
                INSERT INTO reports (incident_type, address, lat, lng, image_name, timestamp, resolved)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (incident_type, address, lat, lng, filename, timestamp, 0))
            db.commit()
            cursor.close()
            db.close()
        except Exception as e:
            return f"Error saving to DB: {e}"

        return '''
            <html>
                <head><title>Success</title>
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

    return render_template('index.html', google_maps_key=GOOGLE_MAPS_API_KEY, s3_base_url=S3_BASE_URL)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        action = request.form.get("action")
        report_id = request.form.get("report_id")

        if action == "delete":
            try:
                db = mysql.connector.connect(
                    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
                )
                cursor = db.cursor()

                # Delete image from S3
                cursor.execute("SELECT image_name FROM reports WHERE id = %s", (report_id,))
                image = cursor.fetchone()
                if image:
                    s3.delete_object(Bucket=BUCKET, Key=image[0])

                cursor.execute("DELETE FROM reports WHERE id = %s", (report_id,))
                db.commit()
                cursor.close()
                db.close()
            except Exception as e:
                return f"Error deleting report: {e}"
        elif action == "resolve":
            try:
                db = mysql.connector.connect(
                    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
                )
                cursor = db.cursor()
                cursor.execute("UPDATE reports SET resolved = 1 WHERE id = %s", (report_id,))
                db.commit()
                cursor.close()
                db.close()
            except Exception as e:
                return f"Error resolving report: {e}"

    db = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
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

    return render_template("admin.html", rows=formatted_rows)

@app.route("/view-image/<image_name>")
def view_image(image_name):
    try:
        signed_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET, 'Key': image_name},
            ExpiresIn=300 
        )
        return redirect(signed_url)
    except Exception as e:
        return f"Error generating signed URL: {e}"

if __name__ == "__main__":
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
                timestamp BIGINT,
                resolved TINYINT(1) DEFAULT 0
            )
        ''')
        db.commit()
        cursor.close()
        db.close()
        print("Table created or already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")

    app.run(host="0.0.0.0", port=80)
