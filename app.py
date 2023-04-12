import os 

# Flask imports
from flask import Flask
from flask_smorest import Api

# Import SQLAlachemy related objects
from db import db
import models

# Import Blueprints
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

# Encapsulate app config and setup into a function
def create_app(db_url=None):
    app = Flask(__name__)

    # Propagate exceptions that exists in scripts in resources folder
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = 'Stores REST API'
    app.config['API_VERSION'] = 'v1'
    # Config OPENAPI, which is a standard for API documentation
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    # Config SQLAlchemy db, for development we use SQLite so we don't have to specify user and password
    # We will migrate to Postgres later on where we will specify it's connection (password/user) to DATABASE_URL env variable
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABASE_URL', 'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Connect flask app to SQLAlchemy
    db.init_app(app)

    # Connect flask_smorest to Flask app
    api = Api(app)
    
    # Make sure SQLAlchemy will create tables if they don't exists before first request
    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    
    return app