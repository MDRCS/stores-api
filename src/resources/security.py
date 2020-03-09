from werkzeug.security import safe_str_cmp
from src.models.user import User


def authenticate(email, password):
    """
    :param email: required field -> (key, value)
    :param password: required field -> (key, value)
    :return:
    """
    user = User.getByEmail(email)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.getById(user_id)
