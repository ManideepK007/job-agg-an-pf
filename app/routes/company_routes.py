from flask import Blueprint, request, jsonify
from app.models.company import Company
from app import db

company_bp = Blueprint("companies", __name__)

# GET all companies
@company_bp.route("/companies", methods=["GET"])
def get_companies():
    companies = Company.query.all()

    result = []
    for c in companies:
        result.append({
            "id": c.id,
            "name": c.name,
            "location": c.location
        })

    return jsonify(result)


# CREATE company
@company_bp.route("/companies", methods=["POST"])
def create_company():
    data = request.json

    company = Company(
        name=data["name"],
        location=data["location"]
    )

    db.session.add(company)
    db.session.commit()

    return jsonify({"message": "Company created"})