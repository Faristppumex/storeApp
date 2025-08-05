from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.product_services import (
    get_product_service,
    get_products_service
)

products_bp = Blueprint('products', __name__)

@products_bp.route('/api/v1/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_products(product_id):
    """
    Get a product by ID
    ---
    tags:
      - Products
    parameters:
      - in: path
        name: product_id
        type: integer
        required: true
        description: The ID of the product to retrieve
    responses:
      200:
        description: Product found
      404:
        description: Product not found
    """
    return get_product_service(product_id)

@products_bp.route('/api/v1/products', methods=['GET'])
@jwt_required()
def get_all_products():
    """
    Get all products
    ---
    tags:
      - Products
    responses:
      200:
        description: List of products
    """
    return get_products_service()