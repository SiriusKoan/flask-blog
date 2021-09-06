from flask import render_template, redirect, url_for
from werkzeug.exceptions import HTTPException
from . import main_bp


@main_bp.route("/", methods=["GET"])
def index_page():
    return render_template("index.html")


@main_bp.app_errorhandler(401)
def handler_401(e):
    return redirect(url_for("user.login_page"))


@main_bp.app_errorhandler(HTTPException)
def handler(e):
    return render_template("error.html", code=e.code, name=e.name), e.code
