from app import db

# ✅ ADVANCED: Association table for User-Skill relationship
user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id', ondelete="CASCADE"), primary_key=True)
)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")

    # ✅ ADVANCED: Relationship to fetch user's skills
    skills = db.relationship('Skill', secondary=user_skills, backref=db.backref('users', lazy='dynamic'))

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "skills": [skill.name for skill in self.skills]
        }