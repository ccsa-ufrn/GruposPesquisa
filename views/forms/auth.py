"""
Forms about content editing.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """
    Sign in form.
    """
    nick = StringField('Usuário', validators=[
        DataRequired('Digite o seu usuário.')
    ])
    password = PasswordField('Senha', validators=[
        DataRequired('Digite sua senha.')
    ])

class NickForm(FlaskForm):
    """
    Request email password reset form
    """
    nick = StringField('Usuário', validators=[
        DataRequired('Digite o seu usuário.')
    ])

class ResetPasswordForm(FlaskForm):
    """
    New password form
    """

    password_one = PasswordField('Digite a senha nova', validators=[
        DataRequired('Digite sua senha.')
    ])

    password_two = PasswordField('Digite novamente', validators=[
        DataRequired('Digite sua senha.')
    ])

    key = StringField('Key escondida', validators=[
        DataRequired('Digite o seu usuário.')
    ])
