#!/usr/bin/env python
"""Check products in database"""

from admin_app import admin_app, db, Product

with admin_app.app_context():
    products = Product.query.all()
    print(f'Total products in database: {len(products)}')
    print('=' * 70)
    for p in sorted(products, key=lambda x: x.name):
        print(f'ID: {p.id:2d} | {p.name:45s} | ${p.price:6.2f}')
