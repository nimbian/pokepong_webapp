from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, widgets, BooleanField, RadioField
from wtforms.validators import DataRequired, ValidationError


class Register(Form):
    username = StringField(u'username', validators=[DataRequired()])
    password1 = PasswordField(u'password1', validators=[DataRequired()])
    password2 = PasswordField(u'password2', validators=[DataRequired()])
    pokemon = RadioField(u'pokemon',
                         choices=[(1, 1), (4, 4), (7, 7)],
                         validators=[DataRequired()],
                         coerce=int)


class Login(Form):
    username = StringField(u'username', validators=[DataRequired()])
    password = PasswordField(u'password', validators=[DataRequired()])


class PartySignup(Form):
    teamname = StringField(u'Teamname', validators=[DataRequired()])
    player1 = StringField(u'Player 1', validators=[DataRequired()])
    player2 = StringField(u'Player 2', validators=[DataRequired()])
    pokemon = SelectMultipleField(u'pokemon',
                                  coerce=int,
                                  option_widget=widgets.CheckboxInput())

    def validate_pokemon(self, field):
        if len(field.data) > 6:
            raise ValidationError('Choose 6 or fewer pokemon')


class BattleSignup(Form):
    pokemon = SelectMultipleField(u'pokemon',
                                  validators=[DataRequired()],
                                  coerce=int,
                                  option_widget=widgets.CheckboxInput())

    def validate_pokemon(self, field):
        if len(field.data) > 6:
            raise ValidationError('Choose 6 of fewer pokemon')


class ServerManager(Form):
    mode = SelectField(u'Game Mode', choices=[('', ''),
                                              ('pong', 'party'),
                                              ('battle', 'battle'),
                                              ('wild', 'campaign')])
    purge = BooleanField(u'Purge')
    admins = SelectMultipleField(u'admins',
                                 coerce=int,
                                 option_widget=widgets.CheckboxInput())
