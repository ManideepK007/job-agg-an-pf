from app import create_app, db
from app.models.job import Job
from app.models.company import Company
from app.models.skill import Skill
from app.models.user import User

app = create_app()

def seed_data():
    with app.app_context():
        print("🌱 Seeding database...")
        
        # 1. Clear existing data (Optional - Be careful!)
        db.drop_all()
        db.create_all()

        # 2. Create Skills
        python = Skill(name="Python")
        flask = Skill(name="Flask")
        react = Skill(name="React")
        sql = Skill(name="PostgreSQL")
        db.session.add_all([python, flask, react, sql])

        # 3. Create a Company
        company = Company(name="Mahi Tech Solutions", location="Hyderabad", website="https://mahi.fashion")
        db.session.add(company)
        db.session.commit() # Commit to get the IDs

        # 4. Create Jobs with Linked Skills
        job1 = Job(title="Backend Developer", location="Hyderabad", salary="8 LPA", company_id=company.id)
        job1.skills.append(python)
        job1.skills.append(flask)

        job2 = Job(title="Frontend Engineer", location="Bangalore", salary="12 LPA", company_id=company.id)
        job2.skills.append(react)

        db.session.add_all([job1, job2])
        
        # 5. Create an Admin User for Testing
        admin = User(username="admin", email="admin@mahi.com", role="admin")
        admin.set_password("admin123") # Ensure your User model has this method
        db.session.add(admin)

        db.session.commit()
        print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed_data()