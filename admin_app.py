from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import threading
import json

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

# Flask-Mail Configuration (Outlook.com / Microsoft 365)
admin_app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
admin_app.config['MAIL_PORT'] = 587
admin_app.config['MAIL_USE_TLS'] = True
admin_app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'Support@infinitelabs.health')
admin_app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'Soso079979462000')
admin_app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'Support@infinitelabs.health')

mail = Mail(admin_app)


def send_shipping_notification_email(order, tracking_number=None, carrier=None, estimated_delivery=None):
    """Send shipping notification in a background thread so the admin response returns instantly."""
    data = dict(
        order_id=order.id,
        recipient=order.email,
        tracking_number=tracking_number or '',
        estimated_delivery=estimated_delivery or '3-7 business days',
        customer_name=order.name,
        customer_address=order.address,
        customer_city=order.city,
        customer_state=order.state,
        customer_postcode=order.postcode,
        customer_phone=order.phone,
        order_total=order.total,
        carrier=carrier or '',
    )

    def _send(data):
        with admin_app.app_context():
            try:
                import os as _os
                tmpl_path = _os.path.join(_os.path.dirname(__file__), 'templates', 'emails', 'shipping_notification.html')
                with open(tmpl_path, 'r', encoding='utf-8') as f:
                    from jinja2 import Template
                    html_body = Template(f.read()).render(**{k: v for k, v in data.items() if k != 'recipient'})
                msg = Message(
                    subject=f'Your Infinite Labs Order #{data["order_id"]} Has Shipped!',
                    recipients=[data['recipient']],
                    html=html_body,
                )
                mail.send(msg)
            except Exception as e:
                admin_app.logger.error(f'Shipping notification email failed for order #{data["order_id"]}: {e}')

    threading.Thread(target=_send, args=(data,), daemon=True).start()


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
    
    # Shipping Information
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(500))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    postcode = db.Column(db.String(10))
    
    # Payment Information
    payment_method = db.Column(db.String(50))  # 'card' or 'paypal'
    payment_id = db.Column(db.String(200))  # PayPal transaction ID or card reference
    payment_status = db.Column(db.String(50), default='pending')
    items_json = db.Column(db.Text)  # JSON snapshot: {"product_id": quantity, ...}

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

# Order Management Routes
@admin_app.route('/orders')
@admin_required
def orders():
    # Get all orders, most recent first
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin_orders.html', orders=all_orders)

@admin_app.route('/orders/<int:order_id>/resend_email', methods=['POST'])
@admin_required
def resend_order_email(order_id):
    order = Order.query.get_or_404(order_id)

    def _send(data):
        with admin_app.app_context():
            from datetime import datetime
            try:
                # Reconstruct order items from stored JSON
                order_items = []
                order_subtotal = 0.0
                if data.get('items_json'):
                    snapshot = json.loads(data['items_json'])
                    for pid, qty in snapshot.items():
                        product = Product.query.get(int(pid))
                        if product:
                            item_total = product.price * qty
                            order_subtotal += item_total
                            order_items.append({
                                'product_name': product.name,
                                'product_description': product.description,
                                'quantity': qty,
                                'price': product.price,
                                'total': item_total,
                            })

                # Use stored total if no items could be reconstructed
                if not order_items:
                    order_subtotal = round(data['order_total'] / 1.10, 2)

                order_tax = round(order_subtotal * 0.10, 2)

                template_vars = dict(
                    order_id=data['order_id'],
                    customer_name=data['customer_name'],
                    customer_email=data['customer_email'],
                    customer_phone=data['customer_phone'],
                    customer_address=data['customer_address'],
                    customer_city=data['customer_city'],
                    customer_state=data['customer_state'],
                    customer_postcode=data['customer_postcode'],
                    order_items=order_items,
                    order_subtotal=order_subtotal,
                    order_tax=order_tax,
                    order_total=data['order_total'],
                    order_status=data['order_status'],
                    payment_date=data['payment_date'],
                    payment_method=data['payment_method'],
                    transaction_id=data['transaction_id'],
                )
                # Load the template from the main templates folder (admin_app has a different template_folder)
                template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'emails', 'order_confirmation.html')
                with open(template_path, encoding='utf-8') as _f:
                    template_str = _f.read()
                from flask import render_template_string
                html_body = render_template_string(template_str, **template_vars)
                msg = Message(
                    subject=f'Order Confirmation & Receipt - Infinite Labs #{data["order_id"]}',
                    recipients=[data['recipient']],
                    html=html_body,
                )
                mail.send(msg)
                admin_app.logger.info(f'Resent order confirmation email for order #{data["order_id"]}')
            except Exception as e:
                admin_app.logger.error(f'Resend email failed for order #{data["order_id"]}: {e}')

    from datetime import datetime
    payment_date = order.created_at.strftime('%d %B %Y') if order.created_at else datetime.utcnow().strftime('%d %B %Y')
    data = dict(
        order_id=order.id,
        recipient=order.email,
        customer_name=order.name,
        customer_email=order.email,
        customer_phone=order.phone,
        customer_address=order.address,
        customer_city=order.city,
        customer_state=order.state,
        customer_postcode=order.postcode,
        order_total=order.total,
        order_status=order.status,
        payment_date=payment_date,
        payment_method=order.payment_method,
        transaction_id=order.payment_id,
        items_json=order.items_json,
    )
    threading.Thread(target=_send, args=(data,), daemon=True).start()
    flash(f'Confirmation email queued for resend to {order.email}', 'success')
    return redirect(url_for('order_detail', order_id=order_id))


