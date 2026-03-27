from flask import Blueprint, request, jsonify
from app.models.job import Job
from app.models.skill import Skill
from app.models.user import User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

job_bp = Blueprint("jobs", __name__)


# ✅ ROOT (health check)
@job_bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running"}), 200


# ⚠️ TEMP ROUTE (REMOVE AFTER USE)
@job_bp.route("/init-db", methods=["GET"])
def init_db():
    
    try:
        db.create_all()
        return jsonify({"message": "DB created"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔍 GET JOBS (SAFE VERSION)
@job_bp.route("/jobs", methods=["GET"])
def get_jobs():
    try:
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

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔐 CREATE JOB (ADMIN ONLY)
@job_bp.route("/jobs", methods=["POST"])
@jwt_required()
def create_job():
    try:
        data = request.get_json()
        print("DEBUG DATA:", data)

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

        if not user:
            return jsonify({"error": "User not found"}), 404

        # 🔥 ROLE CHECK
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
            "message": "Job created",
            "job": {
                "id": job.id,
                "title": job.title,
                "location": job.location
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500