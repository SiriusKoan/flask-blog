from .models import db, Users


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
