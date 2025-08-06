from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.db import get_db
auth_bp = Blueprint('auth', __name__)
from tasks import send_email

@auth_bp.route('/api/v1/signup', methods=['POST'])
def signup():
    email = request.json.get('email')
    password_hash = request.json.get('password_hash')
    name = request.json.get('name')
    role = request.json.get('role', 'customer')
    if not email or not password_hash or not name:
        return jsonify({'msg': 'Email, password, and name required'}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cur.fetchone()
    if user:
        cur.close()
        conn.close()
        return jsonify({'msg': 'Email already exists'}), 409
    cur.execute('INSERT INTO users (email, password_hash, name, role) VALUES (%s, %s, %s, %s)', (email, password_hash, name, role))
    conn.commit()
    cur.close()
    conn.close()
    send_email({
        'email': email,
        'subject': 'Welcome to Store App',
        'body': f'Hello {name}, welcome to Store App!'
    })
    
    return jsonify({'msg': 'User created successfully'}), 201

@auth_bp.route('/api/v1/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password_hash = request.json.get('password_hash')
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user and user['password_hash'] == password_hash:
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad cred"}), 401

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200