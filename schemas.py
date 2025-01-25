from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True) # dump_only means that this field just returns from API
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Int(required=True)

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)