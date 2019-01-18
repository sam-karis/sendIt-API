
from flask_restplus import Resource
from flask import jsonify, request
from flask_jwt_extended import (create_access_token)

# Local Imports
from api.helpers.schema.user import (UserSignUpSchema, UserLoginSchema)
from api.models.users import User

user = User()


class RegisterUserResource(Resource):

    def post(self):
        request_data = request.get_json()
        new_user_data = UserSignUpSchema().load_json_data(request_data)
        new_user_data.pop('confirm_password')
        user.save(**new_user_data)

        response = jsonify({'message': 'user created successfully'})
        response.status_code = 201
        return response


class LoginUserResource(Resource):

    def post(self):
        user_credentials = request.get_json()
        logged_user = UserLoginSchema().load_json_data(user_credentials)
        logged_user_data = {'username': logged_user['username']} if 'username' in user_credentials else {  # noqa E501
            'email': logged_user['email']}
        user_from_db = user.query_user(**logged_user_data)

        if user_from_db:
            if user.verify_password(user_from_db['password'], logged_user['password']):  # noqa E501
                user_from_db.pop('password')
                access_token = create_access_token(identity=user_from_db)
                return jsonify({
                    'message': 'Login success',
                    'user': user_from_db,
                    'access_token': access_token
                })
        response = jsonify({'message': 'Invalid username or password'})
        response.status_code = 401
        return response
