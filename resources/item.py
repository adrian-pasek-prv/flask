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
        # Use Flask SQLAlchemy query method to retrive item from DB
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Item deleted.'}
    
    # Decorate function with ItemUpdateSchema marshmellow validation that returns validated "item_data" json
    @blp.arguments(ItemUpdateSchema)  
    @blp.response(200, ItemUpdateSchema)      
    def put(self, item_data, item_id): 
        item = ItemModel.query.get(item_id)
        # Make sure PUT method is idempotend. 
        # If item doesn't exists create it with ItemModel, if it does update it. The end result is the same
        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else:
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()
        
        return item
            

@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True)) # return list of items not a single item, thus we create instance of ItemSchema with many=True
    def get(self):
        # .query.all() enables to query a list of items and pass it to ItemSchema where many=True
        return ItemModel.query.all()
    
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