#!/usr/bin/env python
"""Script to add peptide products to the database"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from admin_app import admin_app, db, Product

# List of products to add
products_to_add = [
    {
        'name': 'BPC-157 10mg',
        'description': 'BPC-157 (Body Protection Compound-157) - 10mg vial',
        'price': 45.00,
        'stock': 50,
        'category': 'Peptides',
        'image_url': None
    },
    {
        'name': 'RETATRUTIDE 10mg',
        'description': 'RETATRUTIDE - 10mg vial',
        'price': 65.00,
        'stock': 50,
        'category': 'Peptides',
        'image_url': None
    },
    {
        'name': 'TB-500 10mg',
        'description': 'TB-500 (Thymosin Beta-4) - 10mg vial',
        'price': 55.00,
        'stock': 50,
        'category': 'Peptides',
        'image_url': None
    },
    {
        'name': 'CJC-1295 DAC 5mg',
        'description': 'CJC-1295 with DAC (Drug Affinity Complex) - 5mg vial',
        'price': 50.00,
        'stock': 50,
        'category': 'Peptides',
        'image_url': None
    },
    {
        'name': 'CJC-1295 DAC 5mg no DAC',
        'description': 'CJC-1295 without DAC (Drug Affinity Complex) - 5mg vial',
        'price': 40.00,
        'stock': 50,
        'category': 'Peptides',
        'image_url': None
    },
    {
        'name': 'TESAMORELIN 10MG',
        'description': 'TESAMORELIN - 10mg vial',
        'price': 60.00,
        'stock': 50,
        'category': 'Peptides',
        'image_url': None
    },
    {
        'name': 'MOTS-C 10MG',
        'description': 'MOTS-C - 10mg vial',
        'price': 55.00,
        'stock': 50,
        'category': 'Peptides',
        'image_url': None
    },
    {
        'name': 'HCG 5000IU',
        'description': 'HCG (Human Chorionic Gonadotropin) - 5000IU vial',
        'price': 35.00,
        'stock': 50,
        'category': 'Peptides',
        'image_url': None
    },
    {
        'name': 'DSIP 5mg',
        'description': 'DSIP (Delta Sleep Inducing Peptide) - 5mg vial',
        'price': 48.00,
        'stock': 50,
        'category': 'Peptides',
        'image_url': None
    },
    {
        'name': 'GHK-CU 10mg',
        'description': 'GHK-CU - 10mg vial',
        'price': 52.00,
        'stock': 50,
        'category': 'Peptides',
        'image_url': None
    },
    {
        'name': '5-AMINO-1MQ 50MG',
        'description': '5-AMINO-1MQ - 50mg vial',
        'price': 58.00,
        'stock': 50,
        'category': 'Peptides',
        'image_url': None
    },
    {
        'name': 'Bacteriostatic Water 10mL',
        'description': 'Bacteriostatic Water - 10mL vial',
        'price': 15.00,
        'stock': 100,
        'category': 'Supplies',
        'image_url': None
    },
]

def main():
    with admin_app.app_context():
        # Get existing products
        existing_products = Product.query.all()
        existing_names = {p.name for p in existing_products}
        
        print("=" * 70)
        print("PRODUCT ADD REPORT")
        print("=" * 70)
        print(f"\nExisting products in database: {len(existing_names)}")
        if existing_names:
            for name in sorted(existing_names):
                print(f"  - {name}")
        
        added_count = 0
        skipped_count = 0
        added_products = []
        skipped_products = []
        
        print("\n" + "-" * 70)
        print("ADDING NEW PRODUCTS")
        print("-" * 70)
        
        for product_data in products_to_add:
            if product_data['name'] in existing_names:
                print(f"⊘ SKIPPED: {product_data['name']}")
                skipped_products.append(product_data['name'])
                skipped_count += 1
            else:
                try:
                    new_product = Product(**product_data)
                    db.session.add(new_product)
                    db.session.commit()
                    print(f"✓ ADDED: {product_data['name']}")
                    added_products.append(product_data['name'])
                    added_count += 1
                except Exception as e:
                    print(f"✗ ERROR adding {product_data['name']}: {str(e)}")
                    db.session.rollback()
        
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"\nProducts Added:    {added_count}")
        if added_products:
            for name in sorted(added_products):
                print(f"  ✓ {name}")
        
        print(f"\nProducts Skipped:  {skipped_count}")
        if skipped_products:
            for name in sorted(skipped_products):
                print(f"  ⊘ {name}")
        
        print(f"\nTotal Products in Database: {Product.query.count()}")
        print("=" * 70)

if __name__ == '__main__':
    main()
