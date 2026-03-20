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
        print("Starting database migrations...")
        
        # Add phone column to user table if it doesn't exist
        try:
            with connection.begin():
                connection.execute(text("""
                    ALTER TABLE "user" 
                    ADD COLUMN phone VARCHAR(20);
                """))
            print("✓ Added phone column to user table")
        except Exception as e:
            print(f"phone column: {str(e)[:100]}")
        
        # Add created_at column to user table if it doesn't exist
        try:
            with connection.begin():
                connection.execute(text("""
                    ALTER TABLE "user" 
                    ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                """))
            print("✓ Added created_at column to user table")
        except Exception as e:
            print(f"created_at column: {str(e)[:100]}")
        
        # Add is_admin column to user table if it doesn't exist
        try:
            with connection.begin():
                connection.execute(text("""
                    ALTER TABLE "user" 
                    ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;
                """))
            print("✓ Added is_admin column to user table")
        except Exception as e:
            print(f"is_admin column: {str(e)[:100]}")
        
        # Create discount_code table if it doesn't exist
        try:
            with connection.begin():
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
            with connection.begin():
                connection.execute(text("""
                    ALTER TABLE "order" 
                    ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                """))
            print("✓ Added created_at column to order table")
        except Exception as e:
            print(f"order created_at: {str(e)[:100]}")
        
        # Add shipping information columns to order table
        order_columns = [
            ("order_number", "VARCHAR(50) UNIQUE"),
            ("name", "VARCHAR(200)"),
            ("email", "VARCHAR(200)"),
            ("phone", "VARCHAR(20)"),
            ("address", "VARCHAR(500)"),
            ("city", "VARCHAR(100)"),
            ("state", "VARCHAR(50)"),
            ("postcode", "VARCHAR(10)"),
            ("payment_method", "VARCHAR(50)"),
            ("payment_id", "VARCHAR(200)"),
            ("payment_status", "VARCHAR(50) DEFAULT 'pending'"),
            ("items_json", "TEXT"),
        ]
        
        for col_name, col_type in order_columns:
            try:
                with connection.begin():
                    connection.execute(text(f"""
                        ALTER TABLE "order" 
                        ADD COLUMN {col_name} {col_type};
                    """))
                print(f"✓ Added {col_name} column to order table")
            except Exception as e:
                print(f"order {col_name}: {str(e)[:100]}")
        
        # Generate order numbers for existing orders that don't have one
        try:
            with connection.begin():
                # First, check if there are any orders without order_number
                result = connection.execute(text("""
                    SELECT id, created_at FROM "order" WHERE order_number IS NULL
                """))
                orders_to_update = result.fetchall()
                
                if orders_to_update:
                    print(f"Found {len(orders_to_update)} orders without order numbers. Generating...")
                    import random
                    import string
                    from datetime import datetime
                    
                    for order in orders_to_update:
                        order_id, created_at = order
                        # Use created_at date if available, otherwise current date
                        if created_at:
                            date_prefix = created_at.strftime('%Y%m')
                        else:
                            date_prefix = datetime.utcnow().strftime('%Y%m')
                        
                        # Generate unique order number
                        max_attempts = 10
                        for attempt in range(max_attempts):
                            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                            order_number = f'INF-{date_prefix}-{random_suffix}'
                            
                            try:
                                connection.execute(text("""
                                    UPDATE "order" SET order_number = :order_number WHERE id = :order_id
                                """), {"order_number": order_number, "order_id": order_id})
                                print(f"  ✓ Generated order number {order_number} for order ID {order_id}")
                                break
                            except Exception as e:
                                if attempt == max_attempts - 1:
                                    print(f"  ✗ Failed to generate unique order number for order ID {order_id}: {str(e)[:100]}")
                                continue
                    
                    print("✓ Completed generating order numbers for existing orders")
                else:
                    print("✓ No existing orders need order numbers")
        except Exception as e:
            print(f"order_number generation: {str(e)[:100]}")
        
        # Add cost column to product table if it doesn't exist
        try:
            with connection.begin():
                connection.execute(text("""
                    ALTER TABLE "product" 
                    ADD COLUMN cost FLOAT DEFAULT 0.0;
                """))
            print("✓ Added cost column to product table")
        except Exception as e:
            print(f"product cost: {str(e)[:100]}")

        # Add product image blob columns if they don't exist
        try:
            with connection.begin():
                connection.execute(text("""
                    ALTER TABLE "product"
                    ADD COLUMN image_data BYTEA;
                """))
            print("✓ Added image_data column to product table")
        except Exception as e:
            print(f"product image_data: {str(e)[:100]}")

        try:
            with connection.begin():
                connection.execute(text("""
                    ALTER TABLE "product"
                    ADD COLUMN image_mime_type VARCHAR(100);
                """))
            print("✓ Added image_mime_type column to product table")
        except Exception as e:
            print(f"product image_mime_type: {str(e)[:100]}")
        
        # Create site_settings table if it doesn't exist
        try:
            with connection.begin():
                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS site_settings (
                        id SERIAL PRIMARY KEY,
                        key VARCHAR(100) UNIQUE NOT NULL,
                        value VARCHAR(500) NOT NULL
                    );
                """))
            print("✓ Created site_settings table")
        except Exception as e:
            print(f"site_settings table: {str(e)[:100]}")
        
        # Seed default shipping settings if not present
        try:
            with connection.begin():
                connection.execute(text("""
                    INSERT INTO site_settings (key, value)
                    VALUES ('free_shipping_threshold', '150.00')
                    ON CONFLICT (key) DO NOTHING;
                """))
                connection.execute(text("""
                    INSERT INTO site_settings (key, value)
                    VALUES ('shipping_fee', '15.00')
                    ON CONFLICT (key) DO NOTHING;
                """))
            print("✓ Seeded default shipping settings")
        except Exception as e:
            print(f"shipping settings seed: {str(e)[:100]}")
        
        print("\n✓ Database migration completed successfully!")

        # Add sku column to product table if it doesn't exist
        try:
            with connection.begin():
                connection.execute(text("""
                    ALTER TABLE "product"
                    ADD COLUMN sku VARCHAR(50) UNIQUE;
                """))
            print("✓ Added sku column to product table")
        except Exception as e:
            print(f"product sku column: {str(e)[:100]}")

        # Populate SKUs for all existing products
        sku_map = {
            2:  'IL-TB50-002',
            34: 'IL-BPC1-034',
            35: 'IL-RETA-035',
            37: 'IL-CJCD-037',
            38: 'IL-CJCN-038',
            39: 'IL-TESA-039',
            40: 'IL-MOTS-040',
            41: 'IL-HCG5-041',
            42: 'IL-DSIP-042',
            43: 'IL-GHKC-043',
            44: 'IL-5AMQ-044',
            45: 'IL-BWAT-045',
        }
        try:
            with connection.begin():
                for product_id, sku in sku_map.items():
                    connection.execute(text(
                        'UPDATE "product" SET sku = :sku WHERE id = :id AND (sku IS NULL OR sku != :sku)'
                    ), {'sku': sku, 'id': product_id})
            print("✓ Populated SKUs for all products")
        except Exception as e:
            print(f"SKU population: {str(e)[:100]}")

        print("\n✓ Database migration completed successfully!")

if __name__ == '__main__':
    migrate()
