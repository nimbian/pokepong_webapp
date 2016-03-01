from pokepong.app import app
from pokepong.config import _cfg, _cfgi, _cfgb

if __name__ == '__main__':
    app.run(host=_cfg("debug-host"), port=_cfgi('debug-port'), debug=True)
