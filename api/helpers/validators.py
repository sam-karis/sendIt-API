
import re
from flask_json import JsonError


def validate_email(email):
    valid = re.match(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email.strip())
    if valid is None:
        return False
    return True


def validate_id(id_type, id_param, current_user={}):
    try:
        int(id_param)
    except ValueError:
        raise JsonError(error=f'Invalid {id_type}, it must be an integer.')
    if id_type == 'user id' and current_user:
        if current_user['id'] != int(id_param):
            raise JsonError(
                error=f'Cannot access parcels for user id {id_param}.')
