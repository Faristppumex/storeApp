from flask import request, jsonify
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
import pandas as pd

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def create_upload_folder():
    """Create upload folder if it doesn't exist"""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if file is CSV"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

def get_csv_info(filepath):
    """Get CSV file information"""
    try:
        df = pd.read_csv(filepath)
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': df.columns.tolist(),
            'size_mb': round(os.path.getsize(filepath) / (1024 * 1024), 2),
            'preview': df.head(3).to_dict('records')  # First 3 rows
        }
    except Exception as e:
        return {'error': f'Could not read CSV: {str(e)}'}

def upload_csv_service():
    """Handle CSV file upload"""
    create_upload_folder()
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only CSV files are allowed'}), 400
    
    if request.content_length and request.content_length > MAX_FILE_SIZE:
        return jsonify({'error': f'File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB'}), 413
    
    try:
        original_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}.csv"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(filepath)
        
        csv_info = get_csv_info(filepath)
        
        response_data = {
            'success': True,
            'message': 'CSV file uploaded successfully',
            'file': {
                'id': unique_filename.replace('.csv', ''),
                'original_name': original_filename,
                'filename': unique_filename,
                'path': filepath,
                'url': f"/api/v1/files/{unique_filename}",
                'uploaded_at': datetime.now().isoformat(),
                'csv_info': csv_info
            }
        }
        
        print(f"✅ CSV uploaded: {original_filename} -> {unique_filename}")
        return jsonify(response_data), 201
        
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return jsonify({'success': False, 'error': f'Upload failed: {str(e)}'}), 500

def get_uploaded_csvs():
    """Get list of all uploaded CSV files"""
    create_upload_folder()
    
    try:
        files = []
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.endswith('.csv'):
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                csv_info = get_csv_info(filepath)
                
                files.append({
                    'id': filename.replace('.csv', ''),
                    'filename': filename,
                    'path': filepath,
                    'url': f"/api/v1/files/{filename}",
                    'uploaded_at': datetime.fromtimestamp(os.path.getctime(filepath)).isoformat(),
                    'csv_info': csv_info
                })
        
        files.sort(key=lambda x: x.get('uploaded_at', ''), reverse=True)
        
        return jsonify({
            'success': True,
            'csv_files': files,
            'total': len(files)
        }), 200
        
    except Exception as e:
        print(f"❌ Error listing CSV files: {e}")
        return jsonify({'success': False, 'error': f'Failed to list files: {str(e)}'}), 500

def delete_csv_service(filename):
    """Delete a CSV file"""
    try:
        if not filename.endswith('.csv'):
            filename += '.csv'
            
        filepath = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
        
        if not os.path.exists(filepath):
            return jsonify({'success': False, 'error': 'CSV file not found'}), 404
        
        os.remove(filepath)
        print(f"🗑️ CSV deleted: {filename}")
        
        return jsonify({
            'success': True,
            'message': 'CSV file deleted successfully',
            'filename': filename
        }), 200
        
    except Exception as e:
        print(f"❌ Delete error: {e}")
        return jsonify({'success': False, 'error': f'Delete failed: {str(e)}'}), 500