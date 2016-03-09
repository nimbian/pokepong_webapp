from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired

class Register(Form):
    username = StringField(u'username', validators=[DataRequired()])
    password1 = PasswordField(u'password1', validators=[DataRequired()])
    password2 = PasswordField(u'password2', validators=[DataRequired()])

class Login(Form):
    username = StringField(u'username', validators=[DataRequired()])
    password = PasswordField(u'password', validators=[DataRequired()])

class PartySignup(Form):
    teamname = StringField(u'Teamname', validators=[DataRequired()])
    player1 = StringField(u'Player 1', validators=[DataRequired()])
    player2 = StringField(u'Player 2', validators=[DataRequired()])

class BattleSignup(Form):
    #should add a validator to check no more than 6 pokemon are selected
    pokemon = SelectMultipleField(u'pokemon', validators=[DataRequired()])

class ServerManage(Form):
    mode = SelectField(u'Mode', choices=[('battle', 'battle'), ('party', 'party')])

