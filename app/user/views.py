from flask_login import login_required
from . import user_bp

@user_bp.route("/login", methods=["GET", "POST"])
def login_page():
    pass

@user_bp.route("/logout", methods=["GET"])
def logout_page():
    pass

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