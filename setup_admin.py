"""
Script to update database schema and create admin user
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash

# Get database path
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'peptides.db')

def update_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Updating database schema...")
    
    # Check and add is_admin column if it doesn't exist
    try:
        cursor.execute("SELECT is_admin FROM user LIMIT 1")
        print("✓ is_admin column already exists")
    except sqlite3.OperationalError:
        print("Adding is_admin column...")
        cursor.execute("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0")
        conn.commit()
        print("✓ is_admin column added")
    
    # Check and add phone column if it doesn't exist
    try:
        cursor.execute("SELECT phone FROM user LIMIT 1")
        print("✓ phone column already exists")
    except sqlite3.OperationalError:
        print("Adding phone column...")
        cursor.execute("ALTER TABLE user ADD COLUMN phone VARCHAR(20)")
        conn.commit()
        print("✓ phone column added")
    
    # Check and add created_at column if it doesn't exist
    try:
        cursor.execute("SELECT created_at FROM user LIMIT 1")
        print("✓ created_at column already exists")
    except sqlite3.OperationalError:
        print("Adding created_at column...")
        cursor.execute("ALTER TABLE user ADD COLUMN created_at DATETIME")
        conn.commit()
        # Update existing rows with current timestamp
        cursor.execute("UPDATE user SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
        conn.commit()
        print("✓ created_at column added")
    
    # Check if admin user exists
    cursor.execute("SELECT id FROM user WHERE email = ?", ('0430333416',))
    existing_admin = cursor.fetchone()
    
    if existing_admin:
        print("\nAdmin user already exists. Updating password and admin status...")
        password_hash = generate_password_hash('Soso079979462000')
        cursor.execute(
            "UPDATE user SET password_hash = ?, is_admin = 1 WHERE email = ?",
            (password_hash, '0430333416')
        )
        conn.commit()
        print("✓ Admin user updated successfully!")
    else:
        print("\nCreating admin user...")
        password_hash = generate_password_hash('Soso079979462000')
        cursor.execute(
            """INSERT INTO user (email, password_hash, name, is_admin) 
               VALUES (?, ?, ?, ?)""",
            ('0430333416', password_hash, 'Administrator', 1)
        )
        conn.commit()
        print("✓ Admin user created successfully!")
    
    conn.close()
    
    print("\n" + "="*50)
    print("ADMIN LOGIN CREDENTIALS")
    print("="*50)
    print(f"Username: 0430333416")
    print(f"Password: Soso079979462000")
    print(f"\nAccess admin panel at: http://localhost:5001")
    print("="*50)

if __name__ == '__main__':
    update_database()
