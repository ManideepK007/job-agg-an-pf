from app import create_app, db
from app.models.job import Job
from app.models.skill import Skill
from datetime import datetime, timezone, timedelta

app = create_app()

with app.app_context():
    print("🚀 Starting Bulk Seed...")
    
    # 1. Define common skills
    skill_names = ["Python", "Flask", "React", "Node.js", "PostgreSQL", "AWS", "Docker", "Machine Learning"]
    skills = {}
    for name in skill_names:
        s = db.session.query(Skill).filter_by(name=name).first()
        if not s:
            s = Skill(name=name)
            db.session.add(s)
        skills[name] = s
    db.session.commit()

    # 2. Define 10 diverse jobs
    jobs_to_add = [
        ("Backend Developer", "Mahi Systems", "Hyderabad", "8-12 LPA", ["Python", "Flask", "PostgreSQL"]),
        ("Full Stack Engineer", "TechNova", "Remote", "10-15 LPA", ["React", "Node.js", "Docker"]),
        ("Data Scientist", "Insight AI", "Bangalore", "12-20 LPA", ["Python", "Machine Learning"]),
        ("DevOps Engineer", "CloudScale", "Hyderabad", "9-14 LPA", ["AWS", "Docker"]),
        ("Frontend Developer", "PixelPerfect", "Pune", "7-11 LPA", ["React"]),
        ("Junior Web Developer", "StartUp Hub", "Hyderabad", "5-7 LPA", ["Flask", "PostgreSQL"]),
        ("Software Architect", "Enterprise Corp", "Remote", "25-35 LPA", ["AWS", "Node.js", "PostgreSQL"]),
        ("Python Developer", "CodeCraft", "Hyderabad", "6-10 LPA", ["Python", "Flask"]),
        ("ML Ops Engineer", "DataBridge", "Gurgaon", "15-22 LPA", ["Python", "Docker", "Machine Learning"]),
        ("API Specialist", "ConnectIt", "Remote", "8-13 LPA", ["Node.js", "PostgreSQL"])
    ]

    for title, company, loc, sal, req_skills in jobs_to_add:
        # Create unique posting times so the "Latest" sorting works
        offset = jobs_to_add.index((title, company, loc, sal, req_skills))
        posted_time = datetime.now(timezone.utc) - timedelta(days=offset)

        job = Job(
            title=title,
            company_name=company,
            location=loc,
            salary=sal,
            description=f"Join {company} as a {title}. We are looking for talented individuals to join our growing team in {loc}.",
            posted_at=posted_time
        )
        
        # Link Skill objects
        for s_name in req_skills:
            job.skills.append(skills[s_name])
            
        db.session.add(job)

    db.session.commit()
    print(f"✅ Successfully added {len(jobs_to_add)} new jobs to the portal!")