from flask import Blueprint, render_template, request
import logging
from db.connection import get_db_connection
from utils.s3_utils import delete_objects
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
                row = cursor.fetchone()
                attachment_keys = []
                if row and row[0]:
                    attachment_keys = [k.strip() for k in row[0].split(',') if k.strip()]
                    failed = delete_objects(attachment_keys)
                    if failed:
                        logging.getLogger(__name__).warning(
                            "Partial S3 delete failure", extra={
                                "failed_keys": failed,
                                "report_id": report_id,
                                "total_keys": len(attachment_keys)
                            }
                        )
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
