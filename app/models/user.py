from app.extensions import db
from flask_login import UserMixin

# 1. THE ASSOCIATION TABLE (The Bridge)
# Ensure these strings 'user.id' and 'skill.id' match your __tablename__
user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'  # <--- MUST MATCH THE FOREIGN KEY ABOVE

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="seeker")

    # 2. THE RELATIONSHIP
    # This links the Skill model through the user_skills table
    skills = db.relationship('Skill', secondary=user_skills, backref=db.backref('users', lazy='dynamic'))