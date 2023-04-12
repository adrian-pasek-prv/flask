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
        # We will use StoreModel to transform received data into a store fit for a databaase
        # **store_data will unpack the object into keyword arguments that StoreModel accepts
        # and uses them later for creating a store in database
        store = StoreModel(**store_data)
        
        # Try to insert store into database
        try:
            db.session.add(store)
            db.session.commit()
        # Catch exception related to integrity of database 
        # In this case it's uniquness of store
        except IntegrityError:
            abort(400,
                  message='A store with that name already exists.')
        except SQLAlchemyError:
            abort(500, message='An error occured while inserting the store.')

        return store