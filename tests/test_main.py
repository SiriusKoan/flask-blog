from flask import url_for
from tests.helper import TestModel


class IndexPageTest(TestModel):
    def setUp(self) -> None:
        super().setUp()
        self.route = url_for("main.index_page")

    def test_get_with_no_auth(self):
        res = self.get()
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Login", res.data)

    def test_get_with_auth(self):
        res = self.get(login="user")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Dashboard", res.data)
