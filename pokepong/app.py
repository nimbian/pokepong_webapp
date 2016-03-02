from flask import Flask, render_template, redirect, request, jsonify
from time import sleep
from pokepong.forms import Register
from pokepong.models import Trainer
from pokepong.database import db
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


if __name__ == "__main__":
    app.debug = True
    app.run(host='pokepong', port=80)
