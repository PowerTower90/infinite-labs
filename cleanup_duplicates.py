#!/usr/bin/env python
"""Remove duplicate products from database"""

from admin_app import admin_app, db, Product

with admin_app.app_context():
    # Delete duplicates: BPC-157 10mg (ID 5) and TB-500 10mg (ID 7)
    duplicates_to_delete = [5, 7]
    
    print('DELETING DUPLICATES')
    print('=' * 70)
    for product_id in duplicates_to_delete:
        product = Product.query.get(product_id)
        if product:
            print(f'✓ Deleting ID {product_id}: {product.name}')
            db.session.delete(product)
    
    db.session.commit()
    
    print('\n' + '=' * 70)
    print('FINAL PRODUCT LIST (NON-DUPLICATES):')
    print('=' * 70)
    products = Product.query.all()
    for p in sorted(products, key=lambda x: x.name):
        print(f'ID: {p.id:2d} | {p.name:45s} | ${p.price:6.2f}')
    
    print('\n' + '=' * 70)
    print(f'Total Products: {Product.query.count()}')
    print('=' * 70)
