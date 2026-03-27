from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # ==============================
    # 🔥 DATABASE CONFIG
    # ==============================
    database_url = os.getenv("DATABASE_URL")

    # ✅ fallback for local development
    if not database_url:
        database_url = "postgresql://postgres:postgres123@localhost:5432/jobdb"

    # ✅ fix Render old postgres:// issue
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ IMPORTANT: prevent hanging DB connections
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_timeout": 20,
    }

    # ==============================
    # 🔐 JWT CONFIG
    # ==============================
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY",
        "dev-secret-key"
    )

    # ==============================
    # ⚙️ INIT EXTENSIONS
    # ==============================
    db.init_app(app)
    jwt.init_app(app)

    # ==============================
    # 📦 IMPORT MODELS
    # ==============================
    from app.models.company import Company
    from app.models.job import Job
    from app.models.skill import Skill
    from app.models.user import User
    from app.models.job_skill import job_skills

    # ==============================
    # 🌐 REGISTER ROUTES
    # ==============================
    from app.routes.job_routes import job_bp
    from app.routes.company_routes import company_bp
    from app.routes.skill_routes import skill_bp
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(job_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(skill_bp)
    app.register_blueprint(auth_bp)

    # ==============================
    # 🧪 HEALTH CHECK
    # ==============================
    @app.route("/")
    def health():
        return {"status": "API running"}, 200

    return app