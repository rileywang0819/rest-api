from werkzeug.security import safe_str_cmp
from resources.user import UserModel


def authenticate(name, pw):
    """Authenticate a user."""
    user = UserModel.find_by_username(name)
    if user and safe_str_cmp(user.password, pw):
        return user


def identity(payload):
    """Identify a user.

    payload: the contents of JWT Token
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
