from flask import flash, redirect, url_for, request, render_template
from flask_login import login_required, current_user, login_user, logout_user
from ..forms import LoginForm
from ..database import login_auth
from . import user_bp


@user_bp.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_active:
        flash("You have logined.", category="info")
        return redirect(url_for("user.dashboard_page"))
    else:
        form = LoginForm()
        if request.method == "GET":
            return render_template("login.html", form=form)
        if request.method == "POST":
            if form.validate_on_submit():
                username = form.username.data
                password = form.password.data
                if user := login_auth(username, password):
                    login_user(user)
                    flash(f"Login as {username}!", category="success")
                    return redirect(url_for("user.dashboard_page"))
                else:
                    flash("Wrong username or password.", category="alert")
                    return redirect(url_for("user.login_page"))
            else:
                for _, errors in form.errors.items():
                    for error in errors:
                        flash(error, category="alert")
                return redirect(url_for("user.login_page"))


@user_bp.route("/logout", methods=["GET"])
def logout_page():
    logout_user()
    return redirect(url_for("main.index_page"))


@user_bp.route("/register", methods=["GET", "POST"])
def register_page():
    pass


@user_bp.route("/setting", methods=["GET", "POST"])
@login_required
def user_setting_page():
    pass


@user_bp.route("/post/add", methods=["GET", "POST"])
@login_required
def add_post_page():
    pass


@user_bp.route("/post/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post_page(post_id):
    pass


@user_bp.route("/post/delete/<int:post_id>", methods=["GET"])
@login_required
def delete_post_page(post_id):
    pass


@user_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard_page():
    pass


@user_bp.route("/comments", methods=["GET"])
@login_required
def comments_dashboard_page():
    pass


@user_bp.route("/posts", methods=["GET"])
@login_required
def all_posts_page():
    pass


@user_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def view_post_page(post_id):
    pass


@user_bp.route("/@<username>/posts", methods=["GET"])
@login_required
def user_posts_page(username):
    pass
