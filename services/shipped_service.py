from utils.db import get_db
from flask import jsonify

def get_shipped_service():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM shipped')
    orders = cur.fetchall()
    cur.close()
    conn.close()
    result = [
        {'order_id': order['id'], 'item': order['item'], 'quantity': order['quantity']}
        for order in orders
    ]
    return jsonify(result)
