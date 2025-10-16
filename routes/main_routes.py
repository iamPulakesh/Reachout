from flask import Blueprint, render_template, request, jsonify
from db.connection import get_db_connection, GOOGLE_MAPS_API_KEY, S3_BASE_URL, s3, BUCKET
import time
from datetime import datetime
import pytz
import requests
import phonenumbers

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('attachments')
        reporter_name = request.form.get('reporter_name')
        # Expecting E.164 from hidden field and dial code from hidden country_code
        phone_e164 = request.form.get('reporter_phone', '')
        country_code = request.form.get('country_code', '')
        # Server-side validation with phonenumbers
        try:
            parsed = phonenumbers.parse(phone_e164, None)  # E.164 includes country
            if not phonenumbers.is_valid_number(parsed):
                return "Invalid phone number.", 400
            # Optionally normalize to E.164
            reporter_phone = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except Exception:
            return "Invalid phone number.", 400
        address = request.form['address']
        lat = request.form['lat']
        lng = request.form['lng']
        incident_type = request.form['type']
        timestamp = int(time.time())
        
        if not (1 <= len(files) <= 3):
            return "Please upload 1 to 3 files."
        allowed_exts = {'png', 'jpg', 'jpeg', 'mp4'}
        filenames = []
        for file in files:
            ext = file.filename.rsplit('.', 1)[-1].lower()
            if ext not in allowed_exts:
                return "Only png, jpg, jpeg, and mp4 files are allowed."
            unique_name = f"{incident_type}_{timestamp}_{file.filename}"
            s3.upload_fileobj(file, BUCKET, unique_name)
            filenames.append(unique_name)
        try:
            db = get_db_connection()
            cursor = db.cursor()
            insert_query = '''
                INSERT INTO reports (incident_type, address, lat, lng, image_name, timestamp, resolved, reporter_name, reporter_phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (
                incident_type, address, lat, lng, ','.join(filenames), timestamp, 0, reporter_name, reporter_phone
            ))
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

@main_bp.route('/fetch-location', methods=['POST'])
def fetch_location_post():
    """
    Reverse geocode coordinates provided by the client (e.g., from browser GPS).
    Expects JSON body: { "lat": <float>, "lng": <float> }
    Returns JSON: { address, lat, lng }
    """
    try:
        data = request.get_json(silent=True) or {}
        lat = data.get('lat')
        lng = data.get('lng')
        if lat is None or lng is None:
            return jsonify({"error": "lat and lng are required"}), 400
        try:
            flat = float(lat)
            flng = float(lng)
        except (TypeError, ValueError):
            return jsonify({"error": "lat and lng must be numbers"}), 400

        g_url = (
            "https://maps.googleapis.com/maps/api/geocode/json"
            f"?latlng={flat},{flng}&key={GOOGLE_MAPS_API_KEY}"
        )
        g_res = requests.get(g_url, timeout=7)
        if g_res.status_code != 200:
            return jsonify({"error": "Reverse geocoding failed"}), 502
        g = g_res.json()
        address = (
            g.get("results", [{}])[0].get("formatted_address")
            if g.get("results") else None
        )
        return jsonify({
            "address": address or f"Lat {flat}, Lng {flng}",
            "lat": flat,
            "lng": flng,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
