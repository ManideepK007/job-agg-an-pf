from app import create_app, db
from app.models.job import Job
from app.models.skill import Skill
from datetime import datetime, timezone, timedelta

app = create_app()

with app.app_context():
    print("🚀 Populating Pro-Level Job Data...")

    # 1. Define Skills (Keywords)
    skill_map = {
        "Python": Skill.query.filter_by(name="Python").first() or Skill(name="Python"),
        "Flask": Skill.query.filter_by(name="Flask").first() or Skill(name="Flask"),
        "React": Skill.query.filter_by(name="React").first() or Skill(name="React"),
        "Node.js": Skill.query.filter_by(name="Node.js").first() or Skill(name="Node.js"),
        "PostgreSQL": Skill.query.filter_by(name="PostgreSQL").first() or Skill(name="PostgreSQL"),
        "AWS": Skill.query.filter_by(name="AWS").first() or Skill(name="AWS"),
        "Machine Learning": Skill.query.filter_by(name="Machine Learning").first() or Skill(name="Machine Learning"),
        "Docker": Skill.query.filter_by(name="Docker").first() or Skill(name="Docker"),
        "TypeScript": Skill.query.filter_by(name="TypeScript").first() or Skill(name="TypeScript")
    }
    
    db.session.add_all(skill_map.values())
    db.session.commit()

    # 2. Detailed Job Data
    pro_jobs = [
        {
            "title": "Senior Backend Developer",
            "company": "Mahi FinTech",
            "location": "Hyderabad (Hitech City)",
            "salary": "18-25 LPA",
            "desc": "Lead the development of our core banking APIs. Experience with high-traffic Flask/Python applications and PostgreSQL optimization is mandatory.",
            "skills": ["Python", "Flask", "PostgreSQL"]
        },
        {
            "title": "Full Stack Engineer",
            "company": "Zindot Systems",
            "location": "Remote",
            "salary": "12-18 LPA",
            "desc": "Work on a modern MERN stack. You will be responsible for building responsive UI components and scalable Node.js microservices.",
            "skills": ["React", "Node.js", "TypeScript"]
        },
        {
            "title": "AI/ML Engineer",
            "company": "NeuralNode AI",
            "location": "Bangalore",
            "salary": "22-30 LPA",
            "desc": "Build and deploy LLM-based applications. Requires deep knowledge of Python, PyTorch, and deploying models on AWS SageMaker.",
            "skills": ["Python", "Machine Learning", "AWS"]
        },
        {
            "title": "Cloud Infrastructure Engineer",
            "company": "Nexus Cloud",
            "location": "Hyderabad",
            "salary": "15-22 LPA",
            "desc": "Manage multi-region AWS deployments. Strong expertise in Docker, Kubernetes, and Infrastructure as Code (Terraform) is required.",
            "skills": ["AWS", "Docker", "PostgreSQL"]
        },
        {
            "title": "Junior Data Analyst",
            "company": "Global Insight",
            "location": "Pune",
            "salary": "6-9 LPA",
            "desc": "Freshers welcome! Clean and visualize data to help business stakeholders make decisions. Strong SQL and Python skills are a must.",
            "skills": ["Python", "PostgreSQL"]
        },
        {
            "title": "Frontend Architect",
            "company": "Pixel Studio",
            "location": "Remote",
            "salary": "25-35 LPA",
            "desc": "Define the frontend architecture for our global e-commerce platform. Mastery of React, TypeScript, and Webpack is essential.",
            "skills": ["React", "TypeScript"]
        },
        {
            "title": "DevOps Specialist",
            "company": "SecureStream",
            "location": "Chennai",
            "salary": "14-20 LPA",
            "desc": "Automate CI/CD pipelines and enhance security protocols across our cloud environments using AWS and Docker.",
            "skills": ["AWS", "Docker", "Node.js"]
        },
        {
            "title": "Software Engineer II",
            "company": "Ubermensch Tech",
            "location": "Hyderabad",
            "salary": "20-28 LPA",
            "desc": "Scale our real-time messaging system. Focus on low-latency code and efficient database indexing using PostgreSQL.",
            "skills": ["Python", "Node.js", "PostgreSQL"]
        }
    ]

    # 3. Add to Database
    for data in pro_jobs:
        job = Job(
            title=data["title"],
            company_name=data["company"],
            location=data["location"],
            salary=data["salary"],
            description=data["desc"],
            posted_at=datetime.now(timezone.utc)
        )
        for s_name in data["skills"]:
            job.skills.append(skill_map[s_name])
        db.session.add(job)

    db.session.commit()
    print(f"✅ Successfully seeded {len(pro_jobs)} high-quality job listings!")