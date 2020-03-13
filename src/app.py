import os
from datetime import timedelta

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from src.resources.user import UserRegister, UserLogin, TokenRefresh, UserLogout
from src.resources.item import Item_, ItemRegister, GetOneItem
from src.resources.store import StoresList, AddStore, Store_
from src.backlist import BLACKLIST

app = Flask(__name__)
app.secret_key = os.urandom(16)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'sqlite:///data.db')  # -> sqlite3 was just for tests but if he don't find postgresql link he wil use sqlite

app.config['DEBUG'] = True
app.config['JWT_AUTH_URL_RULE'] = '/login'  # replace path // auth -> login
# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config[
    'PROPAGATE_EXCEPTION'] = True  # return a specific error like jwt anthorized http request not just 404 not found error
# config JWT auth key name to be 'email' instead of default 'username'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'  # username

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

# jwt = JWT(app, authenticate, identity)
jwt = JWTManager(app)  # we should add ourselves /auth endpoint

# adding a piece of data each time we request a token
# data will be attached to jwt
"""
`claims` are data we choose to attach to each jwt payload
and for each jwt protected endpoint, we can retrieve these claims via `get_jwt_claims()`
one possible use case for claims are access level control, which is shown below.
"""


@jwt.user_claims_loader
def add_claims_to_jwt(identity):  # Remember identity is what we define when creating the access token
    if identity == 1:  # instead of hard-coding, we should read from a config file or database to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
def check_if_token_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST  # JTI is JWT ID a unique identifier


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


api = Api(app)

api.add_resource(UserLogin, '/login')
api.add_resource(UserRegister, '/user')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

api.add_resource(Item_, '/items')
api.add_resource(ItemRegister, '/item')
api.add_resource(GetOneItem, '/item/<string:name>')

api.add_resource(StoresList, '/stores')
api.add_resource(Store_, '/store/<string:name>')
api.add_resource(AddStore, '/store')

if __name__ == '__main__':
    from src.database.ORM import db  # avoid circular import

    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()
    app.run(debug=True, port=5000)
