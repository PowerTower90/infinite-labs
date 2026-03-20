"""Migration: Add SKU column to products and populate all existing products."""
from app import app, db, Product
from sqlalchemy import text

SKU_MAP = {
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

with app.app_context():
    # Add the column if it doesn't exist
    try:
        db.session.execute(text('ALTER TABLE product ADD COLUMN sku VARCHAR(50) UNIQUE'))
        db.session.commit()
        print('Column "sku" added.')
    except Exception as e:
        db.session.rollback()
        print(f'Column may already exist: {e}')

    # Populate SKUs
    updated = 0
    for product_id, sku in SKU_MAP.items():
        product = Product.query.get(product_id)
        if product:
            product.sku = sku
            updated += 1
            print(f'  Set {product.name} → {sku}')
        else:
            print(f'  Product ID {product_id} not found, skipping.')

    db.session.commit()
    print(f'\nDone. {updated} products updated with SKUs.')

    # Print summary
    print('\n--- Current SKUs ---')
    for p in Product.query.order_by(Product.id).all():
        print(f'  ID {p.id:>3} | {p.sku or "NO SKU":15} | {p.name}')
