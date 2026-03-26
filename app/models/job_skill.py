from app import db

job_skills = db.Table(
    "job_skills",
    db.Column("job_id", db.Integer, db.ForeignKey("jobs.id")),
    db.Column("skill_id", db.Integer, db.ForeignKey("skills.id"))
)