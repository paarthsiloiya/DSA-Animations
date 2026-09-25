from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import pathlib
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('DSA_SECRET_KEY', 'dev-only-insecure-key')
    os.makedirs(app.instance_path, exist_ok=True)
    db_path = pathlib.Path(app.instance_path, DB_NAME).as_posix()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    loginManager = LoginManager()
    loginManager.login_view = 'auth.login'
    loginManager.init_app(app)

    @loginManager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app : Flask):
    db_path = pathlib.Path(app.instance_path, DB_NAME)
    if not db_path.exists():
        with app.app_context():
            db.create_all()