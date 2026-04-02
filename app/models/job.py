from app import db
from datetime import datetime, timezone

# ✅ STEP 1: Define the association table FIRST (Above the class)
job_skills = db.Table('job_skills',
    db.Column('job_id', db.Integer, db.ForeignKey('jobs.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'), primary_key=True),
    extend_existing=True 
)

# ✅ STEP 2: Define the Job class SECOND
class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100), index=True) 
    salary = db.Column(db.String(50))
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"))
    
    # Modernized UTC time for 2026 standards
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Now job_skills is already known to Python, so no NameError!
    skills = db.relationship(
        "Skill",
        secondary=job_skills,
        backref=db.backref("jobs", lazy='dynamic'),
        lazy='selectin' 
    )

    def __repr__(self):
        return f"<Job {self.title} in {self.location}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "location": self.location or "Hyderabad",
            "salary": self.salary or "Not Disclosed",
            "skills": [s.name for s in self.skills],
            "posted_on": self.created_at.strftime("%b %d, %Y") if self.created_at else "Recently"
        }