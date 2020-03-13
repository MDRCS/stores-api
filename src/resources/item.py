from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required
from src.models.item import Item


class ItemRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        help="this help cannot be empty!"
                        )

    parser.add_argument('price',
                        type=float,
                        help="this help cannot be empty!"
                        )

    parser.add_argument('store_id',
                        type=int,
                        help="every item needs a store_id!"
                        )

    @fresh_jwt_required  # if you don't have a fresh token you won't login != jwt_required you need just an access token
    def post(self):
        data = ItemRegister.parser.parse_args()
        item = Item(name=data['name'], price=data['price'], store_id=data['store_id'])
        item.insert()
        return item.json()


class Item_(Resource):

    @jwt_required
    def get(self):
        return Item.getAll()


class GetOneItem(Resource):

    @jwt_required
    def get(self, name):
        return Item.getItemByName(name).json()
