# Admin Dashboard Documentation

## Overview

The Infinite Labs Admin Dashboard is a secure, separate web application for managing your peptides ecommerce store. It provides complete control over products, inventory, and discount codes.

**Live Admin Panel:** https://admin-infinite-labs.herokuapp.com/  
**Main Website:** https://infinite-labs-peptides-8b9f5f5d8ca1.herokuapp.com/

---

## Login Credentials

**Username:** 0430333416  
**Password:** Soso079979462000

⚠️ **IMPORTANT:** Keep these credentials secure. Never share them publicly or commit them to public repositories.

---

## Features

### 1. Dashboard Overview
- **Total Products:** View count of all products in inventory
- **Low Stock Alerts:** Automatic warnings when products fall below 10 units
- **Order Tracking:** Monitor total orders placed
- **Active Discounts:** Track discount codes currently in use

### 2. Product Management
**View Products:**
- Complete inventory table with ID, name, category, price, stock, and status
- Color-coded stock badges (green: in stock, yellow: low stock, red: out of stock)
- Search and sort functionality

**Add New Product:**
- Name (required)
- Category: Growth, Recovery, Performance, Wellness, Research
- Price (USD)
- Stock quantity
- Image URL (optional)
- Description (required)

**Edit Product:**
- Modify any product field
- Update inventory levels
- Change pricing

**Delete Product:**
- Permanently remove products from catalog
- Confirmation prompt to prevent accidental deletion

### 3. Discount Code Management
**Create Discount Codes:**
- Custom code name (e.g., WELCOME20, SAVE50)
- Percentage discount (0-100%)
- Fixed amount discount (dollar value)
- Maximum usage limit (optional for unlimited)

**Manage Discount Codes:**
- View all active and inactive codes
- Track usage statistics (current uses / max uses)
- Activate/deactivate codes without deleting
- Delete expired or unwanted codes

---

## Design Theme

