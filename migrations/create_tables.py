import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import get_db

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
    create_users_table()
    create_product_table()
    create_orders_table()
    print("All migrations completed successfully!")

if __name__ == "__main__":
    run_migration()