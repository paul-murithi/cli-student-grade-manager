from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db, migrate
import os

login_manager = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object('config.ProductionConfig')
    elif env == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .routes import auth, grades

    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(grades.grades_bp)

    return app