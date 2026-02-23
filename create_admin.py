"""
Script to create an admin user for the admin panel
"""
import os
from app import app, db, User

def create_admin():
    admin_password = os.environ.get('ADMIN_BOOTSTRAP_PASSWORD')
    if not admin_password:
        print("Error: ADMIN_BOOTSTRAP_PASSWORD is not set.")
        print("Set it before running this script.")
        return

    with app.app_context():
        # Check if admin user already exists
        existing_admin = User.query.filter_by(email='0430333416').first()
        
        if existing_admin:
            print("Admin user already exists. Updating password...")
            existing_admin.set_password(admin_password)
            existing_admin.is_admin = True
            db.session.commit()
            print("✓ Admin user updated successfully!")
        else:
            # Create new admin user
            admin = User(
                email='0430333416',
                name='Administrator',
                is_admin=True
            )
            admin.set_password(admin_password)
            
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created successfully!")
        
        print(f"\nAdmin Login Credentials:")
        print(f"Username: 0430333416")
        print(f"Password: [value from ADMIN_BOOTSTRAP_PASSWORD]")
        print(f"\nAccess the admin panel at: http://localhost:5001")

if __name__ == '__main__':
    create_admin()
