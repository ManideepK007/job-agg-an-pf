import os

class Config:
    SECRET_KEY = "secret"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost/jobdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONGO_URI = "mongodb://localhost:27017/jobs"