from flask import Blueprint, render_template, request
from db.connection import get_db_connection, s3, BUCKET
from datetime import datetime
import pytz

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        action = request.form.get("action")
        report_id = request.form.get("report_id")
        if action == "delete":
            try:
                db = get_db_connection()
                cursor = db.cursor()
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
                db = get_db_connection()
                cursor = db.cursor()
                cursor.execute("UPDATE reports SET resolved = 1 WHERE id = %s", (report_id,))
                db.commit()
                cursor.close()
                db.close()
            except Exception as e:
                return f"Error resolving report: {e}"
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
    return render_template("admin.html", rows=formatted_rows)
