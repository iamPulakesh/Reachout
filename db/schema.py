from db.connection import get_db_connection


CREATE_REPORTS_TABLE_SQL = (
    '''
    CREATE TABLE IF NOT EXISTS reports (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        incident_type VARCHAR(100),
        address VARCHAR(255),
        lat FLOAT,
        lng FLOAT,
        image_name VARCHAR(255),
        timestamp BIGINT,
        resolved TINYINT(1) DEFAULT 0,
        reporter_name VARCHAR(100),
        reporter_phone VARCHAR(32)
    )
    '''
)


def ensure_schema() -> None:

    db = get_db_connection()
    try:
        cur = db.cursor()
        cur.execute(CREATE_REPORTS_TABLE_SQL)
        db.commit()

    finally:
        try:
            cur.close()
        except Exception:
            pass
        db.close()
