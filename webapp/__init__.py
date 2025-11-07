from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    from webapp.models.models_file import User
    return User.query.get(int(user_id))


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
    login_manager.login_view = 'auth.login'  # type: ignore[assignment]
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    from .routes import auth, grades
    from .routes import dashboard, course
    from .models import models_file

    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(grades.grades_bp)
    app.register_blueprint(dashboard.dashboard_bp)
    app.register_blueprint(course.course_bp)

    from webapp.error_handler import register_error_handlers
    register_error_handlers(app)

    return app
