import json
from random import randrange
from flask import (render_template,
                   redirect, request,
                   url_for,
                   abort,
                   flash,
                   Blueprint,
                   current_app)
from flask.ext.login import (current_user,
                             login_user,
                             logout_user,
                             login_required)
from pokeweb.forms import (Register,
                            Login,
                            PartySignup,
                            BattleSignup,
                            ServerManager)

from pokeweb.models import Trainer, Pokemon, Owned, Caught
from pokeweb.database import db
from pokeweb.red import r

pokeweb = Blueprint('pokeweb', __name__,
                     template_folder='templates',
                     static_folder='static')


@current_app.login_manager.user_loader
def load_user(trainer_id):
    '''Rehadrate the the user-session bassed on the id from cookie'''
    return Trainer.query.get(trainer_id)


@current_app.before_first_request
def init_redis():
    '''Set the mode to party when the app starts if not already set'''
    r.set('mode', 'party', nx=True)


@current_app.teardown_appcontext
def shutdown_session(dummy_exception=None):
    '''Teardown the db session after every request to reset it'''
    db.remove()


@pokeweb.route("/")
def index():
    '''simple index landing page'''
    return render_template('index.html')


@pokeweb.route("/register", methods=['get', 'post'])
def register():
    '''Regester the user'''
    form = Register()
    if form.validate_on_submit():
        trainer = Trainer.query.filter_by(name=form.username.data).first()
        if trainer:
            flash('Username already taken, please select another')
            return render_template('register.html', form=form)
        if form.password1.data != form.password2.data:
            flash('Your passwords did not match, please try again')
            return render_template('register.html', form=form)
        trainer = Trainer(form.username.data, form.password1.data)
        if Trainer.query.first() is None:
            trainer.admin = True
            flash('Congradulations as the first registered trainer, you are \
an admin of the site')
        owned = Owned(form.pokemon.data)
        caught = Caught(trainer, form.pokemon.data)
        caught.caught = True
        trainer.pokemon.append(owned)
        db.add(trainer)
        db.add(caught)
        db.add(owned)
        db.commit()
        flash('Welcome {}'.format(trainer.name))
        return redirect(url_for('.index'))
    return render_template('register.html', form=form)


@pokeweb.route("/login", methods=['get', 'post'])
def login():
    '''Login the user'''
    form = Login()
    if form.validate_on_submit():
        trainer = Trainer.query.filter_by(name=form.username.data).first()
        if not trainer:
            flash('Username not found or passwoord is incorrect')
            return render_template('login.html', form=form)
        elif not trainer.check_password(form.password.data):
            flash('Username not found or passwoord is incorrect')
            return render_template('login.html', form=form)
        login_user(trainer)
        flash('You were logged in')
        redir = request.args.get('next')
        return redirect(redir or url_for('.index'))
    return render_template('login.html', form=form)


@pokeweb.route("/logout")
@login_required
def logout():
    '''log user out and teardown the cookies'''
    logout_user()
    flash('You were logged out')
    return redirect(url_for('.login'))


@pokeweb.route("/signup", methods=['get', 'post'])
def signup():
    '''signup for a new party battle or redirect user if in battle mode'''
    mode = r.get('mode')
    if mode == 'battle':
        flash('game mode is currently set to battle, \
if you want to party please have an admin change it')
        return redirect(url_for('.battle'))
    form = PartySignup()
    form.pokemon.choices = [(pokemon.id, pokemon.name)
                            for pokemon in Pokemon.query.order_by(
                                Pokemon.id).limit(151)]
    if form.validate_on_submit():
        pokemon = form.pokemon.data
        while len(pokemon) < 6:
            pokemon.append(randrange(150) + 1)
        newteam = {'name': form.teamname.data,
                   'player1': form.player1.data,
                   'player2': form.player2.data,
                   'pokemon': pokemon}
        r.rpush('lineup', json.dumps(newteam))
        return redirect(url_for('.lineup'))
    return render_template('party_signup.html', form=form)


@pokeweb.route("/battle", methods=['get', 'post'])
@login_required
def battle():
    '''register for a new battle or warn user if set to party'''
    mode = r.get('mode')
    if mode != 'battle':
        flash('game mode is currently set to party, \
if you want to battle please have an admin change it')
        return redirect(url_for('.signup'))
    form = BattleSignup()
    form.pokemon.choices = [(pokemon.id, pokemon.name)
                            for pokemon in current_user.pokemon]
    base = [p.base_id for p in current_user.pokemon]
    if form.validate_on_submit():
        newteam = {'name': current_user.name,
                   'pokemon': form.pokemon.data}
        r.rpush('lineup', json.dumps(newteam))
        return redirect(url_for('.lineup'))
    return render_template('battle_signup.html', form=form, base=base)


@pokeweb.route("/admin", methods=['get', 'post'])
@login_required
def admin():
    '''simple admin page'''
    if not current_user.admin:
        abort(401)
    form = ServerManager()
    # TODO:Maybe let admin jump the line ;)
    # TODO:Way to make users admins
    if form.validate_on_submit():
        if form.mode.data != '':
            r.set('mode', form.mode.data)
            r.delete('lineup')
        if form.purge.data:
            r.delete('lineup')
    form.admins.data = []
    form.admins.choices = []
    for trainer in Trainer.query.all():
        if trainer:
            form.admins.data.append(True)
        else:
            form.admins.data.append(False)
        form.admins.choices.append((trainer.id, trainer.name))
    return render_template('manage.html', form=form)


@pokeweb.route("/pokemon", methods=['get', 'post'])
@login_required
def view_pokemon():
    return render_template('pokemon.html', pokemon=current_user.pokemon)


@pokeweb.route("/lineup")
def lineup():
    teams = []
    mode = r.get('mode')
    if mode == 'party':
        teams = [json.loads(x) for x in r.lrange('lineup', 0, -1)]
        if len(teams) == 0:
            flash('nobody is queued up')
        return render_template('party_lineup.html', teams=teams)
    elif mode == 'battle':
        for team in r.lrange('lineup', 0, -1):
            load = dict(json.loads(team))
            load['pokemon'] = [pokemon.base_id for pokemon in
                               Owned.query.filter(
                                   Owned.id.in_(load['pokemon']))]
            teams.append(load)
        if len(teams) == 0:
            flash('nobody is queued up')
        return render_template('battle_lineup.html', teams=teams)
