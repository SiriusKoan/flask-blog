import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    introduction = db.Column(db.String)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    register_time = db.Column(
        db.DateTime, default=datetime.datetime.now, nullable=False
    )
    posts = db.relationship("Posts")
    comments = db.relationship("Comments")

    def __init__(self, username, password, email, introduction=None, is_admin=False):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.introduction = introduction
        self.is_admin = is_admin

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Posts(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)
    content = db.Column(db.String, nullable=False)
    comments = db.relationship("Comments")

    def __init__(self, author_id, title, description, content):
        self.author_id = author_id
        self.title = title
        self.description = description
        self.content = content


class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    content = db.Column(db.String, nullable=False)

    def __init__(self, author_id, post_id, content):
        self.author_id = author_id
        self.post_id = post_id
        self.content = content
