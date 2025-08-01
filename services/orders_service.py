from utils.db import get_db
from flask import request, jsonify

from tasks import send_email

def create_order_service(request):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO orders (item, quantity) VALUES (%s, %s) RETURNING id', (data['item'], data['quantity']))
    order_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'order_id': order_id, 'order': {'item': data['item'], 'quantity': data['quantity']}}), 201

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

def get_orders_service():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM orders')
    orders = cur.fetchall()
    cur.close()
    conn.close()
    result = [
        {'order_id': order['id'], 'item': order['item'], 'quantity': order['quantity']}
        for order in orders
    ]
    return jsonify(result)

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
