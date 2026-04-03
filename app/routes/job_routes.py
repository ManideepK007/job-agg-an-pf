from flask import Blueprint, request, jsonify, render_template
from app.models.job import Job
from app.models.skill import Skill
from app.models.user import User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

job_bp = Blueprint("jobs", __name__)

# ==============================
# 🧠 ADVANCED: MATCHING ALGORITHM
# ==============================

def calculate_match_score(user_skills, job_skills):
    """
    Calculates the percentage match between user and job skills.
    Uses Set Intersection (O(n) complexity).
    """
    if not job_skills:
        return 0
    
    # Extract IDs to compare sets
    user_skill_ids = {s.id for s in user_skills}
    job_skill_ids = {s.id for s in job_skills}
    
    # Logic: How many required skills does the user actually have?
    matched_skills = user_skill_ids.intersection(job_skill_ids)
    
    score = (len(matched_skills) / len(job_skill_ids)) * 100
    return round(score, 1)

# ==============================
# 🔍 SEARCH & RECOMMENDATION ROUTES
# ==============================

@job_bp.route("/api/jobs/recommendations", methods=["GET"])
@jwt_required()
def get_recommendations():
    """
    ADVANCED FEATURE: Returns jobs sorted by how well they match 
    the logged-in user's profile.
    """
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    all_jobs = Job.query.all()
    recommendations = []

    for job in all_jobs:
        score = calculate_match_score(user.skills, job.skills)
        
        # We only suggest jobs that have at least a 10% match
        if score > 10:
            job_data = job.to_dict()
            job_data['match_score'] = f"{score}%"
            # Insight: Tell the user exactly what skills they are missing
            job_data['missing_skills'] = [s.name for s in job.skills if s not in user.skills]
            recommendations.append(job_data)

    # Sort by highest match score first
    recommendations.sort(key=lambda x: float(x['match_score'].strip('%')), reverse=True)
    
    return jsonify(recommendations), 200

@job_bp.route("/jobs", methods=["GET"])
def view_jobs_ui():
    location = request.args.get("location")
    skill = request.args.get("skill")

    query = Job.query
    
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    
    if skill:
        query = query.join(Job.skills).filter(Skill.name.ilike(f"%{skill}%"))

    jobs = query.order_by(Job.created_at.desc()).all()

    # UI Enhancement: If user is logged in via browser, we could calculate scores here too
    if "text/html" in request.headers.get("Accept", ""):
        return render_template("jobs.html", jobs=jobs)
    
    return jsonify([j.to_dict() for j in jobs]), 200

# ==============================
# 🛠️ DATABASE & ADMIN ACTIONS
# ==============================

@job_bp.route("/init-db", methods=["GET"])
def init_db():
    try:
        # Import all models here to ensure they are registered with SQLAlchemy
        from app.models.company import Company
        from app.models.user import User 
        db.create_all()
        return jsonify({"message": "Database tables created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@job_bp.route("/api/jobs", methods=["POST"])
@jwt_required()
def create_job():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ("title", "location", "company_id")):
            return jsonify({"error": "Missing required fields"}), 400

        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)

        if not user or user.role != "admin":
            return jsonify({"error": "Unauthorized: Admin access required"}), 403

        from app.models.company import Company
        company = db.session.get(Company, data["company_id"])
        if not company:
            return jsonify({"error": "Invalid company ID"}), 400

        job = Job(
            title=data["title"],
            location=data["location"],
            salary=data.get("salary"),
            company_id=data["company_id"]
        )

        # ADVANCED: Add skills to job during creation
        if "skill_ids" in data:
            skills = Skill.query.filter(Skill.id.in_(data["skill_ids"])).all()
            job.skills.extend(skills)

        db.session.add(job)
        db.session.commit()

        return jsonify({"message": "Job created with skills", "job": job.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500