from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired()], render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw={"placeholder": "Password"}
    )
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=4, max=30, message="The name should be 4 to 30 letters long."),
            Regexp(
                "[a-zA-Z0-9_]+",
                message="Only letters, numbers and underscore are allowed in username.",
            ),
        ],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, message="The password must contain at least 6 characters."),
        ],
        render_kw={"placeholder": "Password"},
    )
    repeat_password = PasswordField(
        "Repeat Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords not match."),
        ],
        render_kw={"placeholder": "Repeat Password"},
    )
    email = EmailField(
        "Email", validators=[DataRequired()], render_kw={"placeholder": "Email"}
    )
    submit = SubmitField("Register")
