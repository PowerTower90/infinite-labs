"""
Update Product Costs Script
Updates all products with their calculated wholesale costs in AUD
Based on USD costs converted at 1.41 exchange rate
"""
import os
from sqlalchemy import create_engine, text

# Product costs mapping (per-vial cost in AUD)
PRODUCT_COSTS = {
    'BPC-157': 11.99,
    'RETATRUTIDE': 14.10,
    'TB-500': 19.74,
    'CJC-1295 DAC': 19.74,
    'CJC-1295 no DAC': 13.40,
    'CJC-1295': 13.40,  # Fallback for products without DAC specifier
    'TESAMORELIN': 26.79,
    'MOTS-C': 9.87,
    'HCG': 12.69,
    'DSIP': 9.17,
    'GHK-CU': 8.46,
    '5-AMINO-1MQ': 21.15,
    'Bacteriostatic Water': 1.41,
}

def update_costs():
    """Update product costs in the database"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    # Handle postgres:// vs postgresql:// URL format
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    engine = create_engine(database_url)
    
    with engine.connect() as connection:
        print("Starting product cost updates...")
        
        # Get all products
        result = connection.execute(text("SELECT id, name FROM product"))
        products = result.fetchall()
        
        if not products:
            print("No products found in database")
            return
        
        print(f"Found {len(products)} products")
        
        for product_id, product_name in products:
            # Try to match product name to cost mapping
            cost = None
            for key, value in PRODUCT_COSTS.items():
                if key.upper() in product_name.upper():
                    cost = value
                    break
            
            if cost:
                try:
                    with connection.begin():
                        connection.execute(
                            text("UPDATE product SET cost = :cost WHERE id = :id"),
                            {"cost": cost, "id": product_id}
                        )
                    print(f"✓ Updated '{product_name}' with cost ${cost:.2f} AUD")
                except Exception as e:
                    print(f"✗ Failed to update '{product_name}': {str(e)[:100]}")
            else:
                print(f"⚠ No cost mapping found for '{product_name}' - skipped")
        
        print("\n✓ Product cost update completed!")

if __name__ == '__main__':
    update_costs()
