from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # 🔥 GET DATABASE URL FROM ENV
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not set!")

    # 🔥 FIX: postgres:// → postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    # 🔥 APPLY CONFIG
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 🔥 REQUIRED FOR RENDER POSTGRES (VERY IMPORTANT)
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"sslmode": "require"}
    }

    # 🔐 JWT CONFIG
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-key")

    # ✅ INIT EXTENSIONS
    db.init_app(app)
    jwt.init_app(app)

    # ✅ IMPORT MODELS (avoid circular imports)
    from app.models.company import Company
    from app.models.job import Job
    from app.models.skill import Skill
    from app.models.user import User
    from app.models.job_skill import job_skills

    # ✅ IMPORT ROUTES
    from app.routes.job_routes import job_bp
    from app.routes.company_routes import company_bp
    from app.routes.skill_routes import skill_bp
    from app.routes.auth_routes import auth_bp

    # ✅ REGISTER ROUTES
    app.register_blueprint(job_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(skill_bp)
    app.register_blueprint(auth_bp)

    return app