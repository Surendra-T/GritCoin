import os
from datetime import timedelta

class Config:
    """
    Configuration class for Flask application.
    Centralizes all configuration variables for security and maintainability.
    """
    
    # Secret key for session management and CSRF protection
    # In production, this should be set via environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    # SQLite database file will be created in the project root
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
    
    # Disable SQLAlchemy modification tracking (saves resources)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    # Sessions expire after 7 days of inactivity
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Security headers
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript access to session cookie
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    
    # Maximum number of users allowed (demo limitation)
    MAX_USERS = 5
    
    # Application settings
    DEBUG = True  # Set to False in production
