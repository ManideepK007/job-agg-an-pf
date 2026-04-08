import os
from pathlib import Path
from flask import Flask, render_template
from dotenv import load_dotenv
from app.extensions import db, login_manager, jwt, migrate

def create_app():
    # 1. PATH SETUP
    base_dir = Path(__file__).resolve().parent
    load_dotenv(base_dir.parent / ".env")

    app = Flask(__name__, 
                template_folder=str(base_dir / "templates"),
                static_folder=str(base_dir / "static"))
    app.config.from_object('config.Config')
    # 2. CONFIGURATION
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "postgresql://postgres:postgres123@localhost:5432/jobdb"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "skill-sync-dev-7788"),
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-secret-123"),
        SESSION_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_HTTPONLY=True,
    )

    # 3. INIT EXTENSIONS
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    
    # 4. DATABASE INITIALIZATION
    # We enter the app context to perform database operations
    with app.app_context():
        # Import all models here so SQLAlchemy "sees" them
        from app.models.user import User
        from app.models.job import Job
        from app.models.application import Application
        from app.models.skill import Skill  # CRITICAL: Fixes the User.skills error
        
        # This creates the tables if they don't exist
        # It ensures your 'user_skills' bridge is built correctly
        db.create_all()

    # 5. AUTHENTICATION HELPERS
    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User # Local import to avoid circularity
        return User.query.get(int(user_id))

    # 6. REGISTER BLUEPRINTS
    from app.routes.job_routes import job_bp
    from app.routes.company_routes import company_bp
    from app.routes.skill_routes import skill_bp
    from app.routes.auth_routes import auth_bp
    
    app.register_blueprint(job_bp)
    app.register_blueprint(auth_bp) 
    app.register_blueprint(company_bp, url_prefix='/api/companies')
    app.register_blueprint(skill_bp, url_prefix='/api/skills')

    # 7. GLOBAL ROUTES & ERROR HANDLING
    @app.route("/")
    def index():
        return render_template('index.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app