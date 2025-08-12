from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
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
# @jwt_required()
def get_orders():
    """
    Get orders with pagination
    ---
    tags:
      - Orders
    parameters:
      - in: query
        name: page
        type: integer
        default: 1
        description: Page number
      - in: query
        name: per_page
        type: integer
        default: 10
        description: Items per page (max 100)
    responses:
      200:
        description: Paginated orders
        schema:
          type: object
          properties:
            orders:
              type: array
            pagination:
              type: object
              properties:
                page:
                  type: integer
                per_page:
                  type: integer
                total:
                  type: integer
                pages:
                  type: integer
                has_next:
                  type: boolean
                has_prev:
                  type: boolean
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)  # Max 100 items per page
    return get_orders_service(page, per_page)

@orders_bp.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def remove_order(order_id):
    return remove_order_service(order_id)

@orders_bp.route('/api/v1/delete_all', methods=['DELETE'])
@jwt_required()
def delete_all():
    identity = get_jwt_identity()
    if identity.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    return delete_all_orders_service()

@orders_bp.route('/api/v1/get_all', methods=['GET'])
@jwt_required()
def get_all():
    return get_all_service()

@orders_bp.route('/api/v1/ship_order', methods=['POST'])
@jwt_required()
def ship_order():
    identity = get_jwt_identity()
    if identity.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    return ship_order_service(request)