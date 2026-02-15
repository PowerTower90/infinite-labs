"""
Script to create an admin user for the admin panel
"""
from app import app, db, User

def create_admin():
    with app.app_context():
        # Check if admin user already exists
        existing_admin = User.query.filter_by(email='0430333416').first()
        
        if existing_admin:
            print("Admin user already exists. Updating password...")
            existing_admin.set_password('Soso079979462000')
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
            admin.set_password('Soso079979462000')
            
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created successfully!")
        
        print(f"\nAdmin Login Credentials:")
        print(f"Username: 0430333416")
        print(f"Password: Soso079979462000")
        print(f"\nAccess the admin panel at: http://localhost:5001")

if __name__ == '__main__':
    create_admin()
