from flask_restful import Resource, reqparse

from src.models.user import User


class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('id',
                        type=int,
                        help="this help cannot be empty!"
                        )

    parser.add_argument('email',
                        type=str,
                        help="this help cannot be empty!"
                        )

    parser.add_argument('password',
                        type=str,
                        help="this help cannot be empty!"
                        )

    def post(self):
        # data = request.get_json()
        data = UserRegister.parser.parse_args()
        user = User.getByEmail(data['email'])
        if user is None:
            user = User(data['id'],data['email'],data['password'])
            user.insert()
            return {"message": "The User has been added successfuly!"}

        return {"message": "The Username is duplicated!"}, 400


