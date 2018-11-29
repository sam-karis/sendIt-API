from flask_jwt_extended import (create_access_token, get_jwt_identity)
from flask_json import JsonError


# local imports
from api.models.roles import Role

role = Role()

def get_user_identity():
    current_user = get_jwt_identity()
    return current_user


def admin_required(func):
    def wrapper(*args, **kwargs):
        user = get_user_identity()
        role_id = {'id': str(user['role_id'])}
        user_role = role.query_role(**role_id)
        if user_role['role'] !=  'admin':
            raise JsonError(error="You don't have access to this functionality.", status_=401)
        return func(*args, **kwargs)
    return wrapper
