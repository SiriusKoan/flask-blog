from . import admin_bp


@admin_bp.route("/admin_dashboard/posts", methods=["GET", "POST"])
def admin_dashboard_posts_page():
    pass


@admin_bp.route("/admin_dashboard/comments", methods=["GET", "POST"])
def admin_dashboard_comments_page():
    pass


@admin_bp.route("/manage_user", methods=["GET", "POST"])
def manage_user_page():
    pass


@admin_bp.route("/admin_dashboard_posts_backend", methods=["DELETE"])
def admin_dashboard_posts_backend():
    pass


@admin_bp.route("/admin_dashboard_comments_backend", methods=["DELETE"])
def admin_dashboard_comments_backend():
    pass


@admin_bp.route("/manage_user_backend", methods=["PATCH", "DELETE"])
def manage_user_backend():
    pass
