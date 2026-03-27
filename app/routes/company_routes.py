from flask import Blueprint, request, jsonify
from app.models.company import Company
from app import db

company_bp = Blueprint("companies", __name__)


# 🔍 GET ALL COMPANIES
@company_bp.route("/companies", methods=["GET"])
def get_companies():
    try:
        companies = Company.query.all()

        result = []
        for c in companies:
            result.append({
                "id": c.id,
                "name": c.name,
                "location": c.location,
                "website": getattr(c, "website", None),
                "email": getattr(c, "email", None)
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ➕ CREATE COMPANY
@company_bp.route("/companies", methods=["POST"])
def create_company():
    try:
        data = request.get_json()

        # 🔥 VALIDATION
        if not data:
            return jsonify({"error": "Request body required"}), 400

        if not data.get("name"):
            return jsonify({"error": "Company name is required"}), 400

        # 🔥 OPTIONAL DUPLICATE CHECK
        existing = Company.query.filter_by(name=data["name"]).first()
        if existing:
            return jsonify({"error": "Company already exists"}), 400

        # ✅ CREATE COMPANY
        company = Company(
            name=data["name"],
            location=data.get("location"),
            website=data.get("website"),
            email=data.get("email")
        )

        db.session.add(company)
        db.session.commit()

        return jsonify({
            "message": "Company created",
            "company": {
                "id": company.id,
                "name": company.name,
                "location": company.location
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500