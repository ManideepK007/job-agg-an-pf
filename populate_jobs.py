from app import create_app, db
from app.models.job import Job
from datetime import datetime, timedelta

app = create_app()

def run_seed():
    with app.app_context():
        # Optional: db.drop_all(); db.create_all() if you want a clean slate
        
        job_data = [
            # HYDERABAD JOBS
            {"title": "Junior Backend Developer", "company": "Mahi Fashion", "loc": "Hyderabad", "sal": "6-9 LPA", "skills": "Python, Flask, PostgreSQL"},
            {"title": "Data Analyst Intern", "company": "TechSol", "loc": "Hyderabad", "sal": "4-6 LPA", "skills": "Python, SQL, PowerBI"},
            {"title": "Full Stack Engineer", "company": "CloudNexus", "loc": "Hyderabad", "sal": "10-15 LPA", "skills": "Next.js, Node.js, MongoDB"},
            
            # REMOTE JOBS
            {"title": "Python Developer (Remote)", "company": "ByteStream", "loc": "Remote", "sal": "8-12 LPA", "skills": "Python, Django, AWS"},
            {"title": "ML Engineer Trainee", "company": "LedgerLogic", "loc": "Remote", "sal": "7-10 LPA", "skills": "Python, Scikit-learn, Pandas"},
            
            # BANGALORE JOBS
            {"title": "Software Engineer I", "company": "UrbanCart", "loc": "Bangalore", "sal": "12-18 LPA", "skills": "Java, Spring Boot, Microservices"},
            {"title": "DevOps Associate", "company": "CloudNexus", "loc": "Bangalore", "sal": "9-13 LPA", "skills": "Docker, Kubernetes, Linux"}
        ]

        # Duplicate/Adjust this list to reach 20 jobs
        for data in job_data:
            job = Job(
                title=data['title'],
                company_name=data['company'],
                location=data['loc'],
                salary=data['sal'],
                description=f"Join {data['company']} as a {data['title']}. We are looking for motivated freshers...",
                skills_required=data['skills'],
                posted_on=datetime.utcnow() - timedelta(days=job_data.index(data)) # Varies dates
            )
            db.session.add(job)
        
        db.session.commit()
        print(f"Successfully added {len(job_data)} jobs!")

if __name__ == "__main__":
    run_seed()