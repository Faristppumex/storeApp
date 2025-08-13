import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_db


def seed_products():
    """Populate products table with sample data"""
    conn = get_db()
    cur = conn.cursor()
    
    products = [
        ("Laptop", "High-performance laptop for work and gaming", 999.99, 10),
        ("Smartphone", "Latest model smartphone with advanced features", 699.99, 25),
        ("Headphones", "Wireless noise-canceling headphones", 199.99, 50),
        ("Coffee Maker", "Automatic drip coffee maker", 89.99, 15),
        ("Desk Chair", "Ergonomic office chair", 299.99, 8),
        ("Monitor", "27-inch 4K display monitor", 399.99, 12),
        ("Keyboard", "Mechanical gaming keyboard", 129.99, 30),
        ("Mouse", "Wireless optical mouse", 49.99, 45),
        ("Tablet", "10-inch tablet for productivity", 449.99, 20),
        ("Webcam", "HD webcam for video calls", 79.99, 35)
    ]
    
    for name, description, price, stock in products:
        cur.execute('''
            INSERT INTO product (name, description, price, stock) 
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        ''', (name, description, price, stock))
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"✓ Seeded {len(products)} products")


def create_users_table():
    """Create users table"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                role VARCHAR(50) DEFAULT 'customer',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    conn.commit()
    cur.close()
    conn.close()
    print("✓ Users table created")

def create_product_table():
    """Create product table"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
            CREATE TABLE IF NOT EXISTS product (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10,2) NOT NULL,
                stock INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
''')
    conn.commit()
    cur.close()
    conn.close()
    print("✓ Product table created")

def create_orders_table():
    """Create orders table"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS orders(
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                total_amount DECIMAL(10,2) NOT NULL,
                payment_status VARCHAR(50) DEFAULT 'pending',
                order_status VARCHAR(50) DEFAULT 'created',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
''')
    conn.commit()
    cur.close()
    conn.close()
    print("✓ Orders table created")

def run_migration():
    """Run all migrations"""
    print("Running database migrations...")
    # create_users_table()
    # create_product_table()
    # create_orders_table()
    seed_products()
    print("All migrations completed successfully!")

if __name__ == "__main__":
    run_migration()