from app import create_app
from models.models import User, Role
from extensions import db

app = create_app()

with app.app_context():
    # Create tables
    db.create_all()
    
    # Create admin role - remove permissions parameter
    if not Role.query.filter_by(name='Admin').first():
        admin_role = Role(name='Admin')  # Removed permissions parameter
        db.session.add(admin_role)
        db.session.commit()

    # Create admin user - use role relationship instead of role_id
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@lab.com',
            first_name='Admin',
            last_name='User',
            role=admin_role  # Changed to use relationship
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")