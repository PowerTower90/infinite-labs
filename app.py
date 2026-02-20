from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///peptides.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# PayPal Configuration
app.config['PAYPAL_CLIENT_ID'] = os.environ.get('PAYPAL_CLIENT_ID', 'AeA3m4r7r0DSTqAc0dq26sKss2MisjRvcWd-w5G95CW4bxWKdacMNp-V0tW0Tuz7GVkSjpF4-Fkfl_lP')
app.config['PAYPAL_CLIENT_SECRET'] = os.environ.get('PAYPAL_CLIENT_SECRET', 'ELm-maxx5eMuQajrb7kprQpdcPS9H3DCCaCy5jJNuM_zFPZcycC2DAa0wO1Sg9DHcm8w7hnvKQvJMmQ_')
app.config['PAYPAL_MODE'] = os.environ.get('PAYPAL_MODE', 'sandbox')  # 'sandbox' or 'live'

# Flask-Mail Configuration (Outlook.com / Microsoft 365)
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'Support@infinitelabss.onmicrosoft.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'Soso079979462000')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'Support@infinitelabss.onmicrosoft.com')

mail = Mail(app)

# Fix for Heroku Postgres URL
uri = app.config['SQLALCHEMY_DATABASE_URI']
if uri and uri.startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = uri.replace('postgres://', 'postgresql://', 1)

db = SQLAlchemy(app)

# Database Models
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

# Routes
@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    cart_products = []
    total = 0
    
    for product_id, quantity in cart_items.items():
        product = Product.query.get(int(product_id))
        if product:
            cart_products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })
            total += product.price * quantity
    
    return render_template('cart.html', cart_products=cart_products, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart = session.get('cart', {})
    quantity = int(request.form.get('quantity', 1))
    
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity
    
    session['cart'] = cart
    flash('Product added to cart!', 'success')
    return redirect(url_for('products'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    session['cart'] = cart
    flash('Product removed from cart!', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    cart_items = session.get('cart', {})
    if not cart_items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('products'))
    
    # Calculate cart total
    total = 0
    cart_products = []
    for product_id, quantity in cart_items.items():
        product = Product.query.get(int(product_id))
        if product:
            cart_products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })
            total += product.price * quantity
    
    return render_template('checkout.html', cart_total=total, paypal_client_id=app.config['PAYPAL_CLIENT_ID'])

@app.route('/process_checkout', methods=['POST'])
def process_checkout():
    try:
        # Get form data
        shipping_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address'),
            'city': request.form.get('city'),
            'state': request.form.get('state'),
            'postcode': request.form.get('zip')
        }
        
        # Store shipping data in session
        session['shipping_data'] = shipping_data
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/create_paypal_order', methods=['POST'])
def create_paypal_order():
    try:
        cart_items = session.get('cart', {})
        total = 0
        
        for product_id, quantity in cart_items.items():
            product = Product.query.get(int(product_id))
            if product:
                total += product.price * quantity
        
        # Return order info for PayPal
        return jsonify({
            'success': True,
            'amount': str(round(total, 2))
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/capture_paypal_payment', methods=['POST'])
def capture_paypal_payment():
    try:
        data = request.get_json()
        order_id = data.get('orderID')
        
        # Get cart and shipping data
        cart_items = session.get('cart', {})
        shipping_data = session.get('shipping_data', {})
        
        # Calculate total
        total = 0
        for product_id, quantity in cart_items.items():
            product = Product.query.get(int(product_id))
            if product:
                total += product.price * quantity
        
        # Create order in database
        new_order = Order(
            total=total,
            name=shipping_data.get('name'),
            email=shipping_data.get('email'),
            phone=shipping_data.get('phone'),
            address=shipping_data.get('address'),
            city=shipping_data.get('city'),
            state=shipping_data.get('state'),
            postcode=shipping_data.get('postcode'),
            payment_method='paypal',
            payment_id=order_id,
            payment_status='completed',
            status='completed'
        )
        
        db.session.add(new_order)
        db.session.commit()
        
        # Clear cart and shipping data
        session.pop('cart', None)
        session.pop('shipping_data', None)
        
        return jsonify({
            'success': True,
            'order_id': new_order.id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/process_card_payment', methods=['POST'])
def process_card_payment():
    try:
        data = request.get_json()
        
        # Get cart and shipping data
        cart_items = session.get('cart', {})
        shipping_data = session.get('shipping_data', {})
        
        # Calculate total
        total = 0
        for product_id, quantity in cart_items.items():
            product = Product.query.get(int(product_id))
            if product:
                total += product.price * quantity
        
        # In a real implementation, you would process the card payment here
        # For demo purposes, we'll simulate a successful payment
        card_reference = f"CARD_{os.urandom(8).hex().upper()}"
        
        # Create order in database
        new_order = Order(
            total=total,
            name=shipping_data.get('name'),
            email=shipping_data.get('email'),
            phone=shipping_data.get('phone'),
            address=shipping_data.get('address'),
            city=shipping_data.get('city'),
            state=shipping_data.get('state'),
            postcode=shipping_data.get('postcode'),
            payment_method='card',
            payment_id=card_reference,
            payment_status='completed',
            status='completed'
        )
        
        db.session.add(new_order)
        db.session.commit()
        
        # Clear cart and shipping data
        session.pop('cart', None)
        session.pop('shipping_data', None)
        
        return jsonify({
            'success': True,
            'order_id': new_order.id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/order_success/<int:order_id>')
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_success.html', order=order)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/returns')
def returns():
    return render_template('returns.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier')  # Email address
        password = request.form.get('password')
        
        # Find user by email
        user = User.query.filter_by(email=identifier).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_name'] = user.name
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please check your email and password.', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not email or not password or not name:
            flash('All fields are required', 'error')
            return render_template('signup.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'error')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')
        
        # Validate email format
        if '@' not in email or '.' not in email:
            flash('Please enter a valid email address', 'error')
            return render_template('signup.html')
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('signup.html')
        
        # Create new user
        new_user = User(email=email, name=name)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

# Initialize database
with app.app_context():
    db.create_all()
    
    # Add sample products if database is empty
    if Product.query.count() == 0:
        sample_products = [
            Product(name='BPC-157', description='Body Protection Compound for healing and recovery', price=49.99, stock=100, category='Recovery'),
            Product(name='TB-500', description='Thymosin Beta-4 for tissue repair', price=59.99, stock=75, category='Recovery'),
            Product(name='CJC-1295', description='Growth hormone releasing hormone', price=69.99, stock=50, category='Growth'),
            Product(name='Ipamorelin', description='Growth hormone secretagogue', price=54.99, stock=80, category='Growth'),
        ]
        db.session.add_all(sample_products)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=5500)
