from flask import Blueprint, request, jsonify, render_template
from app.models.job import Job, job_skills  # ✅ FIX: Import job_skills from Job model
from app.models.skill import Skill
from app.models.user import User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

job_bp = Blueprint("jobs", __name__)

# ==============================
# 🛠️ DATABASE & SETUP
# ==============================

@job_bp.route("/init-db", methods=["GET"])
def init_db():
    try:
        from app.models.company import Company
        # ✅ FIX: Removed the 'from app.models.job_skill' import entirely
        db.create_all()
        return jsonify({"message": "Database tables created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==============================
# 🔍 SEARCH & VIEW ROUTES
# ==============================

@job_bp.route("/jobs", methods=["GET"])
def view_jobs_ui():
    location = request.args.get("location")
    skill = request.args.get("skill")

    query = Job.query
    
    if location:
        # ilike handles 'Hyderabad' vs 'hyderabad'
        query = query.filter(Job.location.ilike(f"%{location}%"))
    
    if skill:
        # Joining the skills table to search by skill name
        query = query.join(Job.skills).filter(Skill.name.ilike(f"%{skill}%"))

    jobs = query.order_by(Job.created_at.desc()).all()

    # Detect if request is from a browser or a tool like Postman
    if "text/html" in request.headers.get("Accept", ""):
        return render_template("jobs.html", jobs=jobs)
    
    return jsonify([j.to_dict() for j in jobs]), 200

@job_bp.route("/api/jobs", methods=["GET"])
def get_jobs_api():
    return view_jobs_ui() 

# ==============================
# 🔐 ADMIN ACTIONS
# ==============================

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

        # Handling skills during job creation (Optional Improvement)
        job = Job(
            title=data["title"],
            location=data["location"],
            salary=data.get("salary"),
            company_id=data["company_id"]
        )

        db.session.add(job)
        db.session.commit()

        return jsonify({"message": "Job created", "job": job.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500