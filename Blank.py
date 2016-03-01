import flask
import flask.ext.login as flask_login
from wtforms import Form, StringField, PasswordField
class SimpleForm(Form):
    content = StringField('content')
form = SimpleForm(content='foobar')
app = flask.Flask(__name__)
app.secret_key = "mykeyftw"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class LoginForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
        if not next_is_valid(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)



if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1', port=5555)