from app import create_app, db
from app.models.job import Job

app = create_app()
with app.app_context():
    count = Job.query.count()
    print("-" * 30)
    print(f"Total Jobs in Database: {count}")
    print("-" * 30)
    
    if count > 0:
        latest = Job.query.order_by(Job.posted_at.desc()).first()
        print(f"Latest Job: {latest.title} at {latest.company_name}")