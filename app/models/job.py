from datetime import datetime, timezone
from app.extensions import db  
from sqlalchemy.dialects.postgresql import JSONB
# ✅ STEP 1: Define the association table FIRST
# This links Jobs and Skills (Many-to-Many)
job_skills = db.Table('job_skills',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

# ✅ STEP 2: Define the Job class (ONLY ONCE)
class Job(db.Model):
    __tablename__ = "job"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False, default="Hyderabad")
    salary = db.Column(db.String(50), default="Not Disclosed")
    description = db.Column(db.Text)
    
    # 💡 Backend Tip: Since you have a relationship for skills below, 
    # you might not need this JSON column. Use the 'skills' relationship instead.
    skills_required = db.Column(db.JSON)

    # ✅ THE FIX: Ensuring the name is consistent
    # Using lambda for dynamic time generation
    posted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Optional: If you want to track edits separately
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    # ✅ RELATIONSHIP: Links to the 'Skill' model
    skills = db.relationship(
        "Skill",
        secondary=job_skills,
        backref=db.backref("jobs", lazy='dynamic'),
        lazy='selectin' 
    )

    # ✅ REPR: Used for debugging in terminal/logs
    def __repr__(self):
        return f"<Job {self.title} at {self.company_name}>"

    # ✅ TO_DICT: Essential for API responses
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company_name": self.company_name,
            "location": self.location,
            "salary": self.salary,
            "skills": [s.name for s in self.skills],
            "posted_at": self.posted_at.strftime("%b %d, %Y") if self.posted_at else "Recently"
        }
