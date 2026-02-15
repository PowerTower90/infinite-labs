from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

admin_app = Flask(__name__, template_folder='admin_templates', static_folder='static')
admin_app.config['SECRET_KEY'] = os.environ.get('ADMIN_SECRET_KEY', 'admin-secret-key-change-in-production')

# Database configuration - use absolute path for SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
admin_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "instance", "peptides.db")}')
admin_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Fix for Heroku Postgres URL
uri = admin_app.config['SQLALCHEMY_DATABASE_URI']
if uri and uri.startswith('postgres://'):
    admin_app.config['SQLALCHEMY_DATABASE_URI'] = uri.replace('postgres://', 'postgresql://', 1)

db = SQLAlchemy(admin_app)

# Database Models (same as main app)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    category = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<Product {self.name}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class DiscountCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_percent = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float)
    max_uses = db.Column(db.Integer)
    current_uses = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access the admin panel.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@admin_app.route('/')
def admin_login():
    if 'admin_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('admin_login.html')

@admin_app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(password):
        session['admin_id'] = user.id
        session['admin_name'] = user.name
        flash('Successfully logged in!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid credentials or unauthorized access.', 'error')
        return redirect(url_for('admin_login'))

@admin_app.route('/logout')
def logout():
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    flash('Successfully logged out.', 'success')
    return redirect(url_for('admin_login'))

@admin_app.route('/dashboard')
@admin_required
def dashboard():
    total_products = Product.query.count()
    low_stock = Product.query.filter(Product.stock < 10).count()
    total_orders = Order.query.count()
    
    # Try to get active discounts, but default to 0 if table doesn't exist
    try:
        active_discounts = DiscountCode.query.filter_by(is_active=True).count()
    except:
        active_discounts = 0
    
    return render_template('admin_dashboard.html', 
                         total_products=total_products,
                         low_stock=low_stock,
                         total_orders=total_orders,
                         active_discounts=active_discounts)

# Product Management Routes
@admin_app.route('/products')
@admin_required
def products():
    all_products = Product.query.all()
    return render_template('admin_products.html', products=all_products)

@admin_app.route('/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        image_url = request.form.get('image_url')
        category = request.form.get('category')
        
        new_product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            image_url=image_url,
            category=category
        )
        
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('admin_add_product.html')

@admin_app.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        product.image_url = request.form.get('image_url')
        product.category = request.form.get('category')
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('admin_edit_product.html', product=product)

@admin_app.route('/products/delete/<int:product_id>')
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products'))

# Discount Code Management Routes (Disabled - table not available in production)
# @admin_app.route('/discounts')
# @admin_required
# def discounts():
#     all_discounts = DiscountCode.query.all()
#     return render_template('admin_discounts.html', discounts=all_discounts)

# @admin_app.route('/discounts/add', methods=['GET', 'POST'])
# @admin_required
# def add_discount():
#     if request.method == 'POST':
#         code = request.form.get('code').upper()
#         discount_percent = float(request.form.get('discount_percent', 0))
#         discount_amount = request.form.get('discount_amount')
#         max_uses = request.form.get('max_uses')
#         
#         if discount_amount:
#             discount_amount = float(discount_amount)
#         if max_uses:
#             max_uses = int(max_uses)
#         
#         new_discount = DiscountCode(
#             code=code,
#             discount_percent=discount_percent,
#             discount_amount=discount_amount,
#             max_uses=max_uses
#         )
#         
#         db.session.add(new_discount)
#         db.session.commit()
#         flash('Discount code created successfully!', 'success')
#         return redirect(url_for('discounts'))
#     
#     return render_template('admin_add_discount.html')

# @admin_app.route('/discounts/toggle/<int:discount_id>')
# @admin_required
# def toggle_discount(discount_id):
#     discount = DiscountCode.query.get_or_404(discount_id)
#     discount.is_active = not discount.is_active
#     db.session.commit()
#     status = 'activated' if discount.is_active else 'deactivated'
#     flash(f'Discount code {status} successfully!', 'success')
#     return redirect(url_for('discounts'))

# @admin_app.route('/discounts/delete/<int:discount_id>')
# @admin_required
# def delete_discount(discount_id):
#     discount = DiscountCode.query.get_or_404(discount_id)
#     db.session.delete(discount)
#     db.session.commit()
#     flash('Discount code deleted successfully!', 'success')
#     return redirect(url_for('discounts'))

if __name__ == '__main__':
    with admin_app.app_context():
        db.create_all()
    admin_app.run(debug=True, port=5001)
