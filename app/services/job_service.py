from app.models.job import Job
from app import db

def save_job(data):
    job = Job(
        title=data["title"],
        location=data["location"],
        salary=data.get("salary", "Not Disclosed")
    )
    db.session.add(job)
    db.session.commit()