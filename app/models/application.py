from app.extensions import db
from datetime import datetime
from app.database import Base
from app.extensions import db
class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)

    # These relationships allow you to access data easily
    # e.g., my_app.job.title or my_app.user.email
    job = db.relationship('Job', backref=db.backref('job_applications', lazy=True))
    user = db.relationship('User', backref=db.backref('user_applications', lazy=True))

    def __repr__(self):
        return f'<Application Job {self.job_id} by User {self.user_id}>'