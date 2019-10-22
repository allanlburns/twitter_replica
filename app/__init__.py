from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config

app = Flask(__name__)

# all variables based on this application must be instantiated after the app instance


bootstrap = Bootstrap(app)

# flask app instance uses from object method to load in all configuration variables

# this loads all the config attributes into app
app.config.from_object(Config)

from app import routes
