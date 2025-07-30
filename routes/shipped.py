from flask import Blueprint, jsonify
from services.shipped_service import get_shipped_service
from flask_jwt_extended import jwt_required

shipped_bp = Blueprint('shipped', __name__)

@shipped_bp.route('/api/v1/shipped', methods=['GET'])
@jwt_required()
def get_shipped():
    return get_shipped_service()
