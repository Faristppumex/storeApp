from flask import Blueprint, send_from_directory
from flask_jwt_extended import jwt_required
from services.upload_services import upload_csv_service, get_uploaded_csvs, delete_csv_service

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/api/v1/upload/csv', methods=['POST'])
@jwt_required()
def upload_csv():
    """
    Upload a CSV file
    ---
    tags:
      - CSV Upload
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: file
        type: file
        required: true
        description: CSV file to upload
    responses:
      201:
        description: CSV uploaded successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            file:
              type: object
      400:
        description: Bad request
    """
    return upload_csv_service()

@upload_bp.route('/api/v1/csv/files', methods=['GET'])
@jwt_required()
def list_csv_files():
    """
    Get list of uploaded CSV files
    ---
    tags:
      - CSV Upload
    responses:
      200:
        description: List of CSV files with metadata
    """
    return get_uploaded_csvs()

@upload_bp.route('/api/v1/files/<filename>', methods=['GET'])
def download_csv(filename):
    """
    Download a CSV file
    ---
    tags:
      - CSV Upload
    parameters:
      - in: path
        name: filename
        type: string
        required: true
    responses:
      200:
        description: CSV file content
      404:
        description: File not found
    """
    try:
        return send_from_directory('uploads', filename)
    except FileNotFoundError:
        return jsonify({'success': False, 'error': 'CSV file not found'}), 404

@upload_bp.route('/api/v1/csv/<filename>', methods=['DELETE'])
@jwt_required()
def delete_csv(filename):
    """
    Delete a CSV file
    ---
    tags:
      - CSV Upload
    parameters:
      - in: path
        name: filename
        type: string
        required: true
    responses:
      200:
        description: CSV deleted successfully
      404:
        description: File not found
    """
    return delete_csv_service(filename)