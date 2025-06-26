from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.db import get_active_key, insert_secret, get_secret_record, get_key_by_id, delete_secret_by_name, update_secret_encryption, rotate_user_key
from utils.crypto import generate_key, encrypt_secret, decrypt_secret

secrets_bp = Blueprint('secrets', __name__)

@secrets_bp.route('/secrets', methods=['POST'])
@jwt_required()
def create_secret():
    current_user = get_jwt_identity()
    data = request.get_json()
    if not data or "name" not in data or "secret" not in data:
        return jsonify({"msg": "Missing fields"}), 400
    
    name = data['name']
    secret = data['secret']
    key_id, key = get_active_key(current_user)
    encrypted_secret = encrypt_secret(secret, key)

    if not insert_secret(current_user, name, encrypted_secret, key_id):
        return jsonify({"msg": "Secret name already exists"}), 400
    
    return jsonify({"msg": "Secret stored"}), 201
    
@secrets_bp.route('/secrets/<name>', methods=['GET'])
@jwt_required()
def get_secret(name):
    current_user = get_jwt_identity()
    record = get_secret_record(current_user, name)
    if not record:
        return jsonify({"msg": "Secret not found"}), 404

    encrypted_secret, key_id = record
    key = get_key_by_id(key_id)
    if not key:
        return jsonify({"msg": "Encryption key not found"}), 500
    
    decrypted_secret = decrypt_secret(encrypted_secret, key)

    active_key_id, active_key = get_active_key(current_user)
    if active_key_id and key_id != active_key_id:
        new_encrypted_secret = encrypt_secret(decrypted_secret, active_key)
        update_secret_encryption(current_user, name, new_encrypted_secret, active_key_id)

    return jsonify({"secret": decrypted_secret}), 200
    
@secrets_bp.route('/secrets/<name>', methods=['DELETE'])
@jwt_required()
def delete_secret(name):
    current_user = get_jwt_identity()
    if not get_secret_record(current_user, name):
        return jsonify({"msg": "Secret not found"}), 404
    
    delete_secret_by_name(current_user, name)
    return jsonify({"msg": "Secret deleted"})

@secrets_bp.route('/secrets/<name>', methods=['PATCH'])
@jwt_required()
def patch_secret(name):
    current_user = get_jwt_identity()
    if not get_secret_record(current_user, name):
        return jsonify({"msg": "Secret not found"}), 404
    
    data = request.get_json()
    if not data or "secret" not in data:
        return jsonify({"msg": "Missing fields"}), 400
    
    new_secret = data['secret']
    key_id, key = get_active_key(current_user)
    if not key:
        return jsonify({"msg": "Encryption key not found"}), 500
    
    new_encrypted_secret = encrypt_secret(new_secret, key)
    update_secret_encryption(current_user, name, new_encrypted_secret, key_id)
    
    return jsonify({"msg": "Secret updated"}), 200


@secrets_bp.route('/rotate-key', methods=['POST'])
@jwt_required()
def rotate_key():
    current_user = get_jwt_identity()
    new_key = generate_key()
    rotate_user_key(current_user, new_key)

    return jsonify({"msg": "Key rotated successfully"})