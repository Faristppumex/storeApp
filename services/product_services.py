from utils.db import get_db
from flask import jsonify, request


def get_product_service(product_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM product WHERE id = %s', (product_id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    if product:
        return jsonify({'product': {'id': product['id'], 'name': product['name'], 'price': product['price']}})
    else:
        return jsonify({'error': 'Product not found'}), 404
    
def get_products_service():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM product')
    products = cur.fetchall()
    cur.close()
    conn.close()
    result = [
        {'id': product['id'], 'name': product['name'], 'price': product['price']}
        for product in products
    ]
    return jsonify(result)

def create_product_service(request):
    data = request.get_json()
    product_id = data.get('id')
    name = data.get('name')
    price = data.get('price')
    if not product_id or not name or not price:
        return jsonify({'error': 'id, name, and price are required'}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO product (id, name, price) VALUES (%s, %s, %s)', (product_id, name, price))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Product created successfully', 'product': {'id': product_id, 'name': name, 'price': price}}), 201