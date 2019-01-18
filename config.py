import os
import datetime


class Config(object):
    """Common configuration."""

    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=60)
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development config"""
    DATABASE_URI = os.getenv('DATABASE_URI')
    DEBUG = True


class TestingConfig(Config):
    """Testing config"""

    TESTING = True
    DATABASE_URI = os.getenv('TEST_DATABASE_URI')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