**Dark Mode Interface:**
- Primary Color: Blue (#3b82f6)
- Background: Dark gray (#020617)
- Cards: Slate (#1e293b)
- Text: Light gray (#e2e8f0)
- Accents: Success (green), Warning (orange), Danger (red)

**Professional Features:**
- Glowing hover effects on interactive elements
- Smooth transitions and animations
- Responsive design for mobile and tablet
- Clean, modern typography

---

## Technical Architecture

### Separate Application
The admin dashboard runs as a **completely separate Flask application** from the main website:

**Main Website:**
- File: `app.py`
- Templates: `templates/`
- URL: https://infinite-labs-peptides-8b9f5f5d8ca1.herokuapp.com/

**Admin Dashboard:**
- File: `admin_app.py`
- Templates: `admin_templates/`
- Styles: `static/css/admin.css`
- URL: https://admin-infinite-labs.herokuapp.com/

### Shared Database
Both applications connect to the same database:
- **Local:** SQLite (`instance/peptides.db`)
- **Production:** PostgreSQL (configured via DATABASE_URL environment variable)

### Security Features
1. **Session-Based Authentication:** Login required for all admin pages
2. **Admin Flag:** Users must have `is_admin = True` in database
3. **Decorator Protection:** `@admin_required` on all admin routes
4. **No Public Links:** Zero references to admin panel from main website
5. **Separate Deployment:** Different Heroku app = different URL

---

## Database Models

### User Model
```python
- id (Integer, Primary Key)
- email (String, Unique) - Used as username
- password_hash (String) - Encrypted password
- name (String)
- phone (String)
- is_admin (Boolean) - Must be True to access admin
- created_at (DateTime)
```

### Product Model
```python
- id (Integer, Primary Key)
- name (String, Required)
- description (Text, Required)
- price (Float, Required)
- stock (Integer, Default: 0)
- image_url (String, Optional)
- category (String) - Growth/Recovery/Performance/Wellness/Research
```

### DiscountCode Model
```python
- id (Integer, Primary Key)
- code (String, Unique, Required)
- discount_percent (Float, 0-100)
- discount_amount (Float) - Fixed dollar discount
- max_uses (Integer, Optional) - Null = unlimited
- current_uses (Integer, Default: 0)
- is_active (Boolean, Default: True)
- created_at (DateTime)
```

### Order Model
```python
- id (Integer, Primary Key)
- user_id (Integer, Foreign Key)
- total (Float, Required)
- status (String) - pending/completed/cancelled
- created_at (DateTime)
```

---

## Admin Routes

All routes require authentication (`@admin_required` decorator)

### Authentication
- `GET /` - Login page (redirects to dashboard if already logged in)
- `POST /login` - Process login credentials
- `GET /logout` - End session and redirect to login

### Dashboard
- `GET /dashboard` - Main admin overview with statistics

### Products
- `GET /products` - View all products table
- `GET /products/add` - Show add product form
- `POST /products/add` - Create new product
- `GET /products/edit/<id>` - Show edit form for specific product
- `POST /products/edit/<id>` - Update specific product
- `POST /products/delete/<id>` - Remove product from database

### Discounts
- `GET /discounts` - View all discount codes table
- `GET /discounts/add` - Show add discount form
- `POST /discounts/add` - Create new discount code
- `POST /discounts/toggle/<id>` - Activate/deactivate discount code
- `POST /discounts/delete/<id>` - Remove discount code

---

## Local Development

### Running Admin Dashboard Locally

1. **Ensure database is set up:**
```powershell
python setup_admin.py
```

2. **Start the admin server:**
```powershell
python admin_app.py
```

3. **Access locally:**
```
http://localhost:5001
```

### Running Main Website Locally

```powershell
python app.py
```
Access at: http://localhost:5000

---

## Deployment

### Main Website Deployment
```powershell
git push heroku main
```

### Admin Dashboard Deployment
```powershell
# Add Heroku remote for admin app
heroku git:remote -a admin-infinite-labs

# Deploy admin dashboard
git push heroku-admin main
```

### Environment Variables (Set in Heroku Dashboard)

**For Admin App:**
- `ADMIN_SECRET_KEY` - Secure random key for sessions
- `DATABASE_URL` - Shared PostgreSQL database connection (set automatically)

**For Main App:**
- `SECRET_KEY` - Secure random key for sessions
- `DATABASE_URL` - PostgreSQL database connection (set automatically)

---

## Maintenance Tasks

### Adding a New Admin User

Run this script locally or use Heroku console:
```python
python setup_admin.py
```

Or manually via Python console:
```python
from app import app, db, User
with app.app_context():
    admin = User(
        email='username_here',
        name='Admin Name',
        is_admin=True
    )
    admin.set_password('secure_password_here')
    db.session.add(admin)
    db.session.commit()
```

### Updating Database Schema

If you add new columns to models, update the database:
```python
python setup_admin.py  # Includes schema updates
```

### Checking Logs

**Heroku Logs (Admin):**
```powershell
heroku logs --tail -a admin-infinite-labs
```

**Heroku Logs (Main Site):**
```powershell
heroku logs --tail -a infinite-labs-peptides
```

---

## Troubleshooting

### Issue: "Invalid username or password"
**Solution:** Ensure the user has `is_admin = True` in the database. Regular users cannot log in to admin panel.

### Issue: "Database connection error"
**Solution:** Check that `DATABASE_URL` environment variable is set correctly in Heroku.

### Issue: "Page not found after login"
**Solution:** Clear browser cache and cookies, then try logging in again.

### Issue: "Changes not appearing on live site"
**Solution:** 
1. Verify deployment was successful: `git push heroku main`
2. Check Heroku logs for errors
3. Ensure database migrations ran successfully

---

## Security Best Practices

1. **Change Default Credentials:** Update the admin password regularly
2. **Use Strong Passwords:** Minimum 12 characters with mixed case, numbers, symbols
3. **Limit Admin Access:** Only create admin accounts for trusted personnel
4. **Monitor Login Attempts:** Check logs for suspicious activity
5. **Keep Separate:** Never link admin panel from the public website
6. **HTTPS Only:** Admin panel uses encrypted HTTPS connection (automatic on Heroku)
7. **Session Timeout:** Log out when finished working

---

## File Structure

```
infinite-labs/
├── admin_app.py              # Admin Flask application
├── admin_templates/          # Admin HTML templates
│   ├── admin_base.html       # Base template with nav
│   ├── admin_login.html      # Login page
│   ├── admin_dashboard.html  # Dashboard overview
│   ├── admin_products.html   # Product inventory table
│   ├── admin_add_product.html
│   ├── admin_edit_product.html
│   ├── admin_discounts.html  # Discount codes table
│   └── admin_add_discount.html
├── static/css/admin.css      # Dark theme styles
├── setup_admin.py            # Database setup script
├── instance/
│   └── peptides.db          # SQLite database (local only)
└── Procfile                 # Heroku process configuration
```

---

## Support

For technical issues or questions about the admin dashboard:
1. Check this documentation first
2. Review error messages in Heroku logs
3. Verify database connection and credentials
4. Contact your developer for assistance

---

**Last Updated:** February 15, 2026  
**Version:** 1.0  
**Admin Dashboard URL:** https://admin-infinite-labs.herokuapp.com/
