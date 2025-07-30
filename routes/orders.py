from flask import Blueprint, request, jsonify
from services.orders_service import (
    create_order_service,
    get_order_service,
    get_orders_service,
    remove_order_service,
    delete_all_orders_service,
    get_all_service,
    ship_order_service
)

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/api/v1/orders', methods=['POST'])
def create_order():
    return create_order_service(request)

@orders_bp.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    return get_order_service(order_id)

@orders_bp.route('/api/v1/orders', methods=['GET'])
def get_orders():
    return get_orders_service()

@orders_bp.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
def remove_order(order_id):
    return remove_order_service(order_id)

@orders_bp.route('/api/v1/delete_all', methods=['DELETE'])
def delete_all():
    return delete_all_orders_service()

@orders_bp.route('/api/v1/get_all', methods=['GET'])
def get_all():
    return get_all_service()

@orders_bp.route('/api/v1/ship_order', methods=['POST'])
def ship_order():
    return ship_order_service(request)
