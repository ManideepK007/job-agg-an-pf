from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager # <--- Add this
from flask_migrate import Migrate # <--- Add this for database migrations

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager() # <--- Add this
migrate=Migrate()