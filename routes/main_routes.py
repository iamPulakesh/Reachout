from flask import Blueprint, render_template, request
from db.connection import get_db_connection, GOOGLE_MAPS_API_KEY, S3_BASE_URL, s3, BUCKET
import time
from datetime import datetime
import pytz

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
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
            db = get_db_connection()
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
        return render_template('success.html')
    return render_template('index.html', google_maps_key=GOOGLE_MAPS_API_KEY, s3_base_url=S3_BASE_URL)

@main_bp.route('/all-reports')
def all_reports():
    db = get_db_connection()
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
