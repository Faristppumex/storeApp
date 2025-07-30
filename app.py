from flask import Flask
from flask_jwt_extended import JWTManager
from utils.db import get_db
from routes.orders import orders_bp
from routes.shipped import shipped_bp
from routes.auth import auth_bp
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Use a strong secret, or load from .env

jwt = JWTManager(app)

@app.route('/')
def home():
    return '''<div>
    <h1>Store App </h1>
    </div>'''

app.register_blueprint(orders_bp)
app.register_blueprint(shipped_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
