from flask import Flask, render_template
import os
from dotenv import load_dotenv
from extensions import db, login_manager, migrate
from datetime import datetime
# Add this import at the top
from flask import redirect, url_for

# Load environment variables
load_dotenv()

# Initialize Flask app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///lab_management.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Add this line

    # Import models here to avoid circular imports
    from models.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    from controllers.auth import auth_bp
    from controllers.equipment import equipment_bp
    from controllers.scheduling import scheduling_bp
    from controllers.inventory import inventory_bp
    from controllers.safety import safety_bp
    from controllers.reports import reports_bp
    from controllers.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(equipment_bp, url_prefix='/equipment')  # Add url_prefix
    app.register_blueprint(scheduling_bp)
    app.register_blueprint(inventory_bp)  # Ensure no url_prefix if templates are in inventory subfolder
    app.register_blueprint(safety_bp)
    app.register_blueprint(reports_bp)
    # In the blueprint registration section
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    # Add root route redirect
    @app.route('/')
    def home():
        return redirect(url_for('dashboard.index'))

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
        
    # Add context processor
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)