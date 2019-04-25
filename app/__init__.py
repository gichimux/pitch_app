from flask import Flask
from flask_bootstrap import Bootstrap
from config import config_options

bootstrap = Bootstrap()

def create_app(config_name):

    app = Flask(__name__)

    #create app configurations
    app.config.from_object(config_options[config_name])

    #initialize flask extensions
    bootstrap.init_app(app)

    return app