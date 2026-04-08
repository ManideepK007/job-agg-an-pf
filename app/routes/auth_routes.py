from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.extensions import db
from app.models import User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

# ✅ FIX: Import db from extensions and models from their individual files
from app.extensions import db
from app.models.user import User
from app.models.profile import Profile

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role') # 'seeker' or 'recruiter'

        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!')
            return redirect(url_for('auth.register'))

        # Create new user with hashed password (Security First!)
        # Note: Changed method to 'scrypt' as 'sha256' is deprecated in newer Werkzeug versions
        new_user = User(
            email=email, 
            password=set_password(password),
            role=role
        )
        db.session.add(new_user)
        db.session.commit()

        # Create a blank profile automatically for Job Seekers
        if role == 'seeker':
            new_profile = Profile(user_id=new_user.id)
            db.session.add(new_profile)
            db.session.commit()

        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth_bp.login'))

        login_user(user)
        
        # Redirect based on ROLE (Precision Routing)
        if user.role == 'recruiter':
            # Ensure you have a 'recruiter' blueprint and a 'dashboard' route!
            return redirect(url_for('recruiter.dashboard'))
        
        # For job seekers, they go to the explore page
        return redirect(url_for('job_bp.explore') if 'job_bp' in str(url_for) else '/')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))