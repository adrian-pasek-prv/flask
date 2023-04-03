from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "my item",
                "price": 15.99
            }
        ]
    }
]

@app.get("/store")
def get_stores():
    return {"stores": stores}


@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {'name': request_data['name'], 'items': []}
    stores.append(new_store)
    # return 201 as response code that says I've accepted your payload and processed it successfully
    return new_store, 201


@app.post('store/<string:name>/item') # string:name allows us to access name var in the URL
def create_item(name):
    pass
