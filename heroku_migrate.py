"""
Heroku Database Migration Script
This script adds missing columns to the production PostgreSQL database
"""
import os
from sqlalchemy import create_engine, text

# Get DATABASE_URL from environment
database_url = os.environ.get('DATABASE_URL')

if not database_url:
    raise ValueError("DATABASE_URL environment variable not set")

# Handle postgres:// vs postgresql:// URL format
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

# Create engine and connect
engine = create_engine(database_url)

def migrate():
    with engine.connect() as connection:
        with connection.begin():
            print("Starting database migrations...")
            
            # Add phone column to user table if it doesn't exist
            try:
                connection.execute(text("""
                    ALTER TABLE "user" 
                    ADD COLUMN phone VARCHAR(20);
                """))
                print("✓ Added phone column to user table")
            except Exception as e:
                print(f"phone column: {str(e)[:100]}")
            
            # Add created_at column to user table if it doesn't exist
            try:
                connection.execute(text("""
                    ALTER TABLE "user" 
                    ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                """))
                print("✓ Added created_at column to user table")
            except Exception as e:
                print(f"created_at column: {str(e)[:100]}")
            
            # Add is_admin column to user table if it doesn't exist
            try:
                connection.execute(text("""
                    ALTER TABLE "user" 
                    ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;
                """))
                print("✓ Added is_admin column to user table")
            except Exception as e:
                print(f"is_admin column: {str(e)[:100]}")
            
            # Create discount_code table if it doesn't exist
            try:
                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS discount_code (
                        id SERIAL PRIMARY KEY,
                        code VARCHAR(50) UNIQUE NOT NULL,
                        discount_percent FLOAT NOT NULL,
                        discount_amount FLOAT,
                        max_uses INTEGER,
                        current_uses INTEGER DEFAULT 0,
                        is_active BOOLEAN DEFAULT TRUE,
                        expires_at TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """))
                print("✓ Created discount_code table")
            except Exception as e:
                print(f"discount_code table: {str(e)[:100]}")
            
            # Add created_at to order table if it doesn't exist
            try:
                connection.execute(text("""
                    ALTER TABLE "order" 
                    ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                """))
                print("✓ Added created_at column to order table")
            except Exception as e:
                print(f"order created_at: {str(e)[:100]}")
            
            print("\n✓ Database migration completed successfully!")

if __name__ == '__main__':
    migrate()
