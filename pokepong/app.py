from flask import Flask
from flask.ext.login import  LoginManager
from pokepong import config as c


def create_app(config='pokepong.config', test=False):

    app = Flask(__name__)
    app.config.from_object(config)
    if test:
        app.config.from_envvar('POKEPONG_SETTINGS')
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'pokepong.login'

    with app.app_context():
        from pokepong.views import pokepong
        from pokepong.database import init_db
        app.register_blueprint(pokepong)
        init_db()
    return app
