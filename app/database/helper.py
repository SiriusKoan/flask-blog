from werkzeug.security import generate_password_hash
from .models import Comments, db, Users, Posts
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


def add_post(user_id, title, description, content):
    post = Posts(user_id, title, description, content)
    try:
        db.session.add(post)
        db.session.commit()
        return True
    except:
        return False


def edit_post(post_id, title, description, content):
    post = Posts.query.filter_by(id=post_id)
    try:
        data = {"title": title, "description": description, "content": content}
        post.update(data)
        db.session.commit()
        return True
    except:
        return False


def render_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    return {
        "id": post.id,
        "author_id": post.author_id,
        "title": post.title,
        "description": post.description,
        "content": post.content,
        "comments": [
            {
                "author_id": comment.author_id,
                "content": comment.content,
            }
            for comment in post.comments
        ],
    }


def get_posts(user_id=None, start=None, end=None):
    query = Posts.query
    if user_id:
        query = query.filter_by(author_id=user_id)
    if start:
        query = query.filter(Posts.time > start)
    if end:
        query = query.filter(Posts.time < end)
    posts = [post.id for post in query.all()]
    posts = list(map(render_post, posts))
    return posts


def delete_post(user_id, post_id):
    post = Posts.query.filter_by(id=post_id).first()
    if post.author_id == user_id:
        db.session.delete(post)
        comments = Comments.query.filter_by(post_id=post_id)
        for comment in comments:
            db.session.delete(comment)
        db.session.commit()
        return True
    else:
        return False


def get_user_by_username(username):
    user = Users.query.filter_by(username=username).first()
    return render_user_data(user.id)


def add_comment(user_id, post_id, content):
    comment = Comments(user_id, post_id, content)
    db.session.add(comment)
    db.session.commit()


def get_comments(post_id):
    comments = Comments.query.filter_by(post_id=post_id).all()
    return [
        {
            "id": comment.id,
            "author_id": comment.author_id,
            "post_id": comment.post_id,
            "content": comment.content,
        }
        for comment in comments
    ]


def get_user_comments(user_id):
    comments = Comments.query.filter_by(author_id=user_id).all()
    return [
        {
            "id": comment.id,
            "author_id": comment.author_id,
            "post_id": comment.post_id,
            "content": comment.content,
        }
        for comment in comments
    ]


def get_all_comments(user_id=None, start=None, end=None):
    query = Comments.query
    if user_id:
        query = query.filter_by(user_id)
    if start:
        query = query.filter(Comments.time > start)
    if end:
        query = query.filter(Comments.time < end)
    return [
        {
            "id": comment.id,
            "author_id": comment.author_id,
            "post_id": comment.post_id,
            "content": comment.content,
        }
        for comment in query.all()
    ]


def get_all_users(user_id=None, username=None, start=None, end=None):
    query = Users.query
    if user_id:
        query = query.filter_by(id=user_id)
    if username:
        query = query.filter_by(username=username)
    if start:
        query = query.filter(Users.register_time > start)
    if end:
        query = query.filter(Users.register_time < end)
    return user_to_dict(query.all())

def delete_post_admin(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    comments = Comments.query.filter_by(post_id=post_id).all()
    db.session.delete(post)
    for comment in comments:
        db.session.delete(comment)
    db.session.commit()
