# /home/paul/gradeshare/webapp/models/__init__.py
"""
This package contains database models for the Gradeshare web application.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()