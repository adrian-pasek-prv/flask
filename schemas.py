# Marshmellow is a tool that enables data validation using Schemas
from marshmallow import Schema, fields

# Config an ItemSchema class that will dictate how an item should look like
class ItemSchema(Schema):
    # dump_only means this field will only be returned
    # it not required as a parameter in request
    id = fields.Str(dump_only=True)
    # required field in the request
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)
    
class ItemUpdateSchema(Schema):
    # These fields are optional
    name = fields.Str()
    price = fields.Float()
    
class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    
    