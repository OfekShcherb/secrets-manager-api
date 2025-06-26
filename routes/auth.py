from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies
from utils.db import get_user_by_username, insert_user
from utils.crypto import generate_key, create_hash, check_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"msg": "Missing fields"}), 400

    username = data['username']
    password = data['password']
    if get_user_by_username(username):
        return jsonify({"msg": "User already exists"}), 400
    
    key = generate_key()
    hashed_password = create_hash(password)
    insert_user(username, hashed_password, key)
    return jsonify({"msg": "User registered"}), 201
    

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"msg": "Missing fields"}), 400
    
    username = data['username']
    password = data['password']
    user = get_user_by_username(username)
    if user and check_hash(password, user[1]):
        token = create_access_token(identity=username)
        response = jsonify({"msg": "Login successful"})
        set_access_cookies(response, token)
        return response
        
    return jsonify({"msg": "Invalid credientials"}), 401