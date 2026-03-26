from app import db
from datetime import datetime
from app.models.job_skill import job_skills
class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100))
    salary = db.Column(db.String(50))
    
    # 🔥 Foreign Key
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    skills = db.relationship(
    "Skill",
    secondary=job_skills,
    backref="jobs"
)