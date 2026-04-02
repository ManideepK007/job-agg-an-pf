from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv()

# Define extensions outside to avoid circular imports
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    # ✅ FIX: Ensure Flask knows where to find your UI templates
    app = Flask(__name__, template_folder='templates')

    # ==============================
    # 🔥 DATABASE CONFIG
    # ==============================
    database_url = os.getenv("DATABASE_URL")

    # Fallback for local development in Hyderabad
    if not database_url:
        database_url = "postgresql://postgres:postgres123@localhost:5432/jobdb"

    # Render Fix: SQLAlchemy 1.4+ requires 'postgresql://'
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ PRETTY PRINT: Helps with JSON readability in the browser
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
    app.config["JSON_AS_ASCII"] = False 

    # Robust connection settings for production/Render
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_timeout": 20,
    }

    # ==============================
    # 🔐 JWT CONFIG
    # ==============================
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-key")

    # ==============================
    # ⚙️ INIT EXTENSIONS
    # ==============================
    db.init_app(app)
    jwt.init_app(app)

    # ==============================
    # 🌐 REGISTER ROUTES & BLUEPRINTS
    # ==============================
    from app.routes.job_routes import job_bp
    from app.routes.company_routes import company_bp
    from app.routes.skill_routes import skill_bp
    from app.routes.auth_routes import auth_bp


    # ✅ IMPROVEMENT 1: Split UI and API logic
    # We remove the global '/api' prefix from job_bp so the UI 
    # (view-jobs) is clean, but the API routes stay under /api.
    
    app.register_blueprint(job_bp) # Now: /view-jobs and /init-db are clean
    app.register_blueprint(company_bp, url_prefix='/api')
    app.register_blueprint(skill_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # ==============================
    # 🧪 HEALTH CHECK
    # ==============================
    @app.route("/")
    def health():
        return {"status": "API running", "message": "Welcome to Mahi Job Portal"}, 200

    return app