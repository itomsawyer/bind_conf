import os

from config import app_config
from app import create_app

runmode="dev"
app = create_app(runmode)
lh = app_config[runmode].LISTEN_HOST
lp = app_config[runmode].LISTEN_PORT

if __name__ == '__main__':
    app.run(host=lh, port=lp, threaded=True)
