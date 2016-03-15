from flask import Flask, render_template, redirect, request, jsonify, url_for, abort, flash
from flask.ext.login import current_user, login_user, logout_user, LoginManager, login_required
from time import sleep
from pokepong.forms import Register, Login, PartySignup, BattleSignup
from pokepong.models import Trainer
from pokepong.database import db
from pokepong.red import r
import sqlite3
import json
from random import randrange

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

@app.route("/")
def index():
    #TODO: make index template
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
            return render_template('login.html', form=form)
        elif not trainer.check_password(form.password.data):
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
    #TODO: move enums to Server model.
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
    return render_template('signup.html', form=form, base=base)

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
    print base
    if form.validate_on_submit():
        newteam = {'name' : current_user.username,
                   'pokemon': form.pokemon.data}
        r.rpush('lineup', json.dumps(newteam))
        return redirect(url_for('lineup'))
    return render_template('battle.html', form=form, base=base)

@app.route("/admin/manage", methods=['get', 'post'])
@login_required
def manage_server():
    if not current_user.admin:
        #401 unauthorized or you are not an admin page or something.
        abort(401)
    form = ServerManager()
    #TODO:should add a button to purge player queue
    #TODO:Maybe let admin jump the line ;)
    if form.validate_on_submit():
        Server.query.first().mode = form.mode.data
        db.commit()
    return render_template('manage.html', form=form)

@app.route("/manage/pokemon", methods=['get', 'post'])
@login_required
def manage_pokemon():
    pass

@app.route("/lineup")
def lineup():
    #TODO: make 2 template 1 for party and 1 for battle, battle should show
    #choosen pokemon instead of players.
    teams = []
    for team in r.lrange('lineup', 0, -1):
        teams.append(json.loads(team))
    return render_template('lineup.html', teams=teams)

if __name__ == "__main__":
    app.debug = True
    app.run(host='pokepong', port=80)
