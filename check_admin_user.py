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
    admin_password = os.environ.get('ADMIN_BOOTSTRAP_PASSWORD')

    # Check if user exists
    user = User.query.filter_by(email='0430333416').first()
    
    if user:
        print("✓ Admin user already exists")
        print(f"  Email: {user.email}")
        print(f"  Name: {user.name}")
    else:
        print("✗ Admin user does not exist - creating...")
        if not admin_password:
            print("Error: ADMIN_BOOTSTRAP_PASSWORD is not set.")
            print("Set it before running this script.")
            raise SystemExit(1)

        new_user = User(
            email='0430333416',
            name='Admin User'
        )
        new_user.set_password(admin_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        print("✓ Admin user created successfully!")
        print(f"  Email: 0430333416")
        print(f"  Password: [value from ADMIN_BOOTSTRAP_PASSWORD]")
