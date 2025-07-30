from flask import Flask
from utils.db import get_db
from routes.orders import orders_bp
from routes.shipped import shipped_bp

app = Flask(__name__)

@app.route('/')
def home():
    return '''<div>
    <h1>Store App </h1>
    </div>'''

app.register_blueprint(orders_bp)
app.register_blueprint(shipped_bp)

if __name__ == '__main__':
    app.run(debug=True)
