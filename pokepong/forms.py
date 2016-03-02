from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class Register(Form):
    username = StringField('username', validators=[DataRequired()])
    password1 = PasswordField('password1', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired()])

