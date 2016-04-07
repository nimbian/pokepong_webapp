from __future__ import absolute_import, print_function
from pokepong.app import create_app


DEBUG = True
SECRET_KEY = 'development key'

app = create_app()
if __name__ == '__main__':
    app.run()
