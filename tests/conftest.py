import pytest
import os
import json

# Local imports
from app import create_app
from api.models.database import Migrate
from api.models.users import User
from api.models.roles import Role


@pytest.fixture(scope='module')
def client():
    config_name = os.getenv('FLASK_CONFIG_ENV', default='testing')
    app = create_app(config_name)
    testing_client = app.test_client()
    # create app context
    context = app.app_context()
    context.push()
    Migrate().create_tables()
    yield testing_client
    Migrate().drop_tables()
    context.pop()


@pytest.fixture(scope='module')
def test_user():
    user = {
        "name": "test",
        "username": "test",
        "email": "test@gmail.com",
        "password": "test12323",
        "confirm_password": "test12323"
    }
    return json.dumps(user)


@pytest.fixture(scope='module')
def test_user_login():
    user = {
        "username": "test",
        "password": "test12323"
    }
    return json.dumps(user)


@pytest.fixture(scope='module')
def wrong_user_details():
    user = {
        "username": "test",
        "password": "wrongpassword"
    }
    return json.dumps(user)


@pytest.fixture(scope='module')
def test_admin():
    role = Role()
    filter_role = {'role': 'admin'}
    admin_role = role.query_role(**filter_role)
    admin = {
        'name': 'Admin',
        'username': 'admin',
        'email': 'admin@gmail.com',
        'password': 'admin1234',
        'role_id': str(admin_role['id'])
    }
    return admin


@pytest.fixture(scope='module')
def test_admin_login():
    user = {
        "username": "admin",
        "password": "admin1234"
    }
    return json.dumps(user)


@pytest.fixture(scope='module')
def parcel():
    details = {
        "title": "laptop",
        "destination": "Kasarani",
        "quantity": "3"
    }
    return json.dumps(details)


@pytest.fixture(scope='module')
def new_destination():
    details = {
        "destination": "Kiambu"
    }
    return json.dumps(details)


@pytest.fixture(scope='module')
def new_status():
    details = {
        "status": "In-transit"
    }
    return json.dumps(details)


@pytest.fixture(scope='module')
def new_location():
    details = {
        "current_location": "Cairo"
    }
    return json.dumps(details)


@pytest.fixture(scope='module')
def access_token(client, test_user, test_user_login):
    client.post(
        '/api/v1/auth/signup',
        data=test_user, headers={'content-type': 'application/json'})
    response = client.post(
        '/api/v1/auth/login',
        data=test_user_login, headers={'content-type': 'application/json'})
    return json.loads(response.data)['access_token']


@pytest.fixture(scope='module')
def admin_access_token(client, test_admin, test_admin_login):
    User().save(**test_admin)
    response = client.post(
        '/api/v1/auth/login',
        data=test_admin_login, headers={'content-type': 'application/json'})
    return json.loads(response.data)['access_token']
