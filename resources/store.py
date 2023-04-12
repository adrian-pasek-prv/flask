import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import StoreSchema


blp = Blueprint('stores', __name__, description='Operations on stores')

# When calling GET/DELETE on "/store/<string:store_id>" endpoint blueprint will route these requests
# to Store class methods
@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message='Store not found.')
    
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {'message': 'Store deleted.'}
        except KeyError:
            abort(404, message='Store not found.')

@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True)) # return list of stores not a single store, thus we create instance of StoreSchema with many=True
    def get(self):
        return stores.values()
    
    # Decorate function with StoreSchema marshmellow validation that returns validated "store_data" json
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data['name'] == store['name']:
                store_name = store_data['name']
                abort(400, message=f"Store '{store_name}' already exists.")
                
        store_id = uuid.uuid4().hex
        store = {**store_data, 'id': store_id}
        stores[store_id] = store

        return store