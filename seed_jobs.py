from sqlalchemy import text # Import text for raw SQL

with app.app_context():
    print("Emptying tables to prevent errors...")
    
    # 1. Clear existing data (Order matters because of Foreign Keys!)
    # Using TRUNCATE is faster and resets the ID counters to 1
    db.session.execute(text('TRUNCATE TABLE job_skills, job, skill RESTART IDENTITY CASCADE;'))
    db.session.commit()

    # 2. Now run your existing seed logic...
    python = Skill(name="Python")
    # ... (rest of your seed code)
    
    db.session.commit()
    print("✅ Database refreshed and seeded!")