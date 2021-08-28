from os import getenv, urandom


class Config:
    # Flask-Mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = getenv("MAIL_USERNAME")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD")
    # Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Testing(Config):
    # Flask
    ENV = "TESTING"
    TESTING = True
    SECRET_KEY = "cyn54g544mxng"
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    # Flask-WTF
    WTF_CSRF_ENABLED = False


class Development(Config):
    # Flask
    ENV = "DEVELOPMENT"
    DEBUG = True
    SECRET_KEY = "cyn54g544mxng"
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"


class Production(Config):
    # Flask
    ENV = "PRODUCTION"
    SECRET_KEY = urandom(32)
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")


configs = {
    "development": Development,
    "testing": Testing,
    "production": Production,
}
