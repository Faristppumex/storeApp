from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, decode_token
from flask_socketio import SocketIO, emit
from routes.orders import orders_bp
from routes.shipped import shipped_bp
from routes.auth import auth_bp
from routes.product import products_bp
from routes.chat import chat_bp
from routes.upload import upload_bp
from services.chat_services import format_message, log_message, validate_message, sanitize_username
import os
from flasgger import Swagger
from migrations.create_tables import run_migration

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
app.config['SECRET_KEY'] = 'your-socket-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

swagger = Swagger(app)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store connected users
connected_users = {}

# Run migrations on startup
with app.app_context():
    run_migration()

@app.route('/')
def home():
    return '''<div>
    <h1>🏪 Store App with WebSocket Chat & CSV Upload</h1>
    <p><a href="/chat" style="font-size: 18px; color: #007bff;">🤖 Chat with StoreBot</a></p>
    <p><a href="/apidocs" style="font-size: 16px; color: #28a745;">📚 API Documentation</a></p>
    <br>
    <h3>📋 Available API Endpoints:</h3>
    <ul style="font-family: monospace;">
        <li><strong>POST</strong> /api/v1/upload/csv - Upload CSV file</li>
        <li><strong>GET</strong> /api/v1/csv/files - List uploaded CSVs</li>
        <li><strong>GET</strong> /api/v1/files/&lt;filename&gt; - Download CSV</li>
        <li><strong>DELETE</strong> /api/v1/csv/&lt;filename&gt; - Delete CSV</li>
        <li><strong>POST</strong> /api/v1/auth/register - Register user</li>
        <li><strong>POST</strong> /api/v1/auth/login - Login user</li>
        <li><strong>GET</strong> /api/v1/products - Get products</li>
        <li><strong>GET</strong> /api/v1/orders - Get orders (with pagination)</li>
    </ul>
    </div>'''

# WebSocket Events for ChatBot
@socketio.on('connect')
def handle_connect():
    print(f'✅ Client connected: {request.sid}')
    emit('message', format_message('StoreBot', 'Hello! I\'m StoreBot 🤖. I can help you with products, orders, and store information. What can I help you with today?'))

@socketio.on('disconnect')
def handle_disconnect():
    print(f'❌ Client disconnected: {request.sid}')
    
    if request.sid in connected_users:
        username = connected_users[request.sid]
        del connected_users[request.sid]
        print(f'👋 User {username} left the chat')

@socketio.on('set_username')
def handle_set_username(data):
    username = sanitize_username(data.get('username', ''))
    connected_users[request.sid] = username
    
    print(f'👤 User {username} set their name (Session: {request.sid})')
    log_message('System', f'{username} joined the chat')
    
    # Welcome message from bot
    emit('message', format_message('StoreBot', f'Nice to meet you, {username}! 👋 How can I assist you today?'))

@socketio.on('send_message')
def handle_send_message(data):
    print(f"🔍 Received data: {data}")
    
    if not validate_message(data):
        print(f'❌ Invalid message data from {request.sid}')
        emit('message', format_message('StoreBot', 'Sorry, I didn\'t understand that. Could you try again?'))
        return
    
    username = sanitize_username(data['username'])
    user_message = data['message'].strip()
    
    # Log the user message
    log_message(username, user_message)
    
    # Echo user message
    emit('message', format_message(username, user_message))
    
    # Get bot response
    
    # Send bot response after a short delay
    import time

@socketio.on('error')
def handle_error(error):
    print(f'🚨 WebSocket error: {error}')

# Error handlers
@app.errorhandler(413)
def too_large(e):
    return jsonify({'success': False, 'error': 'File too large'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

# Register blueprints
app.register_blueprint(orders_bp)
app.register_blueprint(shipped_bp)
app.register_blueprint(products_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(upload_bp)  # Add upload blueprint

if __name__ == '__main__':
    print("🚀 Starting Flask-SocketIO server with CSV Upload...")
    print("🤖 ChatBot available at: http://localhost:5000/chat")
    print("📊 CSV Upload API available at: POST /api/v1/upload/csv")
    print("📚 API docs available at: http://localhost:5000/apidocs")
    print("📁 Uploads will be stored in: ./uploads/")
    
    # Create uploads folder on startup
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        print("✅ Created uploads folder")
    
    socketio.run(
        app, 
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 5000)), 
        debug=True
    )
