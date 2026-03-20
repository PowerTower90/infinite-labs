from admin_app import admin_app, db, Product

with admin_app.app_context():
    products = Product.query.order_by(Product.id).all()
    print(f"{'ID':>4} | {'SKU':<14} | {'Name':<35} | {'Price':>8} | {'Stock':>6}")
    print('-' * 85)
    for p in products:
        sku = p.sku or 'NO SKU'
        print(f"{p.id:>4} | {sku:<14} | {p.name:<35} | ${p.price:>7.2f} | {str(p.stock):>6}")
