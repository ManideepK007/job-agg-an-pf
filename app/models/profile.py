from app.extensions import db

class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    bio = db.Column(db.Text)
    # This stores skills as a list like ["Python", "Flask"]
    skills = db.Column(db.JSON, default=list) 
    experience_years = db.Column(db.Integer, default=0)
    resume_path = db.Column(db.String(255)) 

    def __repr__(self):
        return f'<Profile {self.full_name}>'