from app.user_helper import admin_required
from app.database.helper import (
    add_user,
    delete_comment_admin,
    delete_post_admin,
    delete_user,
    get_all_users,
    update_user_data,
)
import datetime
from flask import (
    redirect,
    url_for,
    request,
    render_template,
    make_response,
    flash,
    abort,
)
from ..forms import AddUserForm, AdminDashboardFilter, UserFilterForm
from ..database import get_posts, get_all_comments
from . import admin_bp


@admin_bp.route("/admin_dashboard/posts", methods=["GET", "POST"])
@admin_required
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
@admin_required
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
        return render_template(
            "admin_dashboard_comments.html", comments=comments, form=form
        )
    if request.method == "POST":
        response = make_response(
            redirect(url_for("admin.admin_dashboard_comments_page"))
        )
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
@admin_required
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
    form_add_user = AddUserForm()
    if request.method == "GET":
        users = get_all_users(**filter_args)
        return render_template("manage_user.html", users=users, form=form)
    if request.method == "POST":
        response = make_response(redirect(url_for("admin.manage_user_page")))
        form_name = request.form["form_name"]
        if form_name == "add_user":
            if form_add_user.validate_on_submit():
                username = form_add_user.username.data
                password = form_add_user.password.data
                email = form_add_user.email.data
                is_admin = form_add_user.is_admin.data
                if add_user(username, password, email, is_admin=is_admin):
                    flash("OK.")
                else:
                    flash("Error.")
            else:
                for _, errors in form.errors.items():
                    for error in errors:
                        flash(error, category="alert")
        if form_name == "filter":
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
@admin_required
def admin_dashboard_posts_backend():
    data = request.get_json(force=True)
    post_id = data["post_id"]
    try:
        delete_post_admin(post_id)
        return "OK"
    except:
        abort(400)


@admin_bp.route("/admin_dashboard_comments_backend", methods=["DELETE"])
@admin_required
def admin_dashboard_comments_backend():
    data = request.get_json(force=True)
    comment_id = data["comment_id"]
    try:
        delete_comment_admin(comment_id)
        return "OK"
    except:
        abort(400)


@admin_bp.route("/manage_user_backend", methods=["PATCH", "DELETE"])
@admin_required
def manage_user_backend():
    if request.method == "PATCH":
        data = request.get_json(force=True)
        if (
            update_user_data(
                data["user_id"], email=data["email"], is_admin=data["is_admin"]
            )
            == True
        ):
            return "OK"
        else:
            abort(400)
    if request.method == "DELETE":
        data = request.get_json(force=True)
        user_id = data["user_id"]
        try:
            delete_user(user_id)
            return "OK"
        except:
            abort(400)
