from flask import Flask, render_template, redirect, request, jsonify, url_for, abort, flash
from flask.ext.login import current_user, login_user, logout_user, LoginManager, login_required
import json
from random import randrange
from pokepong.forms import Register, Login, PartySignup, BattleSignup, ServerManager
from pokepong.config import _cfg, _cfgi
from pokepong.models import Trainer, Pokemon
from pokepong.database import db
from pokepong.red import r

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(trainer_id):
    return Trainer.query.get(trainer_id)

@app.before_first_request
def init_redis():
    r.set('mode', 'party', nx=True)

@app.teardown_appcontext
def shutdown_session(dummy_exception=None):
    db.remove()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register", methods=['get', 'post'])
def register():
    form = Register()
    if form.validate_on_submit():
        trainer = Trainer.query.filter_by(username=form.username.data).first()
        if trainer:
            flash('Username already taken, please select another')
            return render_template('register.html', form=form)
        if form.password1.data != form.password2.data:
            flash('Your passwords did not match, please try again')
            return render_template('register.html', form=form)
        newuser = Trainer(form.username.data, form.password1.data)
        db.add(newuser)
        db.commit()
    return render_template('register.html', form=form)

@app.route("/login", methods=['get', 'post'])
def login():
    form = Login()
    if form.validate_on_submit():
        trainer = Trainer.query.filter_by(username=form.username.data).first()
        if not trainer:
            flash('Username not found or passwoord is incorrect')
            return render_template('login.html', form=form)
        elif not trainer.check_password(form.password.data):
            flash('Username not found or passwoord is incorrect')
            return render_template('login.html', form=form)
        login_user(trainer)
        redir = request.args.get('next')
        return redirect(redir or url_for('index'))
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/signup", methods=['get', 'post'])
def signup():
    mode = r.get('mode')
    form = PartySignup()
    form.pokemon.choices = [(pokemon.id, pokemon.name)
                            for pokemon in Pokemon.query.order_by('id').limit(151)]
    base = range(1, 151)
    if mode == 'party' and form.validate_on_submit():
        pokemon = form.pokemon.data
        while len(pokemon) < 6:
            pokemon.append(randrange(150) + 1)
        newteam = {'name' : form.teamname.data,
                   'player1': form.player1.data,
                   'player2': form.player2.data,
                   'pokemon': pokemon}
        r.rpush('lineup', json.dumps(newteam))
        return redirect(url_for('accepted'))
    elif mode == 'battle':
        return redirect(url_for('battle'))
    return render_template('party_signup.html', form=form, base=base)

@app.route("/battle", methods=['get', 'post'])
@login_required
def battle():
    mode = r.get('mode')
    if mode != 'battle':
        flash('game mode is currently set to party,\
if you want to battle please have an admin change it')
        return redirect(url_for('signup'))
    form = BattleSignup()
    form.pokemon.choices = [(pokemon.id, pokemon.name)
                            for pokemon in current_user.pokemon.order_by('id')]
    base = [p.base_id for p in current_user.pokemon.order_by('id')]
    if form.validate_on_submit():
        newteam = {'name' : current_user.name,
                   'pokemon': form.pokemon.data}
        r.rpush('lineup', json.dumps(newteam))
        return redirect(url_for('lineup'))
    return render_template('battle_signup.html', form=form, base=base)

@app.route("/admin", methods=['get', 'post'])
@login_required
def manage_server():
    if not current_user.admin:
        #401 unauthorized or you are not an admin page or something.
        abort(401)
    form = ServerManager()
    #TODO:Maybe let admin jump the line ;)
    if form.validate_on_submit():
        r.set('mode', form.mode.data)
        if form.purge.data:
            r.delete('lineup')
    return render_template('manage.html', form=form)

@app.route("/pokemon", methods=['get', 'post'])
@login_required
def view_pokemon():
    return render_template('pokemon.html', pokemon=current_user.pokemon)

@app.route("/lineup")
def lineup():
    teams = []
    mode = r.get('mode')
    if mode == 'party':
        for team in r.lrange('lineup', 0, -1):
            teams.append(json.loads(team))
        return render_template('party_lineup.html', teams=teams)
    elif mode == 'battle':
        for team in r.lrange('lineup', 0, -1):
            load = dict(json.loads(team))
            load['pokemon'] = [pokemon.base_id for pokemon in
                              Trainer.query.filter(Trainer.name==load['name']).one().pokemon]
            teams.append(load)
        return render_template('battle_lineup.html', teams=teams)

if __name__ == "__main__":
    app.secret_key = _cfg("secret-key")
    app.run(host=_cfg("debug-host"),
            port=_cfgi('debug-port'),
            debug=True)
