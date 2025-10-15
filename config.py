import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))
DEV_DB_PATH = f'sqlite:///{os.path.join(basedir, "data", "gradeshare_dev.db")}'
TEST_DB_PATH = 'sqlite:///:memory:'

class BaseConfig:
    """Base configuration across all environments."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = False
    JSON_SORT_KEYS = False


class DevelopmentConfig(BaseConfig):
    """Local development configuration."""
    SQLALCHEMY_DATABASE_URI = DEV_DB_PATH
    DEBUG = True


class TestingConfig(BaseConfig):
    """unit tests."""
    SQLALCHEMY_DATABASE_URI = TEST_DB_PATH
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):
    """Production config."""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://") #TODO: update with actual db url
    SESSION_COOKIE_SECURE = True
    DEBUG = False
