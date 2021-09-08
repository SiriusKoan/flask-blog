import unittest
from flask import url_for
from app import create_app
from app.database import db, add_user


class TestModel(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.user_data = {"username": "user", "password": "user"}
        self.admin_data = {"username": "admin", "password": "admin"}
        generate_test_data()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        if self.app_context is not None:
            self.app_context.pop()

    def user_login(self):
        return self.client.post(url_for("user.login_page"), data=self.user_data)

    def admin_login(self):
        return self.client.post(url_for("user.login_page"), data=self.admin_data)

    def login(self, login):
        if login == "user":
            self.user_login()
        if login == "admin":
            self.admin_login()

    def get(self, login=False):
        self.login(login)
        res = self.client.get(self.route, follow_redirects=True)
        return res

    def post(self, login=False, data=None):
        self.login(login)
        res = self.client.post(self.route, data=data, follow_redirects=True)
        return res


def generate_test_data():
    db.create_all()
    add_user("user", "user", "user@user.com")
    add_user("admin", "admin", "admin@admin.com", is_admin=True)
