from flask import Blueprint, jsonify
from services.shipped_service import get_shipped_service

shipped_bp = Blueprint('shipped', __name__)

@shipped_bp.route('/api/v1/shipped', methods=['GET'])
def get_shipped():
    return get_shipped_service()