@admin_app.route('/orders/<int:order_id>')
@admin_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin_order_detail.html', order=order)

@admin_app.route('/orders/update_status/<int:order_id>', methods=['POST'])
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f'Order #{order_id} status updated to {new_status}!', 'success')

        # Send shipping notification when status changes to 'shipped'
        if new_status == 'shipped':
            tracking_number = request.form.get('tracking_number', '').strip() or None
            carrier = request.form.get('carrier', '').strip() or None
            estimated_delivery = request.form.get('estimated_delivery', '').strip() or None
            send_shipping_notification_email(order, tracking_number, carrier, estimated_delivery)
    else:
        flash('Invalid status!', 'error')
    
    return redirect(url_for('order_detail', order_id=order_id))

@admin_app.route('/orders/delete/<int:order_id>')
@admin_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash(f'Order #{order_id} deleted successfully!', 'success')
    return redirect(url_for('orders'))


# ── Email Templates ────────────────────────────────────────────────────────

EMAIL_TEMPLATES = [
    {
        'key': 'order_confirmation',
        'filename': 'templates/emails/order_confirmation.html',
        'trigger': 'Customer completes payment (PayPal or card)',
        'variables': [
            'order_id', 'customer_name', 'customer_email', 'customer_phone',
            'customer_address', 'customer_city', 'customer_state', 'customer_postcode',
            'order_items', 'order_subtotal', 'order_tax', 'order_total',
            'order_status', 'payment_method', 'transaction_id',
        ],
    },
    {
        'key': 'payment_confirmation',
        'filename': 'templates/emails/payment_confirmation.html',
        'trigger': 'Customer completes payment (sent alongside order confirmation)',
        'variables': [
            'order_id', 'transaction_id', 'payment_date', 'payment_method',
            'payment_amount', 'order_subtotal', 'order_tax',
            'customer_name', 'customer_address', 'customer_city',
            'customer_state', 'customer_postcode',
        ],
    },
    {
        'key': 'shipping_notification',
        'filename': 'templates/emails/shipping_notification.html',
        'trigger': 'Admin marks order as \'Shipped\'',
        'variables': [
            'order_id', 'tracking_number', 'carrier', 'estimated_delivery',
            'customer_name', 'customer_phone',
            'customer_address', 'customer_city', 'customer_state', 'customer_postcode',
            'order_total',
        ],
    },
]


@admin_app.route('/email-templates')
@admin_required
def email_templates():
    import os as _os
    tpls = []
    base = _os.path.dirname(_os.path.abspath(__file__))
    for t in EMAIL_TEMPLATES:
        path = _os.path.join(base, t['filename'])
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            content = f'<!-- Template file not found: {t["filename"]} -->'
        tpls.append({**t, 'content': content})
    return render_template('admin_email_templates.html', templates=tpls)


@admin_app.route('/email-templates/save/<template_key>', methods=['POST'])
@admin_required
def save_email_template(template_key):
    import os as _os
    from flask import request as _req
    # Validate key
    allowed_keys = {t['key'] for t in EMAIL_TEMPLATES}
    if template_key not in allowed_keys:
        return jsonify({'success': False, 'error': 'Unknown template key'}), 400
    data = _req.get_json()
    content = data.get('content', '')
    base = _os.path.dirname(_os.path.abspath(__file__))
    tpl_meta = next(t for t in EMAIL_TEMPLATES if t['key'] == template_key)
    path = _os.path.join(base, tpl_meta['filename'])
    try:
        _os.makedirs(_os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    with admin_app.app_context():
        db.create_all()
    admin_app.run(debug=True, port=5001)
