"""
Convert Product Prices from USD to AUD
Multiplies all product prices by 1.41 exchange rate
"""
import os
from sqlalchemy import create_engine, text

USD_TO_AUD = 1.41

def convert_prices():
    """Convert all product prices from USD to AUD"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    # Handle postgres:// vs postgresql:// URL format
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    engine = create_engine(database_url)
    
    with engine.connect() as connection:
        print("Starting price conversion from USD to AUD...")
        print(f"Exchange rate: 1 USD = {USD_TO_AUD} AUD\n")
        
        with connection.begin():
            # Get all products with their current prices
            result = connection.execute(text("SELECT id, name, price FROM product"))
            products = result.fetchall()
            
            if not products:
                print("No products found in database")
                return
            
            print(f"Found {len(products)} products\n")
            
            for product_id, product_name, current_price_usd in products:
                # Calculate new AUD price
                new_price_aud = round(current_price_usd * USD_TO_AUD, 2)
                
                try:
                    connection.execute(
                        text("UPDATE product SET price = :price WHERE id = :id"),
                        {"price": new_price_aud, "id": product_id}
                    )
                    print(f"✓ {product_name}")
                    print(f"  USD ${current_price_usd:.2f} → AUD ${new_price_aud:.2f}")
                except Exception as e:
                    print(f"✗ Failed to update '{product_name}': {str(e)[:100]}")
        
        print("\n✓ Price conversion completed!")

if __name__ == '__main__':
    convert_prices()
