import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAX_CONTENT_LENGTH = 1024 * 1024
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_NAME = 'SERVERDEV'
    SQLALCHEMY_DATABASE_HOST = 'localhost'
    SQLALCHEMY_DATABASE_USER = 'root'
    SQLALCHEMY_DATABASE_PAWD = 'database##^^(('


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_NAME = 'SERVERTEST'
    SQLALCHEMY_DATABASE_HOST = 'localhost'
    SQLALCHEMY_DATABASE_USER = 'root'
    SQLALCHEMY_DATABASE_PAWD = 'database##^^(('


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_NAME = 'SERVER'
    SQLALCHEMY_DATABASE_HOST = 'localhost'
    SQLALCHEMY_DATABASE_USER = 'root'
    SQLALCHEMY_DATABASE_PAWD = 'database##^^(('


config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }
