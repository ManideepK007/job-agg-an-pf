import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. THE CONNECTION STRING
# Uses Environment Variables for security (Standard for Senior Devs)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/job_db")

# 2. THE ENGINE
# The actual bridge between Python and Postgres
engine = create_engine(DATABASE_URL)

# 3. THE SESSION FACTORY
# 'autocommit=False' ensures we have control over when data is saved
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. THE DECLARATIVE BASE
# This is what your Job and Company classes will inherit from
Base = declarative_base()

# 5. DB DEPENDENCY (Crucial for FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()