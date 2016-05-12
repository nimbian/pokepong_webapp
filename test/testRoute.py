import unittest
from pokepong.app import create_app

class Route(unittest.TestCase):
    TESTING = True
    DEBUG = True
    REDIS_CONNECTION = 'redis://localhost:6379/0'
    SECRET_KEY = 'testing key'
    WTF_CSRF_ENABLED = False

    def setUp(self):
        self.CONNECTION_STRING = 'sqlite://'
        self.app = create_app(self, testing=True)
        self.test_client = self.app.test_client()
        self.register('validtrainer', 'validpass', 'validpass', 1)
        with self.app.app_context():
            from pokepong.red import r
            self.r = r
            self.r.flushdb()

    def tearDown(self):
        with self.app.app_context():
            from pokepong.database import engine, db
            db.close()
            engine.dispose()

    def login(self, username, password):
        return self.test_client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.test_client.get('/logout', follow_redirects=True)

    def register(self, username, password1, password2, pokemon):
        return self.test_client.post('/register', data=dict(
            username=username,
            password1=password1,
            password2=password2,
            pokemon=pokemon
        ), follow_redirects=True)

    def set_mode(self, mode):
        self.r.set('mode', mode)

    def party_signup(self, teamname, player1, player2, pokemon=None):
        return self.test_client.post('/signup', data=dict(
            teamname=teamname,
            player1=player1,
            player2=player2,
            pokemon=pokemon
        ), follow_redirects=True)

    def battle_signup(self, pokemon=None):
        return self.test_client.post('/battle', data=dict(
            pokemon=pokemon
        ), follow_redirects=True)

    def lineup(self):
        return self.test_client.get('/lineup')

    def admin_change(self, mode='', purge=False):
        return self.test_client.post('/admin', data=dict(
            mode=mode,
            purge=purge), follow_redirects=False)

    def test_login_logout(self):
        rv = self.login('validtrainer', 'validpass')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('invalidtrainer', 'validpass')
        assert 'Username not found or passwoord is incorrect' in rv.data
        rv = self.login('validtrainer', 'invalidpass')
        assert 'Username not found or passwoord is incorrect' in rv.data

    def test_register(self):
        rv = self.register('validtrainer2', 'validpass2', 'validpass2', 1)
        assert 'Welcome validtrainer2' in rv.data
        rv = self.register('validtrainer', 'validpass', 'validpass', 1)
        assert 'Username already taken, please select another' in rv.data
        rv = self.register('dummytrianer', 'validpass', 'invalidpass', 1)
        assert 'Your passwords did not match, please try again' in rv.data

    def test_party_signup(self):
        self.set_mode('party')
        rv = self.party_signup('testteam1', 'testplayer1', 'testplayer2')
        assert '<th> 1 </th>' in rv.data
        assert '<td> testteam1 </td>' in rv.data
        assert '<td> testplayer1 </td>' in rv.data
        assert '<td> testplayer2 </td>' in rv.data
        self.set_mode('battle')
        rv = self.party_signup('testteam1', 'testplayer1', 'testplayer2')
        assert 'game mode is currently set to battle, \
if you want to party please have an admin change it' in rv.data

    def test_battle_signup(self):
        self.set_mode('battle')
        self.login('validtrainer', 'validpass')
        #TODO: First pokemon will happen to be 152, but could make more robust
        rv = self.battle_signup([152])
        assert '<th> 1 </th>' in rv.data
        assert '<td> validtrainer </td>' in rv.data
        assert 'class="sprite sprite-1"' in rv.data
        self.set_mode('party')
        rv = self.battle_signup([152])
        assert 'game mode is currently set to party, \
if you want to battle please have an admin change it' in rv.data

    def test_empty_linup(self):
        self.set_mode('party')
        rv = self.lineup()
        assert 'nobody is queued up' in rv.data
        self.set_mode('battle')
        rv = self.lineup()
        assert 'nobody is queued up' in rv.data

    def test_admin(self):
        self.register('validtrainer2', 'validpass2', 'validpass2', 1)
        self.login('validtrainer2', 'validpass2')
        rv = self.admin_change()
        assert rv.status_code == 401
        self.logout()
        self.login('validtrainer', 'validpass')
        rv = self.test_client.get('/admin')
        assert rv.status_code == 200
        rv = self.admin_change(mode='battle')
        assert rv.status_code == 200
        rv = self.admin_change(purge=True)
        assert rv.status_code == 200
