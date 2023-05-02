import os 

# Flask imports
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
# Package used to load enviroment variables from .env files
from dotenv import load_dotenv

# Import SQLAlachemy related objects
from db import db
import models
from blocklist import BLOCKLIST

# Import Blueprints
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

# Encapsulate app config and setup into a function
def create_app(db_url=None):
    app = Flask(__name__)
    # Find .env file and populate env variables to be seen by os.getenv
    load_dotenv()

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
    
    # Create an instance of Migrate object
    migrate = Migrate(app, db)

    # Connect flask_smorest to Flask app
    api = Api(app)
    
    # Create JWT instance and config a secret key that will ensure that JWT (access token) coming from user comes from
    # known application
    app.config['JWT_SECRET_KEY'] = 'test'
    jwt = JWTManager(app)
    
    # Customize jwt related messages
    
    # Check if token is on a blocklist (it expired after logging out)
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        # return a token unique id if it's in a BLOCKLIST
        return jwt_payload['jti'] in BLOCKLIST
    # You can add info to JWT such as if user id == 1 then it's an admin and use that info in resources
    
    # This will only be called when above function returns True
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({'description': 'The token has been revoked.', 'error': 'token_revoked'}),
            401
        )
        
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    'description': 'The token is not fresh.',
                    'error': 'fresh_token_required'
                }
            )
        )
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {'is_admin': True}
        return {'is_admin': False}
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )
    

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    
    
    return app