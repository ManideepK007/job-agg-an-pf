from app import db
from app.models.job import job_skills # ✅ This is correct now!

class Skill(db.Model):
    __tablename__ = "skill"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Skill {self.name}>"