from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# db
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)

    # config
    app.config['SECRET_KEY'] = 'secret_key_123'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # views
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # models
    from .models import User, Post, Comment, Like

    create_database(app)

    # login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists(f'website/{DB_NAME}'):
        db.create_all(app=app)
        print('Database Created!')