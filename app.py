from flask import Flask, render_template
from flask_login import LoginManager
from models import db, User
from config import Config

# Import blueprints
from routes.auth import auth_bp
from routes.study import study_bp
from routes.expense import expense_bp
from routes.dashboard import dashboard_bp


def create_app(config_name='default'):
    """
    Application factory function.
    Creates and configures the Flask application.
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login if not authenticated
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        """
        Flask-Login user loader callback.
        Loads a user from the database given the user_id stored in the session.
        """
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(study_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(dashboard_bp)
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Home/Index route
    @app.route('/')
    def index():
        """Landing page for GritCoin."""
        return render_template('index.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 Not Found errors."""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors."""
        db.session.rollback()  # Rollback any failed database transactions
        return render_template('errors/500.html'), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)