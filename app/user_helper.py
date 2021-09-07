from flask_login import LoginManager, UserMixin
from .database.models import Users


class User(UserMixin):
    pass


login_manager = LoginManager()


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
