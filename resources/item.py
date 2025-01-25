import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    
    def get(self, item_id):
        try:
            return {"item": items[item_id]}, 200
        except KeyError:
            abort(404, message="Item not found!")

    @blp.arguments(ItemUpdateSchema)        
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data # in-place modification

            return {"item": item}, 200
        except KeyError:
            abort(404, message="Item not found!")
    
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted!"}, 200
        except KeyError:
            abort(404, message="Item not found!")

@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}
    
    @blp.arguments(ItemSchema)
    def post(self, item_data):
        for item in items.values():
            if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
                abort(400, message=f"Item already exists!")

        if item_data["store_id"] not in stores:
            abort(404, message="Store not found!")
        
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        
        return item, 201
    
    