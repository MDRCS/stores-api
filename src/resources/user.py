from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, \
    create_refresh_token, \
    get_jwt_identity, \
    jwt_refresh_token_required, \
    jwt_required, \
    get_raw_jwt

from src.models.user import User
from src.backlist import BLACKLIST


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
            user = User(data['id'], data['email'], data['password'])
            user.insert()
            return {"message": "The User has been added successfuly!"}

        return {"message": "The Username is duplicated!"}, 400


class UserLogin(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('email',
                        type=str,
                        help="this help cannot be empty!"
                        )

    parser.add_argument('password',
                        type=str,
                        help="this help cannot be empty!"
                        )

    def post(self):
        data = UserLogin.parser.parse_args()
        user = User.getByEmail(data['email'])

        if user and safe_str_cmp(data['password'], user.password):
            access_token = create_access_token(identity=user.id,
                                               fresh=True)  # when you create a token you have a fresh token
            refresh_token = create_refresh_token(user.id)
            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token
                   }, 200

        return {'message': 'invalid credentials !!'}


class UserLogout(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # JTI is JWT ID a unique identifier
        BLACKLIST.add(jti)
        return {"message": "successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user,
                                        fresh=False)  # when you are refreshing token you don't have a fresh token
        return {"access_token": new_token}, 200
