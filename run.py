import os

from config import app_config
from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app("dev")
lh = app_config["dev"].LISTEN_HOST
lp = app_config["dev"].LISTEN_PORT

if __name__ == '__main__':
    app.run(host=lh, port=lp, threaded=True)
