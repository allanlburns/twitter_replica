from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# all variables based on this application must be instantiated after the app instance


bootstrap = Bootstrap(app)

# flask app instance uses from object method to load in all configuration variables

# this loads all the config attributes into app
app.config.from_object(Config)

# set up db variables
db = SQLAlchemy(app) # takes in app instance to know which variables to use
migrate = Migrate(app, db)

from app import routes
