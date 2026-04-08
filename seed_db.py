from app import create_app, db
from app.models.job import Job
from datetime import datetime

app = create_app()

def seed_jobs():
    with app.app_context():
        # Clear existing jobs if you want a fresh start
        # Job.query.delete() 

        job1 = Job(
            title="Junior Python Developer",
            company_name="Mahi Fashion Tech",
            location="Hyderabad",
            salary="5-8 LPA",
            description="We are looking for a fresher to handle Flask backend tasks...",
            skills_required="Python, Flask, MongoDB",
            posted_on=datetime.utcnow()
        )

        db.session.add(job1)
        db.session.commit()
        print("Database Seeded Successfully!")

if __name__ == "__main__":
    seed_jobs()