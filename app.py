
from flask import Flask
from routes.main_routes import main_bp
from routes.admin_routes import admin_bp
from routes.image_routes import image_bp

app = Flask(__name__)
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(image_bp)

if __name__ == "__main__":
    from db.connection import get_db_connection
    try:
        db = get_db_connection()
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