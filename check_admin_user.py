#!/usr/bin/env python
"""
Check if admin user exists and create it if needed
"""
import os
from admin_app import db, User, admin_app

database_url = os.environ.get('DATABASE_URL')
if not database_url:
    database_url = 'sqlite:///instance/peptides.db'

with admin_app.app_context():
    # Check if user exists
    user = User.query.filter_by(email='0430333416').first()
    
    if user:
        print("✓ Admin user already exists")
        print(f"  Email: {user.email}")
        print(f"  Name: {user.name}")
    else:
        print("✗ Admin user does not exist - creating...")
        new_user = User(
            email='0430333416',
            name='Admin User'
        )
        new_user.set_password('Soso079979462000')
        
        db.session.add(new_user)
        db.session.commit()
        
        print("✓ Admin user created successfully!")
        print(f"  Email: 0430333416")
        print(f"  Password: Soso079979462000")
