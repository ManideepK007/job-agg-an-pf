from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# 1. User Table (The Identity)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='seeker') # 'seeker' or 'recruiter'
    
    # Relationships
    profile = db.relationship('Profile', backref='user', uselist=False)
    jobs_posted = db.relationship('Job', backref='recruiter', lazy=True)

# 2. Profile Table (The Data - Skills & Experience)
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    skills = db.Column(db.JSON)  # Stores as ["Python", "Flask", "PostgreSQL"]
    experience_years = db.Column(db.Integer, default=0)
    resume_path = db.Column(db.String(255)) # Link to the uploaded PDF

# 3. Job Table (The Requirements)
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
    salary = db.Column(db.String(50))
    description = db.Column(db.Text)
    required_skills = db.Column(db.JSON) # Stores as ["Python", "AWS"]
    posted_on = db.Column(db.DateTime, default=datetime.utcnow)

# 4. Applications Table (The Connection/ATS)
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    seeker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='Applied') # 'Shortlisted', 'Rejected'
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)