from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
jwt = JWTManager()   # ✅ better practice (init separately)


def create_app():
    app = Flask(__name__)

    # 🔥 DATABASE CONFIG (ENV FIRST, LOCAL FALLBACK)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:YOUR_PASSWORD@localhost/jobdb"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 🔐 JWT SECRET (ENV FIRST)
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY",
        "dev-secret-key"
    )

    # ✅ Init extensions
    db.init_app(app)
    jwt.init_app(app)

    # ✅ Import models (avoid circular import)
    from app.models.company import Company
    from app.models.job import Job
    from app.models.skill import Skill
    from app.models.user import User
    from app.models.job_skill import job_skills

    # ✅ Import routes
    from app.routes.job_routes import job_bp
    from app.routes.company_routes import company_bp
    from app.routes.skill_routes import skill_bp
    from app.routes.auth_routes import auth_bp

    # ✅ Register routes
    app.register_blueprint(job_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(skill_bp)
    app.register_blueprint(auth_bp)

    return app