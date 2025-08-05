from utils.db import get_db
from flask import jsonify, request


def get_product_service(product_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products WHERE id = %s', (product_id,))
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
    cur.execute('SELECT * FROM products')
    products = cur.fetchall()
    cur.close()
    conn.close()
    result = [
        {'id': product['id'], 'name': product['name'], 'price': product['price']}
        for product in products
    ]
    return jsonify(result)