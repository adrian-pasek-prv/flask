import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores


blp = Blueprint('items', __name__, description='Operations on items')

# When calling GET/DELETE on "/item/<string:item_id" endpoint blueprint will route these requests
# to Item class methods
@blp.route('/item/<string:item_id>')
class Item(MethodView):
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
            
    def put(self, item_id):
        item_data = request.get_json()
        if (
            'price' not in item_data
            or 'name' not in item_data
        ):
            abort(
                400,
                messsage="Bad request. Ensure 'price', and 'name' are included in JSON payload."
            )
            
        try:
            items[item_id] = item_data
            return {'message': 'Item updated.'}
        except KeyError:
            abort(404, message="Item not found.")
            

@blp.route('/item')
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}
    
    def post(self):
        item_data = request.get_json()
        # Validate if request is good and contains necessary keys
        # Data types input validation should also be included
        
        if (
            'price' not in item_data
            or 'store_id' not in item_data
            or 'name' not in item_data
        ):
            abort(
                400,
                messsage="Bad request. Ensure 'price', 'store_id', and 'name' are included in JSON payload."
            )
            
        for item in items.values():
            if (
                item_data['name'] == item['name']
                and item_data['store_id'] == item['store_id']
            ):
                item_name = item_data['name']
                store_id = item_data['store_id']
                abort(400, message=f"Item '{item_name}' already exists in store '{store_id}'")
                
        if item_data['store_id'] not in stores:
            abort(404, message='Store not found.')
    
        item_id = uuid.uuid4().hex
        item = {**item_data, 'id': item_id}
        items[item_id] = item
        
        return item