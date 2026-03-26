from app import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    industry = db.Column(db.String(100))
    location = db.Column(db.String(100))
    website = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)