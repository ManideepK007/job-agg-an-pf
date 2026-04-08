from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models.job import Job
from app.models.application import Application
from app.models.skill import Skill 
from app.extensions import db

job_bp = Blueprint('job_bp', __name__)

@job_bp.route('/')
@job_bp.route('/jobs')
def explore():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '').strip()
    city_filter = request.args.get('city', '').strip()
    skill_filter = request.args.get('skill', '').strip() 
    company_filter = request.args.get('company', '').strip()
    # 1. Base Query
    query = db.session.query(Job)

    # 2. Text Search (Title/Description)
    if search_query:
        query = query.filter(
            (Job.title.ilike(f'%{search_query}%')) | 
            (Job.description.ilike(f'%{search_query}%'))
        )
    
    # 3. Location Filter
    if city_filter:
        query = query.filter(Job.location.ilike(f'%{city_filter}%'))

    if company_filter:
        query = query.filter(Job.company_name.ilike(f'%{company_filter}%'))
    
    # 4. SKILL FILTER (Join many-to-many relationship)
    if skill_filter:
        query = query.join(Job.skills).filter(Skill.name.ilike(f'%{skill_filter}%'))

    # 5. FINAL PAGINATION (The Fix)
    # We use .group_by(Job.id) to prevent duplicates from the join.
    # We REMOVE .distinct() because PostgreSQL cannot compare JSON columns.
    pagination = (
        query.group_by(Job.id)
        .order_by(Job.posted_at.desc())
        .paginate(page=page, per_page=10)
    )
    
    return render_template(
        'explore.html', 
        jobs=pagination.items, 
        pagination=pagination,
        search_query=search_query,
        skill_filter=skill_filter,
        company_filter=company_filter # Added company filter to template context
    )

@job_bp.route('/job/<int:job_id>')
def job_detail(job_id):
    job = db.session.get(Job, job_id)
    if not job:
        return render_template('404.html'), 404

    has_applied = False
    if current_user.is_authenticated:
        # Optimization: use exists() for a faster check than .first()
        has_applied = db.session.query(
            db.exists().where(Application.job_id == job.id, Application.user_id == current_user.id)
        ).scalar()
        
    return render_template('job_detail.html', job=job, has_applied=has_applied)

@job_bp.route("/post-job", methods=["GET", "POST"])
@login_required
def post_job():
    if request.method == "POST":
        new_job = Job(
            title=request.form.get("title"),
            company_name=request.form.get("company_name"),
            location=request.form.get("location"),
            salary=request.form.get("salary"),
            description=request.form.get("description")
        )

        skills_input = request.form.get("skills_required", "")
        if skills_input:
            skill_names = [s.strip() for s in skills_input.split(",") if s.strip()]
            for name in skill_names:
                # Optimized: Look up or create skill
                skill = db.session.query(Skill).filter_by(name=name).first()
                if not skill:
                    skill = Skill(name=name)
                    db.session.add(skill)
                new_job.skills.append(skill)

        db.session.add(new_job)
        db.session.commit()
        flash("Job posted successfully!", "success")
        return redirect(url_for('job_bp.explore'))

    return render_template("post_job.html")

@job_bp.route('/apply/quick/<int:job_id>', methods=['POST'])
@login_required
def quick_apply(job_id):
    if current_user.role != 'seeker':
        flash("Only job seekers can apply.", "danger")
        return redirect(url_for('job_bp.explore'))

    existing_app = db.session.query(Application).filter_by(
        job_id=job_id, 
        user_id=current_user.id
    ).first()
    
    if existing_app:
        flash("Already applied!", "info")
        return redirect(url_for('job_bp.explore'))

    try:
        new_app = Application(job_id=job_id, user_id=current_user.id)
        db.session.add(new_app)
        db.session.commit()
        flash("Application submitted!", "success")
    except Exception:
        db.session.rollback()
        flash("Error submitting application.", "danger")
    
    return redirect(url_for('job_bp.explore'))
@job_bp.route('/jobs')
def list_jobs():
    # Get search parameters from the URL
    q = request.args.get('q', '')
    location = request.args.get('location', '')
    
    query = Job.query
    
    # Filter logic
    if q:
        query = query.filter(Job.title.ilike(f'%{q}%'))
    if location and location != 'All India':
        query = query.filter(Job.location.ilike(f'%{location}%'))
        
    jobs = query.order_by(Job.posted_date.desc()).all()
    return render_template('explore.html', jobs=jobs)