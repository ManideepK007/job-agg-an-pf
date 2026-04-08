import random
from app import create_app, db
from app.extensions import db
from app.models.job import Job
from app.models.user import User

app = create_app()

def seed_data():
    with app.app_context():
        print("🧹 Clearing old data...")
        db.session.query(Job).delete()
        db.session.commit()

        # Data for variety
        companies = ["TCS", "Infosys", "Google (Hyd)", "Tata", "Microsoft", "IBM", "Wipro", "Accenture", "Amazon India", "Flipkart", "CMR Foundation"]
        locations = ["Hitech City, Hyderabad", "Gachibowli, Hyderabad", "Bangalore (Remote)", "Pune", "Madhapur, Hyderabad"]
        titles = [
            "Junior Python Developer", "React Frontend Engineer", "Data Analyst", 
            "QA Automation Tester", "DevOps Trainee", "Full Stack Developer",
            "Business Analyst", "Machine Learning Intern", "Artificial Intelligence Trainee", "Cloud Engineer",
            "Software Engineer I", "Software Engineer II", "Associate Software Engineer", "Trainee Software Developer",
            "Junior Backend Developer", "Frontend Developer Intern", "Data Scientist Trainee", "UI/UX Designer Intern",
            "Mobile App Developer", "Cybersecurity Analyst Trainee"
        ]
        
        print("🌱 Planting 20 new jobs...")
        for i in range(20):
            job = Job(
                title=random.choice(titles),
                company_name=random.choice(companies),
                location=random.choice(locations),
                salary=f"₹{random.randint(4, 15)},00,000 - ₹{random.randint(16, 25)},00,000",
                description=f"Exciting opportunity for a fresher to join our {random.choice(titles)} team. Growth guaranteed!",
                skills_required=["Python", "SQL", "Git", "Flask"] if "Python" in titles else ["React", "CSS", "JS"]
            )
            db.session.add(job)
        
        db.session.commit()
        print("✨ Your portal is now packed with data!")

if __name__ == "__main__":
    seed_data()