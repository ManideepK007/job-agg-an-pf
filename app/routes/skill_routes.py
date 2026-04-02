from flask import Blueprint, request, jsonify
from app.models.skill import Skill
from app import db

skill_bp = Blueprint("skills", __name__)

# GET all skills
@skill_bp.route("/skills", methods=["GET"])
def get_skills():
    skills = Skill.query.all()

    return jsonify([{"id": s.id, "name": s.name} for s in skills])


# CREATE skill
@skill_bp.route("/skills", methods=["POST"])
def create_skill():
    data = request.json

    skill = Skill(name=data["name"])

    db.session.add(skill)
    db.session.commit()

    return jsonify({"message": "Skill created"})