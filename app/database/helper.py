from .models import db, Users
from ..user_helper import User


def init():
    db.create_all()


def reset():
    db.drop_all()
    db.create_all()


def add_user(username, password, email, introduction=None, is_admin=False):
    user = Users(username, password, email, introduction, is_admin)
    try:
        db.session.add(user)
        db.session.commit()
        return True
    except:
        return False

def login_auth(username, password):
    if user := Users.query.filter_by(username=username).first():
        if user.check_password(password):
            sessionUser = User()
            sessionUser.id = user.id
            return sessionUser
    return False