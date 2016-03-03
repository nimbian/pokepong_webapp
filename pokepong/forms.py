from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired

class Register(Form):
    username = StringField('username', validators=[DataRequired()])
    password1 = PasswordField('password1', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired()])

class Login(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class PartySignup(Form):
    teamname = StringField('teamname', validators=[DataRequired()])

class BattleSignup(Form):
    teamname = SelectField('teamname', validators=[DataRequired()])

