from app.database.helper import add_comment, get_comments, get_user_by_username, get_user_comments
import datetime
from flask import flash, redirect, url_for, request, render_template, make_response
from flask_login import login_required, current_user, login_user, logout_user
from ..forms import (
    DashboardFilterForm,
    LoginForm,
    RegisterForm,
    UserSettingForm,
    AddPostForm,
    AddCommentForm,
)
from ..database import (
    login_auth,
    add_user,
    render_user_data,
    update_user_data,
    add_post,
    edit_post,
    render_post,
    get_posts,
    delete_post,
)
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
    if current_user.is_active:
        flash("You have logined.", category="info")
        return redirect(url_for("user.dashboard_page"))
    else:
        form = RegisterForm()
        if request.method == "GET":
            return render_template("register.html", form=form)
        if request.method == "POST":
            if form.validate_on_submit():
                username = form.username.data
                password = form.password.data
                email = form.email.data
                if add_user(username, password, email):
                    flash("Register successfully.", category="success")
                    return redirect(url_for("user.login_page"))
                else:
                    flash("The username or the email has been used.", category="alert")
                    return redirect(url_for("user.register_page"))
            else:
                for _, errors in form.errors.items():
                    for error in errors:
                        flash(error, category="alert")
                return redirect(url_for("user.register_page"))


@user_bp.route("/setting", methods=["GET", "POST"])
@login_required
def user_setting_page():
    data = render_user_data(current_user.id)
    form = UserSettingForm(email=data["email"])
    if request.method == "GET":
        return render_template("user_setting.html", form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            password = form.password.data
            email = form.email.data
            if (
                msg := update_user_data(current_user.id, password=password, email=email)
            ) == True:
                flash("OK.", category="success")
            else:
                flash(msg, category="alert")
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
        return redirect(url_for("user.setting_page"))


@user_bp.route("/post/add", methods=["GET", "POST"])
@login_required
def add_post_page():
    form = AddPostForm()
    if request.method == "GET":
        return render_template("write.html", form=form, route="/post/add")
    if request.method == "POST":
        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data
            content = form.content.data
            if add_post(current_user.id, title, description, content):
                flash("Add post.")
                return redirect(url_for("user.dashboard_page"))
            else:
                flash("The title has been used.")
                return redirect(url_for("user.add_post_page"))
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
            return redirect(url_for("user.add_post_page"))


@user_bp.route("/post/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post_page(post_id):
    post_data = render_post(post_id)
    form = AddPostForm(
        title=post_data["title"],
        description=post_data["description"],
        content=post_data["content"],
    )
    if request.method == "GET":
        return render_template("write.html", form=form, route=f"/post/edit/{post_id}")
    if request.method == "POST":
        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data
            content = form.content.data
            if edit_post(post_id, title, description, content):
                flash("Post edited.")
                return redirect(url_for("user.dashboard_page"))
            else:
                flash("The title has been used.")
                return redirect(url_for("user.edit_post_page", post_id=post_id))
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
            return redirect(url_for("user.edit_post_page", post_id=post_id))


@user_bp.route("/post/delete/<int:post_id>", methods=["GET"])
@login_required
def delete_post_page(post_id):
    if delete_post(current_user.id, post_id):
        flash("OK.")
    else:
        flash("Failed.")
    return redirect(url_for("user.dashboard"))


@user_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard_page():
    filter_args = {}
    if start := request.cookies.get("start"):
        filter_args["start"] = datetime.datetime.strptime(start, "%Y-%m-%d")
    if end := request.cookies.get("end"):
        filter_args["end"] = datetime.datetime.strptime(end, "%Y-%m-%d")
    form = DashboardFilterForm(**filter_args)
    if request.method == "GET":
        posts = get_posts(user_id=None, **filter_args)
        return render_template("dashboard.html", posts=posts, form=form)
    if request.method == "POST":
        response = make_response(redirect(url_for("user.dashboard_page")))
        if form.validate_on_submit():
            cookies = []
            if form.start.data:
                cookies.append(("start", form.start.data.strftime("%Y-%m-%d")))
            if form.end.data:
                cookies.append(("end", form.end.data.strftime("%Y-%m-%d")))
            response.delete_cookie("start")
            response.delete_cookie("end")
            for cookie in cookies:
                response.set_cookie(*cookie)
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
        return response


@user_bp.route("/comments", methods=["GET"])
@login_required
def comments_dashboard_page():
    comments = get_user_comments(current_user.id)
    return render_template("comments.html", comments=comments)


@user_bp.route("/posts", methods=["GET"])
@login_required
def all_posts_page():
    posts = get_posts()
    return render_template("posts.html", posts=posts)



@user_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def view_post_page(post_id):
    form = AddCommentForm()
    if request.method == "GET":
        post = render_post(post_id)
        comments = get_comments(post_id)
        return render_template("post.html", post=post, comments=comments, form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            add_comment(current_user.id, post_id, form.content.data)
            flash("Comment added.")
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
        return redirect(url_for("user.view_post_page", post_id=post_id))



@user_bp.route("/@<username>/posts", methods=["GET"])
@login_required
def user_posts_page(username):
    user = get_user_by_username(username)
    posts = get_posts(user["id"])
    return render_template("posts.html", posts=posts)
