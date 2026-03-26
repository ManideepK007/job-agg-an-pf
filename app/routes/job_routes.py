from flask import Blueprint, request, jsonify
from app.models.job import Job
from app.models.skill import Skill
from app.models.user import User   # ✅ correct import
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

job_bp = Blueprint("jobs", __name__)

@job_bp.route("/", methods=["GET"])
def home():
    return "Server is running"

# 🔍 GET JOBS (PUBLIC)
@job_bp.route("/jobs", methods=["GET"])
def get_jobs():
    location = request.args.get("location")
    skill = request.args.get("skill")

    query = Job.query

    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))

    if skill:
        query = query.join(Job.skills).filter(Skill.name.ilike(f"%{skill}%"))

    jobs = query.all()

    result = []
    for j in jobs:
        result.append({
            "id": j.id,
            "title": j.title,
            "location": j.location,
            "skills": [s.name for s in j.skills]
        })

    return jsonify(result)


# 🔐 CREATE JOB (ADMIN ONLY)
@job_bp.route("/jobs", methods=["POST"])
@jwt_required()
def create_job():
    data = request.get_json()

    # 🔥 VALIDATION
    if not data:
        return jsonify({"error": "Request body required"}), 400

    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    if not data.get("location"):
        return jsonify({"error": "Location is required"}), 400

    if not data.get("company_id"):
        return jsonify({"error": "Company ID is required"}), 400

    # 🔥 GET CURRENT USER
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    # 🔥 ROLE CHECK (CORRECT PLACE)
    if user.role != "admin":
        return jsonify({"error": "Only admin can create jobs"}), 403

    # 🔥 CHECK COMPANY EXISTS
    from app.models.company import Company
    company = Company.query.get(data["company_id"])

    if not company:
        return jsonify({"error": "Invalid company ID"}), 400

    # ✅ CREATE JOB
    job = Job(
        title=data["title"],
        location=data["location"],
        salary=data.get("salary"),
        company_id=data["company_id"]
    )

    db.session.add(job)
    db.session.commit()

    return jsonify({
        "id": job.id,
        "title": job.title,
        "location": job.location
    }), 201