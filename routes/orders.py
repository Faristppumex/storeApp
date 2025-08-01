from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
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
@jwt_required()
def create_order():
    """
    Create a new order
    ---
    tags:
      - Orders
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - item
            - quantity
          properties:
            item:
              type: string
            quantity:
              type: integer
    responses:
      201:
        description: Order created
      400:
        description: Invalid input
    """
    return create_order_service(request)

@orders_bp.route('/api/v1/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    return get_order_service(order_id)

@orders_bp.route('/api/v1/orders', methods=['GET'])
@jwt_required()
def get_orders():
    return get_orders_service()

@orders_bp.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def remove_order(order_id):
    return remove_order_service(order_id)

@orders_bp.route('/api/v1/delete_all', methods=['DELETE'])
@jwt_required()
def delete_all():
    return delete_all_orders_service()

@orders_bp.route('/api/v1/get_all', methods=['GET'])
@jwt_required()
def get_all():
    return get_all_service()

@orders_bp.route('/api/v1/ship_order', methods=['POST'])
@jwt_required()
def ship_order():
    return ship_order_service(request)