from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField, DateField, IntegerField
from wtforms.validators import (
    DataRequired,
    Length,
    EqualTo,
    Regexp,
    ValidationError,
    Optional,
)
from flask_pagedown.fields import PageDownField


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


class UserSettingForm(FlaskForm):
    password = PasswordField(
        "Password",
        render_kw={"placeholder": "Password"},
    )
    email = EmailField(
        "Email", validators=[DataRequired()], render_kw={"placeholder": "Email"}
    )
    submit = SubmitField("Update")

    def validate_password(self, field):
        if type(field.data) is str:
            if field.data != "" and len(field.data) < 6:
                raise ValidationError(
                    "The password must contain at least 6 characters."
                )
        else:
            raise ValidationError("Invalid type.")


class AddPostForm(FlaskForm):
    content = PageDownField("Enter your markdown")
    submit = SubmitField("Submit")


class AddCommentFrom(FlaskForm):
    content = StringField("Comment", render_kw={"placeholder": "Comment"})
    submit = SubmitField("Comment")


class AddUserForm(FlaskForm):
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
    email = EmailField(
        "Email", validators=[DataRequired()], render_kw={"placeholder": "Email"}
    )
    is_admin = BooleanField("The user is an admin")
    submit = SubmitField("Add")


class DashboardFilterForm(FlaskForm):
    start = DateField("start", format="%Y-%m-%d", validators=[DataRequired()])
    end = DateField("end", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AdminDashboardFilter(FlaskForm):
    start = DateField("start", format="%Y-%m-%d", validators=[Optional()])
    end = DateField("end", format="%Y-%m-%d", validators=[Optional()])
    user_id = IntegerField(
        "User ID", render_kw={"placeholder": "User ID"}, validators=[Optional()]
    )
    submit = SubmitField("Submit")

class UserFilterForm(FlaskForm):
    user_id = IntegerField(
        "User ID", render_kw={"placeholder": "User ID"}, validators=[Optional()]
    )
    username = StringField("Username", render_kw={"placeholder": "Username"})
    start = DateField("start", format="%Y-%m-%d", validators=[Optional()])
    end = DateField("end", format="%Y-%m-%d", validators=[Optional()])
    submit = SubmitField("Submit")