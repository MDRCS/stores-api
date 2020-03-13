from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity
from src.models.store import Store


class StoresList(Resource):

    @jwt_optional
    def get(self):
        claims = get_jwt_claims()
        user_id = get_jwt_identity()

        if user_id:
            if not claims['is_admin']:
                return {'stores': [store.name for store in Store.query.all()],
                        'message': 'you don''t have the permission to do that !'
                        }, 200

        return {"stores": [store.json() for store in Store.query.all()]}, 200


class Store_(Resource):

    @jwt_required
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

    @jwt_required
    def post(self):
        data = AddStore.parser.parse_args()
        store = Store(data['name'])
        store.insert()
        return store.json(), 200
