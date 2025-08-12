from utils.db import get_db
from flask import request, jsonify
import math

from flask_jwt_extended import get_jwt_identity

from tasks import send_email

def create_order_service(request):
    data = request.get_json()
    product_id = data.get('product_id')
    identity = get_jwt_identity()
    user_id = identity['id'] if isinstance(identity, dict) and 'id' in identity else identity
    if not product_id or not user_id:
        return jsonify({'error': 'product_id and user_id are required'}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM product WHERE id = %s', (product_id,))
    product = cur.fetchone()
    if not product:
        cur.close()
        conn.close()
        return jsonify({'error': 'Product not found'}), 404
    # Example: insert order with user_id, product_id, total_amount, payment_status, order_status, created_at
    total_amount = product['price']
    payment_status = 'pending'
    order_status = 'created'
    from datetime import datetime
    created_at = datetime.utcnow()
    cur.execute('INSERT INTO orders (user_id, total_amount, payment_status, order_status, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING id',
                (user_id, total_amount, payment_status, order_status, created_at))
    order_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'order_id': order_id, 'product': {'id': product['id'], 'name': product['name'], 'price': product['price']}}), 201

def get_order_service(order_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM orders WHERE id = %s', (order_id,))
    order = cur.fetchone()
    cur.close()
    conn.close()
    if order:
        return jsonify({'order_id': order['id'], 'order': {'item': order['item'], 'quantity': order['quantity']}})
    else:
        return jsonify({'error': 'Order not found'}), 404

def get_orders_service(page=1, per_page=10):
    # identity = get_jwt_identity()
    # user_id = identity['id'] if isinstance(identity, dict) and 'id' in identity else identity
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get total count for pagination
    cur.execute('SELECT COUNT(*) FROM orders WHERE user_id = %s', (user_id,))
    total = cur.fetchone()['count']
    
    # Calculate offset
    offset = (page - 1) * per_page
    
    # Get paginated orders
    cur.execute('''
        SELECT * FROM orders 
        WHERE user_id = %s 
        ORDER BY created_at DESC 
        LIMIT %s OFFSET %s
    ''', (user_id, per_page, offset))
    
    orders = cur.fetchall()
    print("orders: ", orders)
    print("offset ", offset)
    print("page ", page)
    cur.close()
    conn.close()
    
    # Calculate pagination info
    total_pages = math.ceil(total / per_page)
    has_next = page < total_pages
    has_prev = page > 1
    
    result = [
        {
            'id': order['id'],
            'user_id': order['user_id'],
            'total_amount': float(order['total_amount']),
            'payment_status': order['payment_status'],
            'order_status': order['order_status'],
            'created_at': order['created_at'].isoformat() if order['created_at'] else None
        }
        for order in orders
    ]
    
    return jsonify({
        'orders': result,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': total_pages,
            'has_next': has_next,
            'has_prev': has_prev
        }
    })


def remove_order_service(order_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM orders WHERE id = %s', (order_id,))
    order = cur.fetchone()
    if order:
        cur.execute('DELETE FROM orders WHERE id = %s', (order_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': f'Order {order_id} deleted'})
    else:
        cur.close()
        conn.close()
        return jsonify({'error': 'Order not found'}), 404

def delete_all_orders_service():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM orders')
    cur.execute('DELETE FROM shipped')
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'All entries deleted from orders and shipped tables.'}), 200

def get_all_service():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM orders')
    orders = cur.fetchall()
    cur.execute('SELECT * FROM shipped')
    shipped = cur.fetchall()
    cur.close()
    conn.close()
    orders_result = [
        {'order_id': order['id'], 'item': order['item'], 'quantity': order['quantity']}
        for order in orders
    ]
    shipped_result = [
        {'order_id': ship['id'], 'item': ship['item'], 'quantity': ship['quantity']}
        for ship in shipped
    ]
    return jsonify({'orders': orders_result, 'shipped': shipped_result})

def ship_order_service(request):
    data = request.get_json()
    order_id = data.get('order_id')
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM orders WHERE id = %s', (order_id,))
    order = cur.fetchone()
    if not order:
        cur.close()
        conn.close()
        return jsonify({'error': 'Order not found'}), 404
    cur.execute('INSERT INTO shipped (id, item, quantity) VALUES (%s, %s, %s)', (order['id'], order['item'], order['quantity']))
    cur.execute('DELETE FROM orders WHERE id = %s', (order_id,))
    conn.commit()
    cur.close()
    conn.close()
    send_email.delay(order_id)
    
    return jsonify({'message': f'Order {order_id} shipped.'}), 200
