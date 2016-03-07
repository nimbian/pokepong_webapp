from flask import Flask, render_template, redirect, request, jsonify, url_for
from flask.ext.login import current_user, login_user, logout_user, LoginManager, login_required
from time import sleep
from pokepong.forms import Register, Login, PartySignup, BattleSignup
from pokepong.models import Trainer
from pokepong.database import db
from pokepong.redis import r
import sqlite3
conn = sqlite3.connect('teams.db')
c = conn.cursor()
try:
    c.execute("""CREATE TABLE teams \
                    (name text, pkmn1 integer, pkmn2 integer, pkmn3 integer, \
                    pkmn4 integer, pkmn5 integer, pkmn6 integer)""")
except:
    pass
c.close()
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(trainer_id):
     return Trainer.get(trainer_id)


@app.route("/")
def master():
    return render_template('master.html')

@app.route("/home")
def homepage():
    return render_template('pkmn.html')

@app.route('/<name>/<pkmn>')
def submit(name, pkmn):
    conn = sqlite3.connect('teams.db')
    c = conn.cursor()
    sub = "INSERT INTO teams values ('{0}',{1},{2},{3},{4},{5},{6})".format(name, *pkmn.split(','))
    c.execute(sub)
    conn.commit()
    c.close()
    conn.close()
    return redirect("/redirect")

@app.route("/checkUser", methods=['GET'])
def check_user():
    team = request.args.get('team')
    conn = sqlite3.connect('teams.db')
    c = conn.cursor()
    sub = "select name from teams where name = '{0}'".format(team)
    x = c.execute(sub).fetchone()
    y = x == None
    return jsonify(res = y)

@app.route("/redirect")
def redir():
    return render_template('redirect.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        trainer = Trainer.query.filter_by(username=form.username.data).first()
        if trainer:
            print trainer
            #Should look into flashing username already taken.
            return render_template('register.html', form=form)
        if form.password1.data != form.password2.data:
            print 'non-pass match'
            #Should look into doing some banner flash in flask
            return render_template('register.html', form=form)
        newuser = Trainer(form.username.data, form.password1.data)
        db.add(newuser)
        db.commit()
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        trainer = Trainer.query.filter_by(username=form.username.data).first()
        if not trainer:
            print 'invalid user'
            return render_template('login.html', form=form)
        elif not trainer.check_password(form.password.data):
            print 'invalid password'
            return render_template('login.html', form=form)
        login_user(trainer)
    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    mode = Server.query.first().mode
    form = PartySignup()
    #TODO: move enums to Server model.
    if mode == 'party' and form.validate_on_submit():
        #should put first 150 pokemon in the all pokemon list and just use
        #that for annonimous users.
        newteam = {'name' : form.teamname.data,
                   'pokemon': None}
        r.rpush('lineup', newteam)
        return redirect(url_for('accepted'))
    elif mode == 'battle':
        return redirect(url_for('battle'))
    return render_template('signup.html', form=form)

@app.route("/battle", methods=['GET, POST'])
@login_required
def battle():
    mode = Server.query.first().mode
    if mode != 'battle':
        #popup something about changing the gametype
        pass
    form = BattleSignup()
    if form.validate_on_submit():
        #"pokemon" relationship does not currently exist in the user model,
        #need to make
        form.pokemon.choices = [(pokemon.id, pokemon.name)
                                    for pokemon in current_user.pokemon]
        newteam = {'name' : current_user.uesrname,
                    'pokemon': form.pokemon.data}
        r.rpush('linup', newteam)
        return redirect(url_for('accepted'))
    return render_template('battle', form=form)

@app.route("/admin/manage", methods=['GET', 'POST'])
@login_required
def manage():
    if not current_user.admin:
        #404 unauthorized or you are not an admin page or something.
        pass
    form = Server()
    if form.validate_on_submit():


if __name__ == "__main__":
    app.debug = True
    app.run(host='pokepong', port=80)
