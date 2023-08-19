# Import necessary modules and classes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler

# Create instances of Mail, SQLAlchemy, and BackgroundScheduler
mail = Mail()
db = SQLAlchemy()
scheduler = BackgroundScheduler()

# Define the database file name
DB_NAME = "database.db"

# Function to create the Flask app
def create_app():
    app = Flask(__name__)

    # Configure app settings
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'reminder.noreply987@gmail.com'
    app.config['MAIL_PASSWORD'] = 'xinzheijwfhzgtfz'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    # Initialize SQLAlchemy and Mail extensions
    db.init_app(app)
    mail.init_app(app)

    # Import and register blueprints for views and auth
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import User and Note models and create database tables
    from .models import User, Note
    with app.app_context():
        db.create_all()  # Create database tables
        scheduler.start()  # Start the scheduler

    # Initialize LoginManager for user authentication
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Load the user for the current session
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# Function to create the database if it doesn't exist
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')