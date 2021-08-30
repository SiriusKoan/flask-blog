from os import getenv
import unittest
from flask_migrate import Migrate
from app import create_app, db
from app.database import init, reset, add_user

app = create_app(getenv("FLASK_ENV"))
migrate = Migrate(app, db, render_as_batch=True)


@app.shell_context_processor
def make_shell_context():
    return globals()


@app.cli.command(name="init_db")
def init_db():
    init()


@app.cli.command(name="reset_db")
def reset_db():
    reset()


@app.cli.command(name="create_user")
def create_user():
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    is_admin = True if input("Is admin or not (y or n): ") == "y" else False
    if add_user(username, password, email, None, is_admin):
        print("OK")
    else:
        print("Failed")


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
