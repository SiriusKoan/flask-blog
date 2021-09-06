from werkzeug.exceptions import HTTPException
from . import main_bp


@main_bp.route("/", methods=["GET"])
def index_page():
    pass


@main_bp.app_errorhandler(401)
def handler_401(e):
    pass


@main_bp.app_errorhandler(HTTPException)
def handler(e):
    pass
