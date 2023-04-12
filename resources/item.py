import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint('items', __name__, description='Operations on items')

# When calling GET/DELETE on "/item/<string:item_id" endpoint blueprint will route these requests
# to Item class methods
@blp.route('/item/<string:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema) # Decorate a successful response
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message='Item not found.')
    
    def delete(self, item_id):
        try:
            del items[item_id]
            return {'message': 'Item deleted.'}
        except KeyError:
            abort(404, message='Item not found.')
    
    # Decorate function with ItemUpdateSchema marshmellow validation that returns validated "item_data" json
    @blp.arguments(ItemUpdateSchema)  
    @blp.response(200, ItemUpdateSchema)      
    def put(self, item_data, item_id): 
        try:
            items[item_id] = item_data
            return {'message': 'Item updated.'}
        except KeyError:
            abort(404, message="Item not found.")
            

@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True)) # return list of items not a single item, thus we create instance of ItemSchema with many=True
    def get(self):
        return items.values()
    
    # Decorate function with ItemSchema marshmellow validation that returns validated "item_data" json
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # We will use ItemModel to transform received data into an item fit for a databaase
        # **item_data will unpack the object into keyword arguments that ItemModel accepts
        # and uses them later for creating an item in database
        item = ItemModel(**item_data)
        
        # Try to insert item into database
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='An error occured while inserting the item.')
        
        return item