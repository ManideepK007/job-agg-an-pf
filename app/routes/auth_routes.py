from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db
from flask_jwt_extended import create_access_token
import bcrypt

auth_bp = Blueprint("auth", __name__)


# 🔐 REGISTER
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # ✅ Handle empty body
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")   # 🔥 role support

    # ✅ validation
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    # ✅ check existing user
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    # 🔥 HASH PASSWORD
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # ✅ create user
    user = User(
        username=username,
        password=hashed_password,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }), 201


# 🔐 LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # ✅ Handle empty body
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "Invalid username"}), 401

    # 🔥 CHECK HASHED PASSWORD
    if not bcrypt.checkpw(
        password.encode("utf-8"),
        user.password.encode("utf-8")
    ):
        return jsonify({"error": "Invalid password"}), 401

    # 🔑 generate token
    token = create_access_token(identity=str(user.id))

    return jsonify({
        "access_token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }), 200