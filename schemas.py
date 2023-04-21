# Marshmellow is a tool that enables data validation using Schemas
from marshmallow import Schema, fields


# Config an PlainItemSchema class that will dictate how an item should look like
# in its simplest form
class PlainItemSchema(Schema):
    # dump_only means this field will only be returned
    # it not required as a parameter in request
    id = fields.Int(dump_only=True)
    # required field in the request
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


# This schema will inherit from PlainItemSchema
# and add additional fields related to store of an item
# Store metadata will exists in a nested field that will be populated by PlainStoreSchema
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class ItemUpdateSchema(Schema):
    # These fields are optional
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
    

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    
class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)