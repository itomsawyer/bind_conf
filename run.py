import os

from config import app_config
from app import create_app

if __name__ == '__main__':
    runmode = app_config["common"].RUN_MODE
    if not runmode in app_config:
        raise Exception("* Run mode " + runmode + " does not exists, check your config.py")

    print (" * Run mode:" , runmode)
    app = create_app(runmode)
    lh = app_config[runmode].LISTEN_HOST
    lp = app_config[runmode].LISTEN_PORT

    app.run(host=lh, port=lp, threaded=True)
