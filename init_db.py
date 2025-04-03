from app import app, db
from models.models import Role, User
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if roles already exist
        if Role.query.count() == 0:
            # Create roles
            roles = [
                Role(name='Administrator'),
                Role(name='Lab Manager'),
                Role(name='Instructor'),
                Role(name='Student'),
                Role(name='Lab Assistant')
            ]
            db.session.add_all(roles)
            db.session.commit()
            print("Roles created successfully!")
        
        # Check if admin user exists
        if User.query.filter_by(username='admin').first() is None:
            # Create admin user
            admin_role = Role.query.filter_by(name='Administrator').first()
            admin_user = User(
                username='admin',
                email='admin@example.com',
                first_name='Admin',
                last_name='User',
                role_id=admin_role.id
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully!")
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()