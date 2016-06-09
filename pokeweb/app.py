from flask import Flask
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect


csrf = CsrfProtect()
login_manager = LoginManager()


def create_app(config='pokeweb.config', testing=False):

    app = Flask(__name__)
    app.config.from_object(config)
    #if not testing:
    #    app.config.from_envvar('POKEWEB_SETTINGS')
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'pokeweb.login'

    with app.app_context():
        from pokeweb.views import pokeweb
        from pokeweb.database import init_db
        app.register_blueprint(pokeweb)
        init_db()
    return app
