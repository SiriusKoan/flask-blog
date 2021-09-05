from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_pagedown import PageDown
from flaskext.markdown import Markdown
from .database import db
from .config import configs

login_manager = LoginManager()
mail = Mail()
pagedown = PageDown()


def create_app(env):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(configs[env])

    login_manager.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    pagedown.init_app(app)
    Markdown(app)

    # Blueprint
    # from .main import main_bp

    # app.register_blueprint(main_bp)

    # from .user import user_bp

    # app.register_blueprint(user_bp)

    # from .admin import admin_bp

    # app.register_blueprint(admin_bp)

    return app
