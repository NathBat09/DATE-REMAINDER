from flask import Flask
from flask import request 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler

mail = Mail()
db = SQLAlchemy()
DB_NAME = "database.db"
scheduler = BackgroundScheduler()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'reminder.noreply987@gmail.com'  
    app.config['MAIL_PASSWORD'] = 'xinzheijwfhzgtfz' 
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    db.init_app(app)
    mail.init_app(app)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all()
        scheduler.start()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def safe_response(response):
        if not is_safe(response):
            raise ValueError('Response is not safe')
        return response

    @app.route('/', methods=['GET', 'POST'])
    @safe_response
    def index():
        if request.method == 'POST':
            # Do something with the request here
            return 'OK'
        else:
            return 'Hello, World!'

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


def is_safe(response):
    # Check if the response is safe according to the safety guidelines
    return True