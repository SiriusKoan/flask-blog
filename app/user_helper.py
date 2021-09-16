from functools import wraps
from flask import current_app, request, abort, flash, redirect, session
from flask_login import LoginManager, UserMixin, current_user
from flask_login.config import USE_SESSION_FOR_NEXT
from flask_login.signals import user_unauthorized
from flask_login.utils import (
    expand_login_view,
    login_url as make_login_url,
    make_next_param,
)
from .database.models import Users


class User(UserMixin):
    pass


class LoginManager_(LoginManager):
    def __init__(self):
        super().__init__()

    def forbidden(self):
        user_unauthorized.send(current_app._get_current_object())

        if self.unauthorized_callback:
            return self.unauthorized_callback()

        if request.blueprint in self.blueprint_login_views:
            login_view = self.blueprint_login_views[request.blueprint]
        else:
            login_view = self.login_view

        if not login_view:
            abort(403)

        if self.login_message:
            if self.localize_callback is not None:
                flash(
                    self.localize_callback(self.login_message),
                    category=self.login_message_category,
                )
            else:
                flash(self.login_message, category=self.login_message_category)

        config = current_app.config
        if config.get("USE_SESSION_FOR_NEXT", USE_SESSION_FOR_NEXT):
            login_url = expand_login_view(login_view)
            session["_id"] = self._session_identifier_generator()
            session["next"] = make_next_param(login_url, request.url)
            redirect_url = make_login_url(login_view)
        else:
            redirect_url = make_login_url(login_view, next_url=request.url)

        return redirect(redirect_url)


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_active:
            if current_user.is_admin:
                return func(*args, **kwargs)
            else:
                return login_manager.forbidden()
        else:
            return login_manager.unauthorized()

    return decorated_view


login_manager = LoginManager_()


@login_manager.user_loader
def load(user_id):
    user_id = int(user_id)
    user = Users.query.filter_by(id=user_id).first()
    if user:
        sessionUser = User()
        sessionUser.id = user.id
        sessionUser.is_admin = user.is_admin
        return sessionUser
    else:
        return None
