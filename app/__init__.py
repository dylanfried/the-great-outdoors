# Extended version of flask that handles YAML config files
from flask_extended import Flask

def create_app(config_override={}):
    # Define the WSGI application object
    app = Flask(__name__)

    # Configuration
    app.config.from_yaml('config/config.yaml')

    return app