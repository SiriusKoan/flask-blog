import unittest
from flask import url_for
from app import create_app


class BasicTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self) -> None:
        if self.app_context:
            self.app_context.pop()

    def test_app_is_alive(self):
        response = self.client.get(url_for("main.index_page"))
        self.assertEqual(response.status_code, 200)

    def test_blueprint(self):
        self.assertNotEqual(self.app.blueprints.get("main", None), None)
        self.assertNotEqual(self.app.blueprints.get("user", None), None)
        self.assertNotEqual(self.app.blueprints.get("admin", None), None)
