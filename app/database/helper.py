from werkzeug.security import generate_password_hash
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

def render_user_data(user_id):
    if user := Users.query.filter_by(id=user_id).first():
        return user_to_dict([user])[0]
    else:
        return False

def user_to_dict(user_objects: list):
    li = []
    for user in user_objects:
        d = dict()
        d["id"] = user.id
        d["username"] = user.username
        d["email"] = user.email
        d["is_admin"] = user.is_admin
        d["introduction"] = user.introduction
        d["register_time"] = user.register_time.strftime("%Y-%m-%d %H:%M:%S")
        li.append(d)
    return li

def update_user_data(user_id, password=None, email=None, is_admin=None):
    filter = Users.query.filter_by(id=user_id)
    if filter.first():
        data = {}
        if password:
            data["password"] = generate_password_hash(password)
        if email:
            data["email"] = email
        if is_admin != None:
            data["is_admin"] = is_admin
        try:
            filter.update(data)
            db.session.commit()
            return True
        except:
            return "Username or email is used."
    else:
        return "The user does not exist."