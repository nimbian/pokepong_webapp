from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, widgets, BooleanField, RadioField, IntegerField
from wtforms.validators import DataRequired, ValidationError, NumberRange, optional
from red import r


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
        if len(field.data) > r.get('max_count'):
            raise ValidationError('Choose {0} of fewer pokemon'.format(r.get('max_count')))


class ServerManager(Form):
    mode = SelectField(u'Game Mode', choices=[('', ''),
                                              ('pong', 'party'),
                                              ('battle', 'battle'),
                                              ('wild', 'campaign')])
    purge = BooleanField(u'Purge')
    max_level = IntegerField('Max Level', [NumberRange(min=0, max=100), optional()])
    min_level = IntegerField('Min Level', [NumberRange(min=0, max=100), optional()])
    max_count = SelectField(u'Max pkmn count', choices=[('6','6'),('5','5'),('4','4'),
                                                        ('3','3'),('2','2'),('1','1')])
    admins = SelectMultipleField(u'admins',
                                 coerce=int,
                                 option_widget=widgets.CheckboxInput())
class Release(Form):
    pass
