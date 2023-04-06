import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


###################################
######### STORE ENDPOINTS #########
###################################

@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.get('/store/<string:store_id>') # string:name allows us to access name var in the URL
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message='Store not found.')


@app.post("/store")
def create_store():
    store_data = request.get_json()
    
    if 'name' not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in JSON payload"
        )
        
    for store in stores.values():
        if store_data['name'] == store['name']:
            store_name = store_data['name']
            abort(400, message=f"Store '{store_name}' already exists.")
            
    store_id = uuid.uuid4().hex
    store = {**store_data, 'id': store_id}
    stores[store_id] = store
    # return 201 as response code that says I've accepted your payload and processed it successfully
    return store, 201

        
@app.delete('/store/<string:store_id>') # string:name allows us to access name var in the URL
def delete_store(store_id):
    try:
        del stores[store_id]
        return {'message': 'Store deleted.'}
    except KeyError:
        abort(404, message='Store not found.')
        
###################################
######### ITEM ENDPOINTS ##########
###################################

@app.post('/item')
def create_item():
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
    
    return item, 201


@app.get("/item")
def get_items():
    return {"items": list(items.values())}


@app.get('/item/<string:item_id>') # string:name allows us to access name var in the URL
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message='Item not found.')


@app.delete('/item/<string:item_id>') # string:name allows us to access name var in the URL
def delete_item(item_id):
    try:
        del items[item_id]
        return {'message': 'Item deleted.'}
    except KeyError:
        abort(404, message='Item not found.')
     
        
@app.put('/item/<string:item_id>')
def update_item(item_id):
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
