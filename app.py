from flask import Flask
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

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

# Connect flask_smorest to Flask app
api = Api(app)

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)