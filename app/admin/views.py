from app.database.helper import delete_post_admin, get_all_users
import datetime
from flask import redirect, url_for, request, render_template, make_response, flash, abort
from ..forms import AdminDashboardFilter, UserFilterForm
from ..database import get_posts, get_all_comments
from . import admin_bp


@admin_bp.route("/admin_dashboard/posts", methods=["GET", "POST"])
def admin_dashboard_posts_page():
    filter_args = {}
    if start := request.cookies.get("start"):
        filter_args["start"] = datetime.datetime.strptime(start, "%Y-%m-%d")
    if end := request.cookies.get("end"):
        filter_args["end"] = datetime.datetime.strptime(end, "%Y-%m-%d")
    if user_id := request.cookies.get("user_id"):
        filter_args["user_id"] = user_id
    form = AdminDashboardFilter(**filter_args)
    if request.method == "GET":
        posts = get_posts(**filter_args)
        return render_template("admin_dashboard_posts.html", posts=posts, form=form)
    if request.method == "POST":
        response = make_response(redirect(url_for("admin.admin_dashboard_posts_page")))
        if form.validate_on_submit():
            cookies = []
            if form.start.data:
                cookies.append(("start", form.start.data.strftime("%Y-%m-%d")))
            if form.end.data:
                cookies.append(("end", form.end.data.strftime("%Y-%m-%d")))
            if form.user_id.data:
                cookies.append(("user_id", str(form.user_id.data)))
            response.delete_cookie("start")
            response.delete_cookie("end")
            response.delete_cookie("user_id")
            for cookie in cookies:
                response.set_cookie(*cookie)
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
        return response


@admin_bp.route("/admin_dashboard/comments", methods=["GET"])
def admin_dashboard_comments_page():
    filter_args = {}
    if start := request.cookies.get("start"):
        filter_args["start"] = datetime.datetime.strptime(start, "%Y-%m-%d")
    if end := request.cookies.get("end"):
        filter_args["end"] = datetime.datetime.strptime(end, "%Y-%m-%d")
    if user_id := request.cookies.get("user_id"):
        filter_args["user_id"] = user_id
    form = AdminDashboardFilter(**filter_args)
    if request.method == "GET":
        comments = get_all_comments(**filter_args)
        return render_template("admin_dashboard_comments.html", comments=comments, form=form)
    if request.method == "POST":
        response = make_response(redirect(url_for("admin.admin_dashboard_comments_page")))
        if form.validate_on_submit():
            cookies = []
            if form.start.data:
                cookies.append(("start", form.start.data.strftime("%Y-%m-%d")))
            if form.end.data:
                cookies.append(("end", form.end.data.strftime("%Y-%m-%d")))
            if form.user_id.data:
                cookies.append(("user_id", str(form.user_id.data)))
            response.delete_cookie("start")
            response.delete_cookie("end")
            response.delete_cookie("user_id")
            for cookie in cookies:
                response.set_cookie(*cookie)
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
        return response


@admin_bp.route("/manage_user", methods=["GET", "POST"])
def manage_user_page():
    filter_args = {}
    if start := request.cookies.get("start"):
        filter_args["start"] = datetime.datetime.strptime(start, "%Y-%m-%d")
    if end := request.cookies.get("end"):
        filter_args["end"] = datetime.datetime.strptime(end, "%Y-%m-%d")
    if user_id := request.cookies.get("user_id"):
        filter_args["user_id"] = user_id
    if username := request.cookies.get("username"):
        filter_args["username"] = username
    form = UserFilterForm(**filter_args)
    if request.method == "GET":
        users = get_all_users(**filter_args)
        return render_template("manage_user.html", users=users, form=form)
    if request.method == "POST":
        response = make_response(redirect(url_for("admin.manage_user_page")))
        if form.validate_on_submit():
            cookies = []
            if form.start.data:
                cookies.append(("start", form.start.data.strftime("%Y-%m-%d")))
            if form.end.data:
                cookies.append(("end", form.end.data.strftime("%Y-%m-%d")))
            if form.user_id.data:
                cookies.append(("user_id", str(form.user_id.data)))
            if form.username.data:
                cookies.append(("username", form.username.data))
            response.delete_cookie("start")
            response.delete_cookie("end")
            response.delete_cookie("user_id")
            response.delete_cookie("username")
            for cookie in cookies:
                response.set_cookie(*cookie)
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
        return response


@admin_bp.route("/admin_dashboard_posts_backend", methods=["DELETE"])
def admin_dashboard_posts_backend():
    data = request.get_json(force=True)
    post_id = data["post_id"]
    try:
        delete_post_admin(post_id)
        return "OK"
    except:
        abort(400)


@admin_bp.route("/admin_dashboard_comments_backend", methods=["DELETE"])
def admin_dashboard_comments_backend():
    pass


@admin_bp.route("/manage_user_backend", methods=["PATCH", "DELETE"])
def manage_user_backend():
    pass
