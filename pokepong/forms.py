from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, widgets, BooleanField
from wtforms.validators import DataRequired, ValidationError


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

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
    pokemon = MultiCheckboxField(u'pokemon', coerce=int)

    def validate_pokemon(self, field):
        if len(field.data) != 6:
            raise ValidationError('Choose 6 pokemon')

class BattleSignup(Form):
    #should add a validator to check no more than 6 pokemon are selected
    pokemon = MultiCheckboxField(u'pokemon', validators=[DataRequired()], coerce=int)

    def validate_pokemon(self, field):
        if len(field.data) != 6:
            raise ValidationError('Choose 6 pokemon')

class ServerManager(Form):
    mode = SelectField(u'Game Mode', choices=[('party', 'party'),
                                              ('battle', 'battle')])
    purge = BooleanField(u'Purge')
