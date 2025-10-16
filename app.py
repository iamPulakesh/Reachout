from flask import Flask
import os
from dotenv import load_dotenv
from routes.main_routes import main_bp
from routes.admin_routes import admin_bp
from routes.image_routes import image_bp
from db.schema import ensure_schema

load_dotenv()

secret_key = os.getenv('SECRET_KEY')
if not secret_key:
    raise RuntimeError('SECRET_KEY is not set')

app = Flask(__name__)
app.secret_key = secret_key
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(image_bp)

if __name__ == "__main__":
    # Ensure DB schema exists at startup
    try:
        ensure_schema()
        print("Database schema created/existed.")
    except Exception as e:
        print(f"Error creating schema: {e}")
    app.run(host="0.0.0.0", port=80)