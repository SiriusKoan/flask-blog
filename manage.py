from os import getenv
from app import create_app, db
from app.database import init, reset, add_user

app = create_app(getenv("FLASK_ENV"))


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
