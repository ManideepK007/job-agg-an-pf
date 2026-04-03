from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    # ✅ IMPROVEMENT: Pathlib ensures templates are found regardless of where you run the script
    base_dir = Path(__file__).resolve().parent
    app = Flask(__name__, 
                template_folder=str(base_dir / "templates"),
                static_folder=str(base_dir / "static"))

    # 🔥 DATABASE CONFIG
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres123@localhost:5432/jobdb")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config.update(
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JSONIFY_PRETTYPRINT_REGULAR=True,
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "skill-sync-dev-7788")
    )

    # ⚙️ INIT EXTENSIONS
    db.init_app(app)
    jwt.init_app(app)

    # 🌐 REGISTER ROUTES & BLUEPRINTS
    from app.routes.job_routes import job_bp
    from app.routes.company_routes import company_bp
    from app.routes.skill_routes import skill_bp
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(job_bp) 
    app.register_blueprint(company_bp, url_prefix='/api')
    app.register_blueprint(skill_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # ✅ IMPROVEMENT: Global variable for templates (saves time renaming later)
    @app.context_processor
    def inject_globals():
        return {'app_name': 'SkillSync'}

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/api/status")
    def health():
        return {
            "status": "online",
            "project": "SkillSync",
            "version": "1.1.0",
            "environment": "Development",
            "db_connected": database_url.split('@')[-1] # Hides password for security
        }, 200

    return app