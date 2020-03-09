from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from src.models.store import Store


class StoresList(Resource):

    @jwt_required()
    def get(self):
       return {"stores": [store.json() for store in Store.query.all()]}, 200


class Store_(Resource):

    @jwt_required()
    def get(self, name):
        return Store.getByName(name)

    def delete(self, name):
        pass


class AddStore(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        help="this help cannot be empty!"
                        )
    @jwt_required()
    def post(self):
        data = AddStore.parser.parse_args()
        store = Store(data['name'])
        store.insert()
        return store.json(), 200
